---
id: 0016
title: Normalize Qdrant Failures to Zero-Context
stage: green
date: 2026-01-13
surface: agent
model: gemini-1.5-flash
feature: 010-agentic-rag-backend
branch: (unset)
user: saad ahmed
command: /sp.implement Normalize Qdrant retrieval failures into zero-context responses (no analysis)
labels: [rag, error-handling, testing]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/backend/agent_core.py
 - tests/test_chat_query.py
tests:
 - tests/test_chat_query.py
---

## Prompt

/sp.implement Normalize Qdrant retrieval failures into zero-context responses (no analysis):

Context:
Runtime logs show that Qdrant timeouts and DNS failures raise exceptions that propagate
out of agent_core.answer_question, causing HTTP 500 errors and violating hard RAG guarantees.

MANDATORY CHANGES:

1. In src/backend/agent_core.py:
   - Wrap all retrieval calls (search_qdrant / retriever.search) in try/except.
   - On ANY exception (timeout, network, DNS, Qdrant down):
     - Log the error.
     - Treat retrieval as returning ZERO chunks.
     - Do NOT rethrow the exception.

2. Enforce RAG guarantees under infrastructure failure:
   - If retrieval fails or returns zero chunks, return a clean refusal response (HTTP 200).
   - LLM MUST NOT be called.
   - No sources must be rendered.

3. Update tests:
   - Add a test that simulates retrieval throwing an exception.
   - Test must FAIL if HTTP 500 occurs.
   - Test must PASS only if a clean refusal (HTTP 200, no sources) is returned.

STRICT RULES:
- No crashing on retrieval failure.
- No analysis-only response.
- No marking complete unless FastAPI runtime behavior matches requirements.

Required outcome:
The RAG system remains correct and non-hallucinating even when Qdrant is unavailable.

## Response snapshot

I have successfully implemented the changes to normalize Qdrant retrieval failures. I updated `src/backend/agent_core.py` to wrap the `search_qdrant` call in a `try/except` block, ensuring that any retrieval failures are gracefully handled and result in a zero-context response. I also added a new test case to `tests/test_chat_query.py` to verify this behavior. All tests are now passing.

## Outcome

- ✅ Impact: The RAG system is now more resilient to infrastructure failures. Qdrant unavailability will no longer cause the API to crash, and the system will gracefully degrade by refusing to answer questions.
- 🧪 Tests: All tests in `tests/test_chat_query.py` are passing, including the new test for retrieval exceptions.
- 📁 Files: `src/backend/agent_core.py` and `tests/test_chat_query.py` were modified.
- 🔁 Next prompts: The user can continue with further development or validation.
- 🧠 Reflection: This change improves the robustness of the system and adheres to the principle of graceful degradation. The tests provide confidence that the system will behave as expected under failure conditions.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A