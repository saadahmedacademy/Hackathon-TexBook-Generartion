from typing import List
from . import config
from . import embedder
from . import vector_db
from .models import RetrievedContext, ContentChunk

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CollectionNotFoundError(Exception):
    """Custom exception for when the Qdrant collection is not found."""
    pass

def retrieve_context(
    query_text: str,
    collection_name: str = config.QDRANT_COLLECTION_NAME,
    top_k: int = 5,
    score_threshold: float = 0.75
) -> RetrievedContext:
    """
    Retrieves relevant context chunks from Qdrant for a given query.
    """
    logging.info(f"Retrieving context for query: '{query_text[:50]}...'")

    qdrant_client = vector_db.get_qdrant_client()
    cohere_client = embedder.get_cohere_client()

    # Validate Qdrant collection existence
    if not vector_db.check_collection_exists(qdrant_client, collection_name):
        logging.error(f"Qdrant collection '{collection_name}' not found or inaccessible.")
        raise CollectionNotFoundError(f"Collection '{collection_name}' does not exist.")

    try:
        # Embed the query
        query_vector = embedder.embed_query(cohere_client, query_text)

        # Search Qdrant
        chunks = vector_db.search_qdrant(
            client=qdrant_client,
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
        )
        
        return RetrievedContext(query=query_text, chunks=chunks)

    except Exception as e:
        logging.error(f"An unexpected error occurred during retrieval: {e}")
        return RetrievedContext(query=query_text, chunks=[]) # Return empty context on error

