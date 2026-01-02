from qdrant_client import QdrantClient
from typing import List
from ..retrieval.config import QDRANT_URL, QDRANT_API_KEY
from ..retrieval.retry_decorator import retry
from ..retrieval.models import ContentChunk
import logging


def get_qdrant_client() -> QdrantClient:
    """Initializes and returns the Qdrant client."""
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        check_compatibility=False,
    )


@retry(tries=3, delay=5, backoff=2)
def search_qdrant(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    limit: int,
    score_threshold: float,
) -> List[ContentChunk]:
    """
    Searches Qdrant for similar vectors and returns matched content chunks.
    """

    try:
        # Correct API call for Qdrant v1.16.x
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
            score_threshold=score_threshold,
        )

        chunks: List[ContentChunk] = []

        for hit in search_result:
            if not hit.payload:
                continue

            chunks.append(
                ContentChunk(
                    doc_id=hit.payload.get("doc_id"),
                    source_url=hit.payload.get("source_url"),
                    text=hit.payload.get("original_text"),
                    score=hit.score,
                    metadata=hit.payload,
                )
            )

        logging.info(f"Found {len(chunks)} relevant chunks in Qdrant.")
        return chunks

    except Exception as e:
        logging.error(
            f"Error searching Qdrant collection '{collection_name}': {e}",
            exc_info=True,
        )
        raise


def check_collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """Checks if a Qdrant collection exists."""
    try:
        client.get_collection(collection_name=collection_name)
        return True
    except Exception as e:
        logging.warning(
            f"Collection '{collection_name}' does not exist or is inaccessible: {e}"
        )
        return False
