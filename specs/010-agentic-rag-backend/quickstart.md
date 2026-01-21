# Quickstart: Agentic RAG Backend

This guide provides instructions on how to set up and run the Agentic RAG Backend locally.

## Prerequisites

- Python 3.11 or later
- `pip` for package installation

## 1. Setup Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Navigate to the root of the repository
cd /path/to/your/sp-hackathon

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

## 2. Install Dependencies

Install the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
*Note: This command assumes `requirements.txt` is in the root directory and contains `fastapi`, `uvicorn`, etc.*

## 3. Run the FastAPI Server

The backend is a FastAPI application run with `uvicorn`. The entry point is `src.backend.main:app`.

```bash
# From the repository root directory
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- `--host 0.0.0.0` makes the server accessible from your local network.
- `--port 8000` runs the server on port 8000.
- `--reload` automatically restarts the server when code changes are detected.

You should see output indicating the server is running, similar to this:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 4. Test the API Endpoint

You can interact with the running API using tools like `curl` or by visiting the interactive documentation.

### Using `curl`

Open a new terminal and run the following command to send a POST request to the `/chat/query` endpoint.

```bash
curl -X POST "http://localhost:8000/chat/query" \
-H "Content-Type: application/json" \
-d 
  "question": "What is a ROS 2 node?",
  "code_block": ""
```

You should receive a JSON response from the stubbed API, for example:

```json
{
  "answer": "This is a stubbed answer about ROS 2 nodes.",
  "sources": [
    "stub:source_1"
  ],
  "status": "success"
}
```

### Using Interactive Docs (Swagger UI)

Once the server is running, open your web browser and navigate to:
[http://localhost:8000/docs](http://localhost:8000/docs)

You will see the FastAPI-generated interactive API documentation, where you can inspect the schema and send test requests directly from your browser.

```