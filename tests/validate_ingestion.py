import random
from qdrant_client import QdrantClient
from src.pipelines.ingestion.config import QDRANT_URL, QDRANT_COLLECTION_NAME
from src.pipelines.ingestion.models import QdrantPayload

def validate_ingestion(sample_size: int = 10):
    """
    Connects to Qdrant, fetches a random sample of vectors, and validates their payload.
    """
    print("--- Starting Ingestion Validation ---")
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        collection_info = client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        total_vectors = collection_info.vectors_count
        print(f"Found collection '{QDRANT_COLLECTION_NAME}' with {total_vectors} vectors.")

        if total_vectors == 0:
            print("Validation failed: No vectors found in the collection.")
            return

        # Qdrant doesn't have a built-in random sample, so we retrieve with an offset
        # This is a simplified sampling method.
        offset = random.randint(0, max(0, total_vectors - sample_size))
        
        print(f"Fetching {sample_size} vectors with offset {offset} for validation...")
        records, _ = client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            limit=sample_size,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        validated_count = 0
        for i, record in enumerate(records):
            print(f"\n--- Validating Record {i+1} (ID: {record.id}) ---")
            try:
                payload_data = record.payload
                QdrantPayload.model_validate(payload_data)
                print(f"  [✓] Payload for record {record.id} matches the QdrantPayload schema.")
                print(f"  Source URL: {payload_data.get('source_url')}")
                validated_count += 1
            except Exception as e:
                print(f"  [✗] Payload for record {record.id} is invalid: {e}")
                print(f"  Invalid Payload: {record.payload}")

        print("\n--- Validation Summary ---")
        if validated_count == len(records):
            print(f"[✓] Successfully validated {validated_count}/{len(records)} sampled records.")
        else:
            print(f"[✗] Validation failed. {len(records) - validated_count} out of {len(records)} records had invalid payloads.")

    except Exception as e:
        print(f"An error occurred during validation: {e}")

if __name__ == "__main__":
    validate_ingestion()
