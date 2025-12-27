# Retrieval Module

This module provides functionality to retrieve relevant content chunks from a Qdrant vector database based on a natural language query. It utilizes Cohere embeddings for semantic search.

## Overview

The core functionality is exposed via the `retrieve_context` function, which performs the following steps:
1.  Takes a user query as input.
2.  Generates an embedding for the query using the Cohere API.
3.  Connects to a Qdrant instance.
4.  Performs a similarity search against a specified Qdrant collection.
5.  Filters results based on configurable `top_k` and `score_threshold` parameters.
6.  Returns a structured object containing the retrieved content chunks and their metadata.

## Setup

### 1. Install Dependencies
Ensure you have the necessary dependencies installed. You can add them to your `requirements.txt`:
```
qdrant-client
cohere
python-dotenv
pydantic
```
Then run:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root or export the following environment variables:

```bash
# Your Cohere API Key
COHERE_API_KEY="your_cohere_api_key"

# The URL for your Qdrant instance
QDRANT_URL="http://localhost:6333" # e.g., for local Qdrant
# or for Qdrant Cloud: QDRANT_URL="https://[YOUR_QDRANT_CLUSTER_URL]"
# QDRANT_API_KEY="your_qdrant_cloud_api_key" # If using Qdrant Cloud

# The name of the Qdrant collection to search
QDRANT_COLLECTION_NAME="ros2_textbook_v1"
```

## Usage

```python
import os
from dotenv import load_dotenv
from src.retrieval.main import retrieve_context
from src.retrieval.models import RetrievedContext

# Load environment variables if not already loaded
load_dotenv()

def run_retrieval_example():
    user_query = "What are the main components of ROS 2?"
    
    try:
        results: RetrievedContext = retrieve_context(
            query_text=user_query,
            collection_name=os.getenv("QDRANT_COLLECTION_NAME"), # Defaults from config
            top_k=5,                                             # Defaults from config
            score_threshold=0.75                                 # Defaults from config
        )

        if results.chunks:
            print(f"\n---
 Retrieved Context for Query: '{results.query}' ---")
            for i, chunk in enumerate(results.chunks):
                print(f"\nChunk {i+1} (Score: {chunk.score:.4f}):")
                print(f"  Source: {chunk.source_url}")
                print(f"  Section: {chunk.metadata.get('section_heading', 'N/A')}")
                print(f"  Content: {chunk.text[:200]}...")
        else:
            print(f"\nNo relevant content found for query: '{user_query}'")
            
    except Exception as e:
        print(f"\nAn error occurred during retrieval: {e}")

if __name__ == "__main__":
    run_retrieval_example()
```

## Testing

You can run the provided unit tests to verify the module's behavior:
```bash
pytest tests/test_retrieval.py
```
