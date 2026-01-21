# Agentic RAG Backend

This FastAPI application serves as the backend for the RAG (Retrieval-Augmented Generation) chatbot for the ROS 2 Textbook. It leverages the OpenAI Agent SDK and the Gemini API to provide grounded answers, code-aware reasoning, and Pytest test generation based on the textbook content.

## Overview

The backend exposes a REST API endpoint (`/chat/query`) that orchestrates the following:
1.  Receives a user question and an optional code block.
2.  Utilizes a custom Gemini adapter to allow the OpenAI Agent SDK to interact with the Gemini API.
3.  Invokes a Retrieval Tool (which uses the `008-retrieval-validation-layer` module) to fetch relevant context from a Qdrant vector database.
4.  Feeds the retrieved context and user query to the Gemini LLM via the agent.
5.  Generates a grounded answer, including citations, and handles refusal logic for out-of-scope or ungrounded queries.

## Setup

### 1. Prerequisites
-   Python 3.11+
-   `GEMINI_API_KEY` (for LLM calls)
-   A running Qdrant instance with an ingested textbook collection (from Feature `007-content-ingestion-pipeline`)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Ensure all dependencies like `fastapi`, `uvicorn`, `openai-agent-sdk`, `google-generativeai`, `python-dotenv`, `qdrant-client` are in `requirements.txt`)*

### 3. Configure Environment Variables
Create a `.env` file in the project root or export the following variables:

```bash
# Your Gemini API Key
GEMINI_API_KEY="your_gemini_api_key"

# The URL for your Qdrant instance (used by the Retrieval Layer)
QDRANT_URL="http://localhost:6333"

# The name of the Qdrant collection to search (used by the Retrieval Layer)
QDRANT_COLLECTION_NAME="ros2_textbook_v1"
```

## Running the Application

Navigate to the project root and start the FastAPI application:

```bash
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

## API Endpoints

### `GET /`
Welcome message.

### `GET /health`
Health check endpoint.
**Response**: `{"status": "ok"}`

### `POST /chat/query`
Query the RAG agent for answers.

**Request Body**:
```json
{
  "question": "What is a ROS 2 node?",
  "code_block": "Optional code snippet for context"
}
```

**Response Body**:
```json
{
  "answer": "...",
  "citations": [
    {
      "source_url": "...",
      "section_heading": "..."
    }
  ],
  "refusal_reason": null
}
```

## Testing

Run unit and integration tests:
```bash
pytest tests/
```
*(Ensure `pytest` is installed: `pip install pytest`)*
