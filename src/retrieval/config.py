import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")


if not all([QDRANT_URL, QDRANT_COLLECTION_NAME, QDRANT_API_KEY]):
    raise ValueError("One or more essential environment variables are not set for retrieval module.")
