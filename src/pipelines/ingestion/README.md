# Content Ingestion Pipeline

This pipeline is responsible for crawling a deployed Docusaurus website, processing its content, and storing it as embeddings in a Qdrant vector database.

## Overview

The process is as follows:
1.  **Crawl**: Discover all pages of the target website.
2.  **Parse**: Extract the main article content from each page's HTML.
3.  **Chunk**: Break down the content into smaller, manageable chunks.
4.  **Embed**: Convert each chunk into a vector embedding.
5.  **Store**: Upload the vectors and their metadata to a Qdrant collection.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root or export the following variables:

```bash
# The full URL of the deployed Docusaurus website
VERCEL_URL="https://your-docusaurus-site.vercel.app"

# The URL for your Qdrant instance
QDRANT_URL="http://localhost:6333"

# The name for the Qdrant collection to be created
QDRANT_COLLECTION_NAME="ros2_textbook_v1"
```

## Execution

Run the pipeline from the root of the project:

```bash
python -m src.pipelines.ingestion
```

### Command-Line Arguments

You can override the environment variables using CLI arguments:

-   `--url TEXT`: The base URL of the Docusaurus site.
-   `--collection-name TEXT`: The name of the Qdrant collection.
-   `--chunk-size INTEGER`: Target size for content chunks (default: 512).
-   `--chunk-overlap INTEGER`: Token overlap between chunks (default: 50).
-   `--force-recreate`: Flag to delete and recreate the Qdrant collection if it exists.

**Example:**
```bash
python -m src.pipelines.ingestion --url "https://my-site.com" --force-recreate
```

## Validation

After the pipeline runs, you can run the validation script to sample the data in Qdrant and check its integrity.

```bash
python tests/validate_ingestion.py
```
