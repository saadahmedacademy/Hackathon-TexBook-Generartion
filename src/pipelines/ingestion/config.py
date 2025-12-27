import os
from dotenv import load_dotenv

load_dotenv()

VERCEL_URL = os.getenv("VERCEL_URL")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

if not all([VERCEL_URL, COHERE_API_KEY, QDRANT_URL, QDRANT_COLLECTION_NAME]):
    raise ValueError("One or more essential environment variables are not set.")

