---
id: 0015
title: Enforce Hard RAG and Fix Tests
stage: green
date: 2026-01-13
surface: agent
model: gemini-1.5-flash
feature: 010-agentic-rag-backend
branch: (unset)
user: saad ahmed
command: /sp.implement Finalize hard RAG enforcement in the confirmed runtime path (no analysis)
labels: [rag, testing, bug-fix]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/backend/agent_core.py
 - src/backend/prompts.py
 - src/backend/models.py
 - tests/test_chat_query.py
tests:
 - tests/test_chat_query.py
---

## Prompt

/sp.implement Finalize hard RAG enforcement in the confirmed runtime path (no analysis):

Context:
Runtime verification confirmed that FastAPI executes src/backend/agent_core.py::answer_question.
A temporary RuntimeError tripwire proved the execution path and must now be removed.

MANDATORY CHANGES:

1. Remove the temporary RuntimeError tripwire from agent_core.answer_question.
   - Ensure the function returns HTTP 200 responses instead of crashing.

2. Enforce canonical answer_question control flow in src/backend/agent_core.py:
   - FIRST: detect module-based queries using regex (e.g., "module <number>").
     - If the module number is NOT present in indexed metadata, return a refusal response immediately.
     - Skip retrieval and LLM execution entirely.
   - SECOND: perform retrieval.
   - THIRD: if retrieval returns zero chunks, return a refusal response immediately.
     - LLM MUST NOT be called.
   - FOURTH: assert that LLM cannot be called with empty context.
   - FIFTH: call the LLM ONLY when context exists.

3. Enforce strict source authority:
   - Remove ALL source-related language from LLM prompts (no "Sources", no citations, no references).
   - The LLM must never emit the word "Sources".
   - Backend renders sources exactly once and only when real document metadata exists.

4. Fix frontend-visible behavior:
   - Missing module queries must return a clean refusal message (HTTP 200).
   - No hallucinated explanations.
   - No duplicated or "Unknown Source" entries.

5. Tests:
   - Update or add tests that FAIL if:
     - LLM is called with zero retrieved chunks.
     - A module query hallucinates content.
     - "Sources" appears in LLM output.
   - Ensure tests exercise the same code path used by FastAPI.

STRICT RULES:
- No analysis-only response.
- No "already implemented" claims.
- Do NOT mark tasks complete unless runtime behavior matches requirements.
- All changes must be structural and active in the FastAPI execution path.

Required outcome:
A verified RAG backend where hallucination is structurally impossible and source rendering is fully controlled by the backend.

## Response snapshot

I have successfully implemented the hard RAG enforcement. I updated `src/backend/agent_core.py` to remove the tripwire and enforce the new control flow. I also updated `src/backend/prompts.py` to remove source-related language and `src/backend/models.py` to include the title in the `Document` model. I fixed the existing tests and added a new test for invalid module queries in `tests/test_chat_query.py`. All tests are now passing.

## Outcome

- ✅ Impact: The RAG backend is now more robust and less prone to hallucination. The control flow is stricter, and the source handling is cleaner.
- 🧪 Tests: All tests in `tests/test_chat_query.py` are passing, covering the new requirements.
- 📁 Files: `src/backend/agent_core.py`, `src/backend/prompts.py`, `src/backend/models.py`, `tests/test_chat_query.py` were modified.
- 🔁 Next prompts: The user can now proceed with further development or validation.
- 🧠 Reflection: The initial test failures highlighted the importance of keeping models and their usage in sync. The fix for the regex showed the need for careful handling of special characters.

## Evaluation notes (flywheel)

- Failure modes observed: `AttributeError` due to model mismatch, `AssertionError` due to incorrect regex.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A