from .gemini_client import GeminiClient
from .prompts import QA_PROMPT, CODE_QA_PROMPT, PYTEST_GENERATION_PROMPT
from .models import Query, ChatResponse, Document
from ..retrieval.embedder import get_cohere_client, embed_query
from ..retrieval.vector_db import get_qdrant_client, search_qdrant
from ..retrieval.config import QDRANT_COLLECTION_NAME

class AgentCore:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.cohere_client = get_cohere_client()
        self.qdrant_client = get_qdrant_client()
        self.greetings = {"hi", "hello", "hey", "hi!", "hello!", "hey!"}

    def answer_question(self, query: Query) -> ChatResponse:
        """
        Answers a question using a RAG pipeline.
        """
        normalized_question = query.question.lower().strip()

        if normalized_question in self.greetings:
            return ChatResponse(
                answer="Hi! I can help you with questions about the ROS 2 textbook. What would you like to learn?",
                citations=[],
                status="system",
                refusal_reason=None
            )

        # Embed the user's query
        query_vector = embed_query(self.cohere_client, query.question)

        # Search for relevant context in Qdrant
        retrieved_chunks = search_qdrant(
            client=self.qdrant_client,
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=5,
            score_threshold=0.5,
        )

        if not retrieved_chunks:
            return ChatResponse(
                answer="",
                citations=[],
                status="refused",
                refusal_reason="I could not find any relevant information in the ROS 2 textbook for your query."
            )

        # Format context for the LLM
        context = "\n".join([chunk.text for chunk in retrieved_chunks])
        
        if query.code_block:
            prompt = CODE_QA_PROMPT.format(context=context, code=query.code_block, question=query.question)
        else:
            prompt = QA_PROMPT.format(context=context, question=query.question)
            
        llm_response = self.gemini_client.query_llm(prompt)
        
        citations = [
            Document(source_id=chunk.doc_id, content=chunk.text) for chunk in retrieved_chunks
        ]
        
        return ChatResponse(answer=llm_response, citations=citations, status="success")

    def generate_pytest(self, code: str) -> str:
        """
        Generates Pytest unit tests for a given code block.
        """
        prompt = PYTEST_GENERATION_PROMPT.format(code=code)
        llm_response = self.gemini_client.query_llm(prompt)
        return llm_response
