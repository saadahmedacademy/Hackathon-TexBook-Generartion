from src.retrieval.vector_db import get_qdrant_client, search_qdrant
from src.retrieval.embedder import embed_query
from src.retrieval.config import QDRANT_COLLECTION_NAME

def main():
    """
    Searches the Qdrant database for content related to Module 6 and prints the results.
    """
    client = get_qdrant_client()
    query = "Vision, Language, and Action"
    query_vector = embed_query(query)

    print(f"Searching for '{query}' in collection '{QDRANT_COLLECTION_NAME}'...")

    results = search_qdrant(
        client=client,
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=10,
        score_threshold=0.5,
    )

    if not results:
        print("No results found for Module 6 content.")
        return

    print(f"Found {len(results)} results:")
    for result in results:
        print(f"  - Source: {result.metadata.get('source_url', 'N/A')}")
        print(f"    Score: {result.score}")
        print(f"    Text: {result.text[:100]}...")

if __name__ == "__main__":
    main()
