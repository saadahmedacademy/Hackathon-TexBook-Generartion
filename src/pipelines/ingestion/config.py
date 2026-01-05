import os
from dotenv import load_dotenv

load_dotenv()

VERCEL_URL = os.getenv("VERCEL_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not all([VERCEL_URL, QDRANT_URL, QDRANT_COLLECTION_NAME, QDRANT_API_KEY]):
    raise ValueError("One or more essential environment variables are not set.")

