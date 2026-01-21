import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.retrieval.vector_db import get_qdrant_client, search_qdrant
from src.retrieval.embedder import embed_query
from src.retrieval.config import QDRANT_COLLECTION_NAME

def verify_retrieval():
    """
    Connects to Qdrant, embeds a query, and retrieves context to verify the pipeline.
    """
    load_dotenv() 
    
    print("--- Verification: Retrieval Context ---")
    
    # 1. Initialize clients
    try:
        qdrant_client = get_qdrant_client()
        print("✅ Qdrant client initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize Qdrant client: {e}")
        return

    # 2. Embed a known query
    test_query = "What is ROS 2?"
    try:
        query_vector = embed_query(test_query)
        print(f"✅ Query '{test_query}' embedded successfully.")
    except Exception as e:
        print(f"❌ Failed to embed query: {e}")
        return

    # 3. Search Qdrant
    print(f"\nSearching for chunks with score threshold > 0.5...")
    try:
        retrieved_chunks = search_qdrant(
            client=qdrant_client,
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=3,
            score_threshold=0.5,
        )
        print(f"✅ Search completed. Found {len(retrieved_chunks)} chunks.")
        
        if not retrieved_chunks:
            print("⚠️ Warning: No chunks found. This may indicate an issue with ingestion or a high score threshold.")
        else:
            for i, chunk in enumerate(retrieved_chunks):
                print(f"\n--- Chunk {i+1} ---")
                print(f"  Score: {chunk.score:.4f}")
                print(f"  Doc ID: {chunk.doc_id}")
                # Print a snippet of the content to verify it's not empty/corrupt
                content_snippet = chunk.text.strip().replace('\n', ' ')[:100]
                print(f"  Content: '{content_snippet}...'")
                
                if not chunk.text.strip():
                    print(f"❌ ERROR: Chunk {chunk.doc_id} has empty content!")

    except Exception as e:
        print(f"❌ An error occurred during search: {e}")

if __name__ == "__main__":
    verify_retrieval()
