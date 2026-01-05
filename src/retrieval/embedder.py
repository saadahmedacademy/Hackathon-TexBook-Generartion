from sentence_transformers import SentenceTransformer
from typing import List
import logging

# Initialize the SentenceTransformer model as a singleton instance.
# This ensures the model is loaded only once when the module is imported.
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logging.info("SentenceTransformer model 'all-MiniLM-L6-v2' loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load SentenceTransformer model: {e}")
    model = None

def embed_query(text: str) -> List[float]:
    """
    Embeds a single query string using the local SentenceTransformer model.

    Args:
        text: The input string to embed.

    Returns:
        A list of floats representing the embedding.
        Returns an empty list if the model is not loaded.
    """
    if not model:
        logging.error("SentenceTransformer model is not available. Cannot embed query.")
        return []

    try:
        # The model.encode() method returns a numpy array, which we convert to a list.
        embedding = model.encode(text, convert_to_tensor=False).tolist()
        logging.info(f"Successfully embedded query: '{text[:50]}...'")
        return embedding
    except Exception as e:
        logging.error(f"Error embedding query with SentenceTransformer: {e}")
        # Depending on the desired error handling, you might want to raise the exception
        # or return an empty list to indicate failure.
        return []

# Example of how to use the embedder:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_query = "What is the capital of France?"
    embedding_vector = embed_query(sample_query)

    if embedding_vector:
        print(f"Query: {sample_query}")
        print(f"Embedding dimension: {len(embedding_vector)}")
        # print(f"Embedding vector (first 5 dimensions): {embedding_vector[:5]}")
    else:
        print("Failed to generate embedding.")
