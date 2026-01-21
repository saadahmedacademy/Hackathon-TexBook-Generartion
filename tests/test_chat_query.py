import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.backend.main import app, agent_core
from src.backend.models import ChatResponse, Document
from src.retrieval.models import ContentChunk

client = TestClient(app)

@patch('src.backend.agent_core.embed_query')
@patch('src.backend.agent_core.search_qdrant')
def test_chat_query_successful_rag(mock_search_qdrant, mock_embed_query):
    """
    Test a successful RAG query where context is found and an answer is generated.
    """
    # Mock the inputs and outputs
    mock_embed_query.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.return_value = [
        ContentChunk(doc_id='doc1', source_url='/test', text='This is a test chunk.', score=0.9, metadata={'title': 'Test Title'})
    ]
    
    with patch.object(agent_core, 'gemini_client', MagicMock()) as mock_gemini_client:
        mock_gemini_client.query_llm.return_value = "This is a test answer."

        # Make the request
        response = client.post("/chat/query", json={"question": "What is a test?"})

        # Assert the response
        assert response.status_code == 200
        chat_response = ChatResponse(**response.json())
        assert chat_response.answer == "This is a test answer."
        assert "Sources" not in chat_response.answer
        assert len(chat_response.citations) == 1
        assert chat_response.citations[0].source_id == 'doc1'
        assert chat_response.citations[0].title == 'Test Title'
        assert chat_response.status == "success"

@patch('src.backend.agent_core.embed_query')
@patch('src.backend.agent_core.search_qdrant')
def test_chat_query_empty_retrieval_refusal(mock_search_qdrant, mock_embed_query):
    """
    Test the refusal mechanism when no relevant context is found.
    """
    # Mock the inputs and outputs
    mock_embed_query.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.return_value = [] # No chunks found

    with patch.object(agent_core, 'gemini_client', MagicMock()) as mock_gemini_client:
        # Make the request
        response = client.post("/chat/query", json={"question": "An obscure question."})

        # Assert the response
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["citations"] == []
        assert response_json["answer"] == ""
        assert response_json["status"] == "refused"
        assert response_json["refusal_reason"] is not None
        
        # Ensure Gemini was not called
        mock_gemini_client.query_llm.assert_not_called()

def test_chat_query_greeting():
    """
    Test the system's response to a simple greeting.
    """
    # Make the request
    response = client.post("/chat/query", json={"question": "hello"})

    # Assert the response
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["citations"] == []
    assert "Hi! I can help" in response_json["answer"]
    assert response_json["status"] == "system"

def test_chat_query_invalid_module():
    """
    Test the refusal mechanism when an invalid module is queried.
    """
    # Make the request
    response = client.post("/chat/query", json={"question": "Tell me about module 99"})

    # Assert the response
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["citations"] == []
    assert response_json["answer"] == ""
    assert response_json["status"] == "refused"
    assert "I cannot provide information for Module 99" in response_json["refusal_reason"]

def test_chat_query_vague_term():
    """
    Test that a vague term like "ros 2" gets a canned response and no sources.
    """
    response = client.post("/chat/query", json={"question": "ros 2"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["citations"] == []
    assert "That's a very general question" in response_json["answer"]
    assert response_json["status"] == "system"

def test_chat_query_identity_question():
    """
    Test that an identity question like "who are you" gets a canned response and no sources.
    """
    response = client.post("/chat/query", json={"question": "who are you"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["citations"] == []
    assert "I am a helpful assistant" in response_json["answer"]
    assert response_json["status"] == "system"

@patch('src.backend.agent_core.embed_query')
@patch('src.backend.agent_core.search_qdrant')
def test_chat_query_retrieval_exception(mock_search_qdrant, mock_embed_query):
    """
    Test the refusal mechanism when Qdrant retrieval fails.
    """
    # Mock the inputs and outputs
    mock_embed_query.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.side_effect = Exception("Qdrant is down")

    with patch.object(agent_core, 'gemini_client', MagicMock()) as mock_gemini_client:
        # Make the request
        response = client.post("/chat/query", json={"question": "A question that will fail."})

        # Assert the response
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["citations"] == []
        assert response_json["answer"] == ""
        assert response_json["status"] == "refused"
        assert response_json["refusal_reason"] is not None
        
        # Ensure Gemini was not called
        mock_gemini_client.query_llm.assert_not_called()

@patch('src.backend.agent_core.embed_query')
@patch('src.backend.agent_core.search_qdrant')
def test_source_stripping_from_llm_answer(mock_search_qdrant, mock_embed_query):
    """
    Test that 'Sources:', 'References:', etc., are correctly stripped from the LLM's output.
    """
    # Mock the inputs and outputs
    mock_embed_query.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.return_value = [
        ContentChunk(doc_id='doc1', source_url='/test', text='This is a test chunk.', score=0.9, metadata={'title': 'Test Title'})
    ]
    
    # Mock the Gemini client to return an answer with a "Sources" section
    with patch.object(agent_core, 'gemini_client', MagicMock()) as mock_gemini_client:
        mock_gemini_client.query_llm.return_value = "This is the main answer.\n\nSources: doc1"

        # Make the request
        response = client.post("/chat/query", json={"question": "What is a test?"})

        # Assert the response
        assert response.status_code == 200
        chat_response = ChatResponse(**response.json())
        
        # The core assertion: The 'Sources' section should be stripped
        assert chat_response.answer == "This is the main answer."
        assert "Sources" not in chat_response.answer
        
        # Citations should still be present in the structured data
        assert len(chat_response.citations) == 1
        assert chat_response.citations[0].source_id == 'doc1'
        assert chat_response.status == "success"
