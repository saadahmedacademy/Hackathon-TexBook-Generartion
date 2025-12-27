from qdrant_client import QdrantClient, models as qdrant_models
from typing import List
from .config import QDRANT_URL
from .models import ContentChunk
from .chunker import generate_deterministic_id
import logging

def get_qdrant_client():
    """Initializes and returns the Qdrant client."""
    return QdrantClient(url=QDRANT_URL)

def create_collection(client: QdrantClient, collection_name: str, vector_size: int = 1024):
    """
    Creates a new collection in Qdrant if it doesn't already exist.
    Cohere's embed-english-v3.0 has a dimension of 1024.
    """
    try:
        client.get_collection(collection_name=collection_name)
        logging.info(f"Collection '{collection_name}' already exists.")
    except Exception:
        logging.info(f"Creating collection '{collection_name}'...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant_models.VectorParams(size=vector_size, distance=qdrant_models.Distance.COSINE),
        )

def upsert_vectors(client: QdrantClient, collection_name: str, chunks: List[ContentChunk], vectors: List[List[float]]):
    """
    Upserts vectors and their payloads into the specified Qdrant collection.
    """
    if not vectors:
        return

    points = []
    for i, chunk in enumerate(chunks):
        point_id = generate_deterministic_id(chunk.metadata.source_url, chunk.text)
        points.append(
            qdrant_models.PointStruct(
                id=point_id,
                vector=vectors[i],
                payload=chunk.metadata.model_dump(),
            )
        )

    # Upsert in batches
    client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )
    logging.info(f"Upserted {len(points)} vectors into '{collection_name}'.")
