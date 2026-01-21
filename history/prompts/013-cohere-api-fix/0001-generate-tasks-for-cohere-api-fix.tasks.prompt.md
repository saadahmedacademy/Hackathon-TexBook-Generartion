---
id: 0001
title: Generate Tasks for Cohere API Fix
stage: tasks
date: 2025-12-28
surface: agent
model: gemini
feature: 013-cohere-api-fix
branch: 010-agentic-rag-backend
user: {{USER}}
command: /sp.tasks You are a senior Python backend engineer and RAG systems expert...
labels: [backend, cohere, bugfix, tasks]
links:
  spec: specs/013-cohere-api-fix/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/013-cohere-api-fix/tasks.md
tests:
  null
---

## Prompt

You are a senior Python backend engineer and RAG systems expert. Context: - Project: sp-hackathon - Stack: FastAPI, Uvicorn, Qdrant (qdrant-client 1.16.x), Cohere embeddings - Environment: Ubuntu (WSL), Python 3.11, virtualenv - Architecture: AI-driven RAG using SpecKit / SpecKit-Plus workflow - Current phase: Debugging & integration fixes Known working parts: - Qdrant retrieval is FIXED and MUST use: client.search(collection_name, query_vector, limit, with_payload=True, score_threshold) - Do NOT use search_points, query_points, SearchRequest, Vector models - Backend starts cleanly with uvicorn - Cohere API key is valid Current problems to fix (ALL REQUIRED): 1. Cohere 429 TooManyRequests errors are crashing the app 2. Code incorrectly catches `cohere.CohereError` (this class does NOT exist) 3. Retry logic retries blindly and causes cascading failures 4. No embedding cache exists, causing excessive API calls 5. Error handling is not production-safe 6. Need clean logs instead of stack-trace explosions 7. App should degrade gracefully if embeddings fail Your tasks (DO ALL): - Replace invalid `except cohere.CohereError` with correct Cohere SDK exceptions - Use `TooManyRequestsError` and `CohereAPIError` from `cohere.errors` - Implement rate-limit-aware retry logic with exponential backoff - Add an LRU cache for embeddings to reduce API calls - Ensure retries stop after max attempts with a clear error message - Prevent FastAPI from crashing on embedding failures - Improve logging (INFO, WARNING, ERROR separation) - Do NOT modify Qdrant retrieval logic (it is already correct) - Do NOT introduce breaking API changes Constraints: - Follow clean Python architecture - Keep code compatible with Cohere Python SDK (latest) - No deprecated APIs - No speculative code - No placeholder implementations Deliverables: - Corrected `embedder.py` - Corrected retry decorator - Any minimal supporting changes required - Brief explanation of WHY each fix is necessary Output format: - Provide only the final corrected code blocks - Use clear file names as headers - Keep explanations concise and technical Fix everything in one pass.

## Response snapshot

Generated `tasks.md` for fixing the Cohere API integration issues.

## Outcome

- ✅ Impact: Created a new tasks.md file for a bug fix.
- 🧪 Tests: None
- 📁 Files: specs/013-cohere-api-fix/tasks.md
- 🔁 Next prompts: The user can now proceed with implementing the tasks.
- 🧠 Reflection: The request was clear and specific, allowing for straightforward task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
