import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.retrieval.models import Query, ContentChunk, RetrievedContext
from src.retrieval.main import retrieve_context
from qdrant_client.http.models import Batch, ScoredPoint
import cohere

# Mock Qdrant and Cohere clients
@pytest.fixture
def mock_qdrant_client():
    mock_client = MagicMock()
    mock_client.search.return_value = [
        ScoredPoint(
            id="1",
            vector=None,
            score=0.9,
            payload={
                "doc_id": "doc1",
                "source_url": "url1",
                "text": "text1",
                "section_heading": "head1",
                "content_type": "text",
                "original_text": "original_text1"
            }
        ),
        ScoredPoint(
            id="2",
            vector=None,
            score=0.8,
            payload={
                "doc_id": "doc2",
                "source_url": "url2",
                "text": "text2",
                "section_heading": "head2",
                "content_type": "text",
                "original_text": "original_text2"
            }
        ),
    ]
    return mock_client

@pytest.fixture
def mock_cohere_client():
    mock_client = MagicMock()
    mock_client.embed.return_value = cohere.types.EmbedResponse(
        embeddings=[[0.1, 0.2, 0.3]],
        id="embed_id",
        texts=["test query"]
    )
    return mock_client

# Test cases
@patch("src.retrieval.vector_db.get_qdrant_client")
@patch("src.retrieval.embedder.get_cohere_client")
def test_retrieve_context_success(mock_get_cohere_client, mock_get_qdrant_client, mock_qdrant_client, mock_cohere_client):
    mock_get_qdrant_client.return_value = mock_qdrant_client
    mock_get_cohere_client.return_value = mock_cohere_client

    query_str = "test query"
    collection_name = "test_collection"
    top_k = 2
    score_threshold = 0.7

    result = retrieve_context(query_str, collection_name, top_k, score_threshold)

    assert isinstance(result, RetrievedContext)
    assert result.query == query_str
    assert len(result.chunks) == 2
    assert result.chunks[0].doc_id == "doc1"
    assert result.chunks[0].score == 0.9

    mock_cohere_client.embed.assert_called_once_with(
        texts=[query_str],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    mock_qdrant_client.search.assert_called_once()
    args, kwargs = mock_qdrant_client.search.call_args
    assert kwargs["collection_name"] == collection_name
    assert kwargs["query_vector"] == [0.1, 0.2, 0.3]
    assert kwargs["limit"] == top_k
    assert kwargs["score_threshold"] == score_threshold
    assert kwargs["with_payload"] is True

@patch("src.retrieval.vector_db.get_qdrant_client")
@patch("src.retrieval.embedder.get_cohere_client")
def test_retrieve_context_no_results(mock_get_cohere_client, mock_get_qdrant_client, mock_qdrant_client, mock_cohere_client):
    mock_qdrant_client.search.return_value = []
    mock_get_qdrant_client.return_value = mock_qdrant_client
    mock_get_cohere_client.return_value = mock_cohere_client

    query_str = "no match query"
    collection_name = "test_collection"

    result = retrieve_context(query_str, collection_name)

    assert isinstance(result, RetrievedContext)
    assert result.query == query_str
    assert len(result.chunks) == 0

@patch("src.retrieval.vector_db.get_qdrant_client")
@patch("src.retrieval.embedder.get_cohere_client")
def test_retrieve_context_cohere_error(mock_get_cohere_client, mock_get_qdrant_client, mock_qdrant_client, mock_cohere_client):
    mock_cohere_client.embed.side_effect = cohere.CohereError("Cohere API error")
    mock_get_qdrant_client.return_value = mock_qdrant_client
    mock_get_cohere_client.return_value = mock_cohere_client

    query_str = "error query"
    collection_name = "test_collection"

    result = retrieve_context(query_str, collection_name) # Should return empty context on error

    assert isinstance(result, RetrievedContext)
    assert result.query == query_str
    assert len(result.chunks) == 0
    mock_qdrant_client.search.assert_not_called() # Should not call Qdrant if embedding fails

