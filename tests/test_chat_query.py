import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from src.backend.main import app
from src.backend.models import ChatResponse, Citation

# Mock the RetrievalTool and GeminiAdapter
@pytest.fixture
def mock_retrieval_tool():
    tool = MagicMock()
    tool.name = "retrieve_textbook_context"
    # Mock a successful retrieval
    tool.return_value = '{"status": "success", "context": [{"text": "ROS 2 nodes are ...", "source_url": "/docs/node-basics", "section_heading": "ROS 2 Nodes"}]}'
    return tool

@pytest.fixture
def mock_gemini_adapter():
    adapter = MagicMock()
    # Mock a successful Gemini generation
    adapter.generate.return_value = "A ROS 2 node is an executable that uses the ROS 2 client library. (Citation: /docs/node-basics, Section: ROS 2 Nodes)"
    return adapter

@pytest.mark.asyncio
async def test_chat_query_grounded_answer(mock_retrieval_tool, mock_gemini_adapter):
    """
    Test successful grounded Q&A with citations.
    """
    with patch("src.backend.tools.RetrievalTool", return_value=mock_retrieval_tool):
        with patch("src.backend.llm_adapter.GeminiAdapter", return_value=mock_gemini_adapter):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/chat/query", json={"question": "What is a ROS 2 node?"})
            
            assert response.status_code == 200
            chat_response = ChatResponse(**response.json())
            assert "ROS 2 node" in chat_response.answer
            assert len(chat_response.citations) > 0
            assert chat_response.refusal_reason is None
            
            mock_retrieval_tool.assert_called_once()
            mock_gemini_adapter.generate.assert_called_once()

@patch("src.backend.tools.RetrievalTool")
@patch("src.backend.llm_adapter.GeminiAdapter")
@pytest.mark.asyncio
async def test_chat_query_refusal_no_context(mock_gemini_adapter_cls, mock_retrieval_tool_cls):
    """
    Test agent refusal when retrieval tool returns no context.
    """
    mock_retrieval_tool = mock_retrieval_tool_cls.return_value
    mock_retrieval_tool.return_value = '{"status": "no_context", "message": "No relevant context found."}'
    mock_gemini_adapter = mock_gemini_adapter_cls.return_value
    mock_gemini_adapter.generate.return_value = "I cannot answer your question based on the available information."

    with patch("src.backend.tools.RetrievalTool", return_value=mock_retrieval_tool):
        with patch("src.backend.llm_adapter.GeminiAdapter", return_value=mock_gemini_adapter):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/chat/query", json={"question": "Tell me about advanced quantum physics."})
            
            assert response.status_code == 200
            chat_response = ChatResponse(**response.json())
            assert chat_response.answer == "I cannot answer your question based on the available information."
            assert len(chat_response.citations) == 0
            assert chat_response.refusal_reason == "No relevant context found for the query."

            mock_retrieval_tool.assert_called_once()
            mock_gemini_adapter.generate.assert_called_once()
