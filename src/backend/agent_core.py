from .gemini_client import GeminiClient
from .prompts import SYNTHESIS_PROMPT, CODE_QA_PROMPT, PYTEST_GENERATION_PROMPT
from .models import Query, ChatResponse, Document
from .config import DEFAULT_TOP_K, DEFAULT_SCORE_THRESHOLD
from ..retrieval.embedder import embed_query
from ..retrieval.vector_db import (
    get_qdrant_client,
    search_qdrant,
    check_collection_exists,
)
from ..retrieval.config import QDRANT_COLLECTION_NAME
import logging
import re


class AgentCore:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.qdrant_client = get_qdrant_client()
        self.greetings = {
            "hi", "hello", "hey", "hi!", "hello!", "hey!",
            "good morning", "good afternoon", "good evening",
        }
        self.identity_questions = {"what is your name", "what's your name", "who are you"}
        self.vague_terms = {"ros", "ros 2", "robotics"}
        self.conversational_questions = {
            "how are you", "how are you doing", "how's it going",
            "what's up", "what are you",
        }
        self._module_mapping = {
            "1": "ROS Foundations",
            "2": "Nodes, Topics, and Services",
            "3": "URDF and Humanoid Simulation",
            "4": "Perception and SLAM",
            "5": "Navigation and Manipulation",
            "6": "Vision, Language, and Action",
        }

    def _preprocess_query(self, question: str) -> tuple[str, bool, bool]:
        """
        Expands module/chapter-style queries into semantically meaningful search queries.
        Returns (processed_query, is_module_query, is_valid_module).
        """
        match = re.search(r"\b(module|chapter)\s+(\d+)\b", question, re.IGNORECASE)
        if match:
            module_number = match.group(2)
            if module_number in self._module_mapping:
                module_title = self._module_mapping[module_number]
                expanded_query = f"Tell me about {module_title} (Module {module_number}) in the ROS 2 textbook."
                logging.info(
                    f"Query preprocessed: '{question}' -> '{expanded_query}'"
                )
                return expanded_query, True, True
            else:
                logging.info(f"Invalid module number '{module_number}' detected in query: '{question}'")
                return question, True, False # Module detected but invalid
        return question, False, False # No module detected

    def answer_question(self, query: Query) -> ChatResponse:
        """
        Answers a question using a RAG pipeline.
        """
        normalized_question = query.question.lower().strip().rstrip("?")

        if normalized_question in self.greetings:
            return ChatResponse(
                answer="Hi! I can help you with questions about the ROS 2 textbook. What would you like to learn?",
                status="system",
                citations=[],
                refusal_reason=None,
            )
        
        if normalized_question in self.identity_questions:
            return ChatResponse(
                answer="I am a helpful assistant for the ROS 2 textbook, designed by Spec-Collective.",
                status="system",
                citations=[],
                refusal_reason=None,
            )

        if normalized_question in self.vague_terms:
            return ChatResponse(
                answer="That's a very general question. Could you be more specific about what you'd like to know regarding ROS 2 or robotics? I have access to a textbook that might have the answer.",
                status="system",
                citations=[],
                refusal_reason=None,
            )

        if normalized_question in self.conversational_questions:
            return ChatResponse(
                answer="I am a helpful assistant for the ROS 2 textbook. I can answer your questions about ROS 2.",
                status="system",
                citations=[],
                refusal_reason=None,
            )

        # ---- 1. Preprocess query ----
        preprocessed_question, is_module_query, is_valid_module = self._preprocess_query(query.question)

        if is_module_query and not is_valid_module:
            # Extract the module number from the original query for the refusal message
            module_match = re.search(r"\b(module|chapter)\s+(\d+)\b", query.question, re.IGNORECASE)
            module_num = module_match.group(2) if module_match else "unknown"
            return ChatResponse(
                answer="",
                status="refused",
                citations=[],
                refusal_reason=f"I cannot provide information for Module {module_num} as it is not part of the indexed textbook content. Please specify a valid module number (1-6).",
            )

        # ---- 2. Embed query safely ----
        try:
            query_vector = embed_query(preprocessed_question)
        except Exception as e:
            logging.error("Embedding failed", exc_info=True)
            return ChatResponse(
                answer="",
                status="error",
                citations=[],
                refusal_reason="Failed to generate embeddings. Please try again.",
            )

        # ---- 3. Ensure collection exists ----
        if not check_collection_exists(self.qdrant_client, QDRANT_COLLECTION_NAME):
            return ChatResponse(
                answer="",
                status="error",
                citations=[],
                refusal_reason="Knowledge base is not initialized yet.",
            )

        # ---- 4. Search Qdrant ----
        try:
            retrieved_chunks = search_qdrant(
                client=self.qdrant_client,
                collection_name=QDRANT_COLLECTION_NAME,
                query_vector=query_vector,
                limit=DEFAULT_TOP_K,
                score_threshold=DEFAULT_SCORE_THRESHOLD,
            )
        except Exception as e:
            logging.error(f"Qdrant retrieval failed: {e}", exc_info=True)
            retrieved_chunks = []


        if not retrieved_chunks:
            logging.info(f"No chunks retrieved for query: '{preprocessed_question[:50]}...'")
            return ChatResponse(
                answer="",
                status="refused",
                citations=[],
                refusal_reason="I could not find any relevant information in the ROS 2 textbook for your query. Please try rephrasing your question or making it more specific.",
            )

        # ---- 4.1. Log retrieval results ----
        retrieved_ids = [chunk.doc_id for chunk in retrieved_chunks]
        logging.info(
            f"Query: '{preprocessed_question[:50]}...' - Retrieved {len(retrieved_chunks)} chunks with IDs: {retrieved_ids}"
        )

        # ---- 5. Build context ----
        context = "\n".join(chunk.text for chunk in retrieved_chunks)
        assert context, "Refused to call LLM with empty context"

        if query.code_block:
            prompt = CODE_QA_PROMPT.format(
                context=context,
                code=query.code_block,
                question=preprocessed_question,
            )
        else:
            prompt = SYNTHESIS_PROMPT.format(
                context=context,
                question=preprocessed_question,
            )

        # ---- 6. LLM call ----
        llm_response = self.gemini_client.query_llm(prompt)

        # ---- 7. Format sources & final response ----
        final_answer = re.split(r'^\s*(Sources|Source|References|Citations):', llm_response, flags=re.MULTILINE | re.IGNORECASE)[0].strip()

        citations = [
            Document(source_id=chunk.doc_id, content=chunk.text, title=chunk.metadata.get("title"))
            for chunk in retrieved_chunks
        ]

        return ChatResponse(
            answer=final_answer,
            citations=citations,
            status="success",
        )

    def generate_pytest(self, code: str) -> str:
        """
        Generates Pytest unit tests for a given code block.
        """
        prompt = PYTEST_GENERATION_PROMPT.format(code=code)
        return self.gemini_client.query_llm(prompt)
