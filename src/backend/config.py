import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY") # Used by retrieval layer
QDRANT_URL = os.getenv("QDRANT_URL") # Used by retrieval layer
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME") # Used by retrieval layer

if not all([GEMINI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_COLLECTION_NAME]):
    raise ValueError("One or more essential environment variables are not set for the RAG backend.")
