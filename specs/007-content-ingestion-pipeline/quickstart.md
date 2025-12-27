# Quickstart: Content Ingestion Pipeline

This guide explains how to run the content ingestion and embedding pipeline.

## 1. Setup

### a. Install Dependencies
The pipeline script will require several Python libraries.

```bash
pip install "qdrant-client[fastembed]" cohere requests beautifulsoup4 markdownify langchain
```

### b. Configure Environment Variables
Create a `.env` file in the root of the project or export the following environment variables:

```bash
# The full URL of the deployed Docusaurus website
export VERCEL_URL="https://your-docusaurus-site.vercel.app"

# Your Cohere API Key
export COHERE_API_KEY="your_cohere_api_key"

# The URL for your Qdrant instance
export QDRANT_URL="http://localhost:6333"

# The name for the Qdrant collection to be created
export QDRANT_COLLECTION_NAME="ros2_textbook_v1"
```

## 2. Execution

The entire pipeline is executed via a single Python script.

```bash
python -m pipelines.ingest --url $VERCEL_URL --collection-name $QDRANT_COLLECTION_NAME
```

### Command-Line Arguments

-   `--url`: (Required) The base URL of the Docusaurus site to crawl. Overrides `VERCEL_URL` environment variable if both are present.
-   `--collection-name`: (Required) The name of the Qdrant collection to create or update. Overrides `QDRANT_COLLECTION_NAME` environment variable.
-   `--chunk-size`: (Optional) The target size for content chunks in tokens. Defaults to `512`.
-   `--chunk-overlap`: (Optional) The token overlap between adjacent chunks. Defaults to `50`.
-   `--force-recreate`: (Optional) If set, the script will delete the Qdrant collection if it already exists before starting ingestion. Use with caution.

## 3. Validation

After the script completes successfully, you can validate the results:

1.  **Check Logs**: The script will output its progress, including the number of pages found, chunks created, and vectors uploaded.
2.  **Inspect Qdrant**: Use the Qdrant web UI or the client library to inspect the created collection. Verify the `points_count` matches the number of vectors the script reported uploading. Retrieve a few random points to ensure the metadata payload is correctly populated.
