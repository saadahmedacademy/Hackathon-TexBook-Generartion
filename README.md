---
title: Ros2 Rag Backend
emoji: 🐠
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Agentic RAG Backend

This project contains the backend for a RAG-powered conversational agent for the ROS 2 Textbook.

## Running the Server

To run the server, use the canonical run script:

```bash
./scripts/run_server.sh
```

**Important**: The `GEMINI_API_KEY` environment variable must be set for the application's LLM functionality to work correctly.

This script starts the FastAPI application with the recommended stable settings.

### Known Constraints

- **Uvicorn Workers**: The number of `uvicorn` workers is intentionally set to 1. Increasing the number of workers has been observed to cause silent runtime crashes in some environments. This is likely due to how certain libraries (e.g., `qdrant-client`, `sentence-transformers`) handle multiprocessing.
- **WSL (Windows Subsystem for Linux)**: When running in WSL or other non-native Linux environments, it is critical to use the hardened flags provided in the `run_server.sh` script (`--workers 1 --loop asyncio --http h11`) to ensure stability. Using default `uvicorn` settings in these environments may lead to unexpected silent crashes.
>>>>>>> c55823b (feat: Implement Gemini API integration improvements and production hardening)
