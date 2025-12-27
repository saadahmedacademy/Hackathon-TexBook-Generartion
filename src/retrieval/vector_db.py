from qdrant_client import QdrantClient, models as qdrant_models
from typing import List
from ..retrieval.config import QDRANT_URL
from ..retrieval.retry_decorator import retry
from ..retrieval.models import ContentChunk
import logging

def get_qdrant_client():
    """Initializes and returns the Qdrant client."""
    return QdrantClient(url=QDRANT_URL)

@retry(tries=3, delay=5, backoff=2)
def search_qdrant(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    limit: int,
    score_threshold: float,
) -> List[ContentChunk]:
    """
    Performs a similarity search against the Qdrant collection.
    """
    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True,
            with_vectors=False,
        )
        
        chunks = []
        for hit in search_result:
            # Ensure payload exists and convert to ContentChunk
            if hit.payload:
                chunks.append(
                    ContentChunk(
                        doc_id=hit.payload.get("doc_id"),
                        source_url=hit.payload.get("source_url"),
                        text=hit.payload.get("original_text"), # Use original_text from ingestion
                        score=hit.score,
                        metadata=hit.payload # Keep full payload as metadata
                    )
                )
        logging.info(f"Found {len(chunks)} relevant chunks in Qdrant.")
        return chunks
    except Exception as e:
        logging.error(f"Error searching Qdrant collection '{collection_name}': {e}")
        raise e

def check_collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """Checks if a Qdrant collection exists."""
    try:
        client.get_collection(collection_name=collection_name)
        return True
    except Exception as e:
        logging.warning(f"Collection '{collection_name}' does not exist or is inaccessible: {e}")
        return False
