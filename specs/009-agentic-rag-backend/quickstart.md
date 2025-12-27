# Quickstart: Agentic RAG Backend

This guide demonstrates how to set up, run, and interact with the Agentic RAG Backend.

## 1. Setup

### a. Prerequisites
-   Python 3.11+
-   `COHERE_API_KEY` (for retrieval embeddings)
-   `GEMINI_API_KEY` (for LLM calls)
-   A running Qdrant instance with an ingested textbook collection (from Feature `007-content-ingestion-pipeline`)

### b. Install Dependencies

```bash
pip install "fastapi[all]" openai-agent-sdk google-generativeai qdrant-client cohere python-dotenv uvicorn
```
*(Note: `openai-agent-sdk` is a placeholder. The actual package name might vary or a custom adapter will be used.)*

### c. Configure Environment Variables
Create a `.env` file in the project root or export the following environment variables:

```bash
# Your Gemini API Key
export GEMINI_API_KEY="your_gemini_api_key"

# Your Cohere API Key (used by the Retrieval Layer)
export COHERE_API_KEY="your_cohere_api_key"

# The URL for your Qdrant instance (used by the Retrieval Layer)
export QDRANT_URL="http://localhost:6333"

# The name of the Qdrant collection to search (used by the Retrieval Layer)
export QDRANT_COLLECTION_NAME="ros2_textbook_v1"
```

## 2. Run the FastAPI Application

Navigate to the root of the project and run the FastAPI application:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*(Note: The actual entry point file, e.g., `main.py`, will be created during implementation.)*

The API documentation will be available at `http://localhost:8000/docs`.

## 3. Interact with the API

### a. Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{"status": "ok"}
```

### b. Query the Agent (Grounded Q&A)

```bash
curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d 
     {
           "question": "What are the core components of ROS 2?"
         }
```

**Expected Response (example)**:
```json
{
  "answer": "The core components of ROS 2 include nodes, topics, services, actions, and parameters. Nodes are processes that perform computation...",
  "citations": [
    {
      "source_url": "/docs/module-1-ros-foundations/chapter-1",
      "section_heading": "ROS 2 Core Concepts"
    }
  ],
  "refusal_reason": null
}
```

### c. Query the Agent (Code-Aware Reasoning)

```bash
curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d 
     {
           "question": "Explain this Python code for a ROS 2 publisher.",
           "code_block": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalPublisher(Node):\n    def __init__(self):\n        super().__init__(\'minimal_publisher\')\n        self.publisher_ = self.create_publisher(String, \'topic\', 10)\n        timer_period = 0.5\n        self.timer = self.create_timer(timer_period, self.timer_callback)\n        self.i = 0\n    def timer_callback(self):\n        msg = String()\n        msg.data = \'Hello World: %d\' % self.i\n        self.publisher_.publish(msg)\n        self.get_logger().info(\'Publishing: \"%s\"\' % msg.data)\n        self.i += 1"
         }
```

### d. Query the Agent (Out-of-Scope Refusal)

```bash
curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d 
     {
           "question": "What is the capital of France?"
         }
```

**Expected Response (example)**:
```json
{
  "answer": "I cannot answer your question based on the available textbook content.",
  "citations": [],
  "refusal_reason": "Query out of scope: The question is not related to ROS 2 or humanoid robotics."
}
```
