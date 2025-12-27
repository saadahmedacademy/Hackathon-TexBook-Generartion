import cohere
from typing import List
from .config import COHERE_API_KEY
import logging
from .retry_decorator import retry

def get_cohere_client():
    """Initializes and returns the Cohere client."""
    return cohere.Client(COHERE_API_KEY)

@retry(tries=3, delay=10, backoff=2)
def embed_chunks(client: cohere.Client, texts: List[str]) -> List[List[float]]:
    """
    Embeds a list of text chunks using the Cohere API.
    """
    if not texts:
        return []
        
    try:
        response = client.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        logging.info(f"Successfully embedded {len(texts)} chunks.")
        return response.embeddings
    except cohere.CohereError as e:
        logging.error(f"Error embedding chunks with Cohere: {e}")
        # Re-raise after logging to be caught by the retry decorator
        raise e
