# ROS 2 Textbook Assistant (Agentic RAG System)

The ROS 2 Textbook Assistant is an AI-powered chatbot that answers questions strictly grounded in an indexed ROS 2 textbook. It uses a Retrieval-Augmented Generation (RAG) pipeline to prevent hallucinations, enforce source grounding, and provide citations for every answer.

This project was built using an AI-agent-assisted development workflow with the Gemini CLI coding agent.

## Architecture

The system is composed of a Python backend and a React/Docusaurus frontend. The backend is deployed on Hugging Face Spaces and integrated as a floating chat widget within a Docusaurus website.

### Conceptual Diagram

```
[User on Docusaurus Frontend] -> [Chat Widget (React)] -> [Gradio API on Hugging Face Spaces]
                                                                      |
                                                                      v
+-------------------------------------------------------------------------------------------------+
|                                         Backend (FastAPI/Python)                                          |
|                                                                                                 |
|  [Query] -> [AgentCore] -> [Preprocessing] -> [Embedding] -> [Qdrant Search] -> [Context] -> [LLM] -> [Response]  |
|      ^           |                                                                                |
|      |           +--------------------------------------------- [Refusal if no context] <--------+
|      |                                                                                            |
|      +------------------------------------------- [ChatResponse with Citations] ------------------+
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

## Tech Stack

| Component | Technology                                                              |
| :-------- | :---------------------------------------------------------------------- |
| **Backend**   | Python 3.10+, FastAPI, Gradio, Pydantic, Google Gemini, Qdrant, Sentence Transformers |
| **Frontend**  | TypeScript, React, Docusaurus, CSS Modules                            |
| **Deployment**| Hugging Face Spaces, Vercel (or any static host)                        |

## Features

- **Strict Grounding**: Answers are generated only from retrieved text from the ROS 2 textbook.
- **Hallucination Prevention**: The system refuses to answer if no relevant context is found.
- **Citations**: Every answer includes clickable citations to the source material.
- **Streaming-like UX**: The frontend renders responses progressively for a better user experience.
- **Contextual Questions**: Users can select text on the page to ask a question about it.
- **Agentic Core**: The backend uses an agent-style orchestrator (`AgentCore`) to manage the RAG flow.
- **Status-Aware Rendering**: The UI clearly distinguishes between successful answers, refusals, and system messages.

## Installation

### Backend

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ros2-textbook-assistant.git
    cd ros2-textbook-assistant
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Frontend

1.  **Navigate to the Docusaurus directory:**
    ```bash
    cd ros2-textbook
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Environment Variables

The backend requires the following environment variables. Create a `.env` file in the root directory:

```env
# .env

# Google Gemini API Key
GOOGLE_API_KEY="your_google_api_key"

# Qdrant Configuration
QDRANT_URL="your_qdrant_instance_url"
QDRANT_API_KEY="your_qdrant_api_key" # Optional
QDRANT_COLLECTION_NAME="ros2_textbook"

# Hugging Face Configuration
HF_TOKEN="your_hugging_face_write_token" # For deploying to Spaces
```

## Running Locally

### Backend

1.  Ensure your Qdrant instance is running and accessible.
2.  Make sure the environment variables are set.
3.  Run the Gradio application:
    ```bash
    python app.py
    ```
    The API will be available at `http://127.0.0.1:7860`.

### Frontend

1.  Navigate to the `ros2-textbook` directory.
2.  Start the Docusaurus development server:
    ```bash
    npm run start
    ```
    The website will be available at `http://localhost:3000`. The chat widget will connect to the local backend if configured correctly.

## Deployment

### Backend

The backend is designed for deployment on Hugging Face Spaces using Gradio.

1.  Create a new Space on Hugging Face.
2.  Set the required secrets (e.g., `GOOGLE_API_KEY`, `QDRANT_URL`) in the Space settings.
3.  Push your code to the Hugging Face repository. The `app.py` and `requirements.txt` files will be used to build and run the application.

### Frontend

The Docusaurus site is a static application and can be deployed to any static hosting provider like Vercel, Netlify, or GitHub Pages.

1.  **Build the site:**
    ```bash
    cd ros2-textbook
    npm run build
    ```
2.  **Deploy the `build` directory** to your chosen provider.

## API Contract

The backend exposes an API endpoint that returns a `ChatResponse` object.

**Endpoint:** `POST /api/chat` (exposed via Gradio)

**Request Body:**
```json
{
  "query": "What is a ROS 2 node?"
}
```

**Response Body (`ChatResponse`):**
```json
{
  "answer": "A ROS 2 node is a fundamental component in the ROS 2 graph that performs a specific task. It can communicate with other nodes by sending and receiving messages via topics, services, or actions.",
  "citations": [
    {
      "source_url": "/docs/module-2-nodes-topics-services/nodes",
      "section_heading": "What is a Node?"
    }
  ],
  "status": "success",
  "refusal_reason": null
}
```

- **status**: Can be `"success"`, `"refused"`, or `"system"`.
- **refusal_reason**: Provides an explanation when `status` is `"refused"`.

## Project Structure

```
.
├── app.py                  # Gradio application entrypoint
├── requirements.txt        # Backend Python dependencies
├── src/
│   └── backend/
│       ├── agent_core.py   # Core RAG orchestration logic
│       ├── llm_adapter.py    # Gemini LLM client adapter (formerly gemini_client.py)
│       ├── models.py       # Pydantic data models (e.g., ChatResponse)
│       ├── prompts.py      # System prompts for the LLM
│       └── config.py       # Application configuration
│   └── retrieval/
│       ├── embedder.py     # Sentence Transformer embedding logic
│       └── vector_db.py    # Qdrant client and search logic
├── ros2-textbook/
│   ├── docusaurus.config.ts # Docusaurus configuration
│   ├── package.json        # Frontend Node.js dependencies
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWidget.tsx # Main chat UI component
│   │   │   └── ChatMessage.tsx # Individual message rendering
│   │   ├── theme/            # Docusaurus theme overrides for the chat
│   │   └── utils/
│   │       ├── useChat.ts    # React hook for managing chat state
│   │       └── apiClient.ts  # Client for communicating with the backend API
│   └── docs/                 # The ROS 2 textbook content
└── ...
```

## Design Decisions

- **Gradio for API**: Gradio was chosen to simplify deployment on Hugging Face Spaces, as it provides both a simple UI for testing and a REST API that the frontend can consume.
- **Qdrant for Vector DB**: Qdrant offers a robust, scalable, and easy-to-use vector database solution that can be self-hosted or used as a managed service.
- **Decoupled Frontend/Backend**: This separation allows the backend API to be used by other clients and enables independent development and deployment cycles.
- **Strict Union Types on Frontend**: Using a TypeScript union for `ChatStatus` (`"success" | "refused" | "system"`) ensures type-safe handling of all possible response states in the UI.

## Safety & Grounding Guarantees

The system is designed with a strong emphasis on providing trustworthy, grounded answers.

1.  **Refusal to Answer**: If the vector search does not return any context chunks above a certain relevance threshold, the `AgentCore` will not call the LLM. Instead, it generates a "refused" response, informing the user that it cannot answer based on the available information.
2.  **Grounded Prompting**: The LLM is explicitly instructed in the system prompt to *only* use the provided context to formulate its answer and to ignore its internal knowledge.
3.  **Citation Enforcement**: The system is designed to extract source information for each piece of context used, which is then passed to the frontend and displayed to the user. This allows for direct verification of the information.

## Known Limitations

- **Fixed Knowledge Base**: The chatbot's knowledge is limited to the version of the ROS 2 textbook that was indexed. It cannot answer questions about topics outside this scope.
- **Embedding Model Dependency**: The quality of retrieval is highly dependent on the performance of the chosen sentence transformer model.
- **No Conversational Memory**: Each query is treated as an independent event. The chatbot does not remember the context of previous turns in a conversation.

## Future Improvements

- **Conversational History**: Implement a memory mechanism to allow for follow-up questions and a more natural conversational flow.
- **Advanced Retrieval**: Explore more sophisticated retrieval strategies, such as hybrid search or re-ranking, to improve context relevance.
- **Multi-Source Indexing**: Expand the knowledge base to include other relevant ROS 2 documentation or official tutorials.
- **Feedback Mechanism**: Add a feature for users to rate the quality of answers, providing valuable data for improving the system.
- **Automated Ingestion Pipeline**: Create a script to automatically process, chunk, and embed new or updated textbook content into Qdrant.

## Credits & Acknowledgements

- This project was developed with the assistance of the **Gemini CLI**, an AI-powered coding agent.
- The ROS 2 textbook content is provided by the open-source community.
- Built with powerful open-source tools including FastAPI, Gradio, Docusaurus, and Qdrant.
