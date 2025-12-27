import cohere
from typing import List
from ..retrieval.config import COHERE_API_KEY
from ..retrieval.retry_decorator import retry
import logging

def get_cohere_client():
    """Initializes and returns the Cohere client."""
    return cohere.Client(COHERE_API_KEY)

@retry(tries=3, delay=10, backoff=2)
def embed_query(client: cohere.Client, text: str) -> List[float]:
    """
    Embeds a single query string using the Cohere API.
    """
    try:
        response = client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        logging.info(f"Successfully embedded query: '{text[:50]}...'")
        return response.embeddings[0]
    except cohere.CohereError as e:
        logging.error(f"Error embedding query with Cohere: {e}")
        raise e