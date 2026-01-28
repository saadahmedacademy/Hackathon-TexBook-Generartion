from .gemini_client import GeminiClient
from .prompts import SYNTHESIS_PROMPT, CODE_QA_PROMPT, PYTEST_GENERATION_PROMPT
from .models import Query, ChatResponse, Document
from .config import DEFAULT_TOP_K, DEFAULT_SCORE_THRESHOLD
from retrieval.embedder import embed_query
from retrieval.vector_db import (
    get_qdrant_client,
    search_qdrant,
    check_collection_exists,
)
from retrieval.config import QDRANT_COLLECTION_NAME
import logging
import re


class AgentCore:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.qdrant_client = get_qdrant_client()

        self.greetings = {
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
        }

        self.identity_questions = {
            "what is your name",
            "what's your name",
            "who are you",
        }

        self.vague_terms = {"ros", "ros 2", "robotics"}

        self.conversational_questions = {
            "how are you",
            "how are you doing",
            "how's it going",
            "what's up",
            "what are you",
        }

        self._module_mapping = {
            "1": "ROS Foundations",
            "2": "Nodes, Topics, and Services",
            "3": "URDF and Humanoid Simulation",
            "4": "Perception and SLAM",
            "5": "Navigation and Manipulation",
            "6": "Vision, Language, and Action",
        }

    # --------------------------------------------------
    # Query preprocessing
    # --------------------------------------------------
    def _preprocess_query(self, question: str) -> tuple[str, bool, bool]:
        match = re.search(r"\b(module|chapter)\s+(\d+)\b", question, re.IGNORECASE)

        if match:
            module_number = match.group(2)
            if module_number in self._module_mapping:
                module_title = self._module_mapping[module_number]
                expanded_query = (
                    f"Explain {module_title} (Module {module_number}) from the ROS 2 textbook."
                )
                logging.info(f"Expanded module query: {expanded_query}")
                return expanded_query, True, True
            return question, True, False

        return question, False, False

    # --------------------------------------------------
    # Main RAG pipeline
    # --------------------------------------------------
    def answer_question(self, query: Query) -> ChatResponse:
        normalized = query.question.lower().strip().rstrip("?!. ")

        # ---- Greetings (robust for HF Gradio) ----
        if any(normalized.startswith(g) for g in self.greetings):
            return ChatResponse(
                answer="Hi! I can help you with questions about the ROS 2 textbook. What would you like to learn?",
                status="system",
                citations=[],
                refusal_reason=None,
            )

        if any(normalized.startswith(q) for q in self.identity_questions):
            return ChatResponse(
                answer="I am a ROS 2 textbook assistant designed to answer questions using verified textbook content.",
                status="system",
                citations=[],
                refusal_reason=None,
            )

        if normalized in self.vague_terms:
            return ChatResponse(
                answer=(
                    "That topic is quite broad. Could you ask a more specific ROS 2 question? "
                    "For example, nodes, topics, services, or navigation."
                ),
                status="system",
                citations=[],
                refusal_reason=None,
            )

        if any(normalized.startswith(q) for q in self.conversational_questions):
            return ChatResponse(
                answer="I'm here to help with ROS 2 textbook questions 🙂",
                status="system",
                citations=[],
                refusal_reason=None,
            )

        # ---- Preprocess module queries ----
        processed_question, is_module_query, is_valid_module = self._preprocess_query(
            query.question
        )

        if is_module_query and not is_valid_module:
            return ChatResponse(
                answer="",
                status="refused",
                citations=[],
                refusal_reason="That module is not part of the indexed ROS 2 textbook (valid modules: 1–6).",
            )

        # ---- Embedding ----
        try:
            query_vector = embed_query(processed_question)
        except Exception:
            logging.exception("Embedding failed")
            return ChatResponse(
                answer="",
                status="error",
                citations=[],
                refusal_reason="Failed to process your question. Please try again.",
            )

        # ---- Qdrant readiness ----
        if not check_collection_exists(self.qdrant_client, QDRANT_COLLECTION_NAME):
            return ChatResponse(
                answer="",
                status="error",
                citations=[],
                refusal_reason="The knowledge base is not initialized yet.",
            )

        # ---- Retrieval ----
        try:
            retrieved_chunks = search_qdrant(
                client=self.qdrant_client,
                collection_name=QDRANT_COLLECTION_NAME,
                query_vector=query_vector,
                limit=DEFAULT_TOP_K,
                score_threshold=DEFAULT_SCORE_THRESHOLD,
            )
        except Exception:
            logging.exception("Qdrant search failed")
            retrieved_chunks = []

        if not retrieved_chunks:
            logging.info(f"No retrieval for: {processed_question}")
            return ChatResponse(
                answer="",
                status="refused",
                citations=[],
                refusal_reason=(
                    "I could not find relevant information in the ROS 2 textbook. "
                    "Please rephrase or be more specific."
                ),
            )

        # ---- Context assembly ----
        context = "\n\n".join(chunk.text for chunk in retrieved_chunks if chunk.text)

        if not context.strip():
            return ChatResponse(
                answer="",
                status="refused",
                citations=[],
                refusal_reason="Relevant documents were found, but no usable context was available.",
            )

        # ---- Prompt selection ----
        if query.code_block:
            prompt = CODE_QA_PROMPT.format(
                context=context,
                code=query.code_block,
                question=processed_question,
            )
        else:
            prompt = SYNTHESIS_PROMPT.format(
                context=context,
                question=processed_question,
            )

        # ---- LLM ----
        llm_response = self.gemini_client.query_llm(prompt)

        final_answer = re.split(
            r"^\s*(sources?|references?|citations?):",
            llm_response,
            flags=re.IGNORECASE | re.MULTILINE,
        )[0].strip()

        citations = [
            Document(
                source_id=chunk.doc_id,
                content=chunk.text,
                title=chunk.metadata.get("title"),
            )
            for chunk in retrieved_chunks
        ]

        return ChatResponse(
            answer=final_answer,
            citations=citations,
            status="success",
        )

    # --------------------------------------------------
    # Pytest generation
    # --------------------------------------------------
    def generate_pytest(self, code: str) -> str:
        prompt = PYTEST_GENERATION_PROMPT.format(code=code)
        return self.gemini_client.query_llm(prompt)
