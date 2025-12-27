# Quickstart: Retrieval and Validation Module

This guide provides a practical, executable example of how to use the retrieval module.

## Installation

The module's dependencies will be managed via `requirements.txt`.

```bash
pip install qdrant-client cohere python-dotenv pydantic
```

## Usage

The module exposes a primary function, `retrieve_context`. The following example shows how to set up the environment and call this function.

```python
import os
from dotenv import load_dotenv
from src.retrieval import retrieve_context
from src.retrieval.models import RetrievedContext

# --- Setup ---
# In a real application, this would be handled by your application's entry point.
load_dotenv()
os.environ["COHERE_API_KEY"] = "your_cohere_api_key"  # Replace with a valid key
os.environ["QDRANT_URL"] = "http://localhost:6333"   # Replace with your Qdrant URL

# --- Execution ---
def main():
    """
    Example of how to use the retrieval module.
    """
    user_query = "What is the difference between a topic and a service in ROS 2?"
    collection_name = "ros2_textbook_v1" # The collection created by the ingestion pipeline

    print(f"Executing query: '{user_query}'")

    try:
        # Call the main retrieval function
        results: RetrievedContext = retrieve_context(
            query=user_query,
            collection_name=collection_name,
            top_k=5,
            score_threshold=0.75
        )

        # --- Process Results ---
        if results.chunks:
            print(f"\nSuccessfully retrieved {len(results.chunks)} relevant chunks:")
            for i, chunk in enumerate(results.chunks):
                print(f"\n--- Chunk {i+1} (Score: {chunk.score:.4f}) ---")
                print(f"  URL: {chunk.source_url}")
                print(f"  Text: {chunk.text[:150]}...")
        else:
            print("\nNo relevant results found. The query may be out of scope.")

    except Exception as e:
        print(f"\nAn error occurred during retrieval: {e}")


if __name__ == "__main__":
    main()
```

### Expected Output

```text
Executing query: 'What is the difference between a topic and a service in ROS 2?'

Successfully retrieved 3 relevant chunks:

--- Chunk 1 (Score: 0.8951) ---
  URL: /docs/module-2-nodes-topics-services/chapter-2
  Text: While topics use a publish/subscribe model for continuous data streams, services are designed for request/reply interactions. A service has a single s...

--- Chunk 2 (Score: 0.8420) ---
  URL: /docs/module-2-nodes-topics-services/chapter-1
  Text: Topics are buses over which nodes send data. They are one-way and asynchronous. Any node can publish data to a topic, and any number of nodes can su...

--- Chunk 3 (Score: 0.8199) ---
  URL: /docs/module-2-nodes-topics-services/chapter-2
  Text: A key distinction is that services are synchronous. The client sends a request and waits for a response from the server. This is useful for comma...
```