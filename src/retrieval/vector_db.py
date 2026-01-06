from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams, VectorParams, Distance
from typing import List
from ..retrieval.config import QDRANT_URL, QDRANT_API_KEY
from ..retrieval.retry_decorator import retry
from ..retrieval.models import ContentChunk
import logging


def get_qdrant_client() -> QdrantClient:
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

    try:
        result = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
            score_threshold=score_threshold,
            search_params=SearchParams(exact=False),
        )

        chunks: List[ContentChunk] = []

        for point in result.points:
            payload = point.payload
            if not payload:
                continue

            doc_id = payload.get("doc_id")
            if not doc_id:
                doc_id = str(point.id)
                logging.warning(f"Missing 'doc_id' in payload for point {point.id}. Falling back to point ID.")

            chunks.append(
                ContentChunk(
                    doc_id=doc_id,
                    source_url=payload.get("source_url", ""),
                    text=payload.get("original_text", ""),
                    score=point.score,
                    metadata=payload,
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
    try:
        client.get_collection(collection_name=collection_name)
        return True
    except Exception as e:
        logging.warning(
            f"Collection '{collection_name}' does not exist or is inaccessible: {e}"
        )
        return False

def recreate_collection(client: QdrantClient, collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
    """
    Deletes a collection if it exists and creates it with the specified configuration.
    """
    try:
        if check_collection_exists(client, collection_name):
            logging.info(f"Deleting existing collection '{collection_name}'...")
            client.delete_collection(collection_name=collection_name)
            logging.info(f"Collection '{collection_name}' deleted.")

        logging.info(f"Creating collection '{collection_name}' with vector size {vector_size}...")
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )
        logging.info(f"Collection '{collection_name}' created successfully.")
        return True
    except Exception as e:
        logging.error(f"Error recreating Qdrant collection '{collection_name}': {e}", exc_info=True)
        return False
