import pytest
from unittest.mock import MagicMock, patch
from src.retrieval.models import RetrievedContext, ContentChunk
from src.retrieval.main import retrieve_context
from qdrant_client.http.models import ScoredPoint, QueryResponse

# Mock Qdrant client
@pytest.fixture
def mock_qdrant_client():
    return MagicMock()

# Test cases
@patch("src.retrieval.main.vector_db.check_collection_exists")
@patch("src.retrieval.main.vector_db.search_qdrant")
@patch("src.retrieval.embedder.embed_query")
def test_retrieve_context_success(mock_embed_query, mock_search_qdrant, mock_check_collection, mock_qdrant_client):
    mock_check_collection.return_value = True
    mock_embed_query.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.return_value = [
        ContentChunk(
            doc_id="doc1",
            source_url="url1",
            text="original_text1",
            score=0.9,
            metadata={}
        ),
        ContentChunk(
            doc_id="doc2",
            source_url="url2",
            text="original_text2",
            score=0.8,
            metadata={}
        ),
    ]

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

    mock_embed_query.assert_called_once_with(query_str)
    mock_search_qdrant.assert_called_once()
    args, kwargs = mock_search_qdrant.call_args
    assert kwargs["collection_name"] == collection_name
    assert kwargs["query_vector"] == [0.1, 0.2, 0.3]
    assert kwargs["limit"] == top_k
    assert kwargs["score_threshold"] == score_threshold

@patch("src.retrieval.main.vector_db.check_collection_exists")
@patch("src.retrieval.main.vector_db.search_qdrant")
@patch("src.retrieval.embedder.embed_query")
def test_retrieve_context_no_results(mock_embed_query, mock_search_qdrant, mock_check_collection, mock_qdrant_client):
    mock_check_collection.return_value = True
    mock_search_qdrant.return_value = []
    mock_embed_query.return_value = [0.1, 0.2, 0.3]

    query_str = "no match query"
    collection_name = "test_collection"

    result = retrieve_context(query_str, collection_name)

    assert isinstance(result, RetrievedContext)
    assert result.query == query_str
    assert len(result.chunks) == 0

@patch("src.retrieval.main.vector_db.check_collection_exists")
@patch("src.retrieval.main.vector_db.search_qdrant")
@patch("src.retrieval.embedder.embed_query")
def test_retrieve_context_embedding_error(mock_embed_query, mock_search_qdrant, mock_check_collection, mock_qdrant_client):
    mock_check_collection.return_value = True
    mock_embed_query.side_effect = Exception("Embedding error")

    query_str = "error query"
    collection_name = "test_collection"

    result = retrieve_context(query_str, collection_name) # Should return empty context on error

    assert isinstance(result, RetrievedContext)
    assert result.query == query_str
    assert len(result.chunks) == 0
    mock_search_qdrant.assert_not_called() # Should not call Qdrant if embedding fails