---
id: 0018
title: Enforce Source-Free Answer Text and Backend-Only Rendering
stage: green
date: 2026-01-21
surface: agent
model: gemini-1.5-flash
feature: 010-agentic-rag-backend
branch: (unset)
user: saad ahmed
command: /sp.implement Enforce source-free answer text and backend-only source rendering (no analysis)
labels: [rag, ui-contract, hallucination-prevention]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/backend/agent_core.py
 - src/backend/prompts.py
 - tests/test_chat_query.py
tests:
 - tests/test_chat_query.py
---

## Prompt

/sp.implement Enforce source-free answer text and backend-only source rendering (no analysis):Context:Even after refusal hardening, successful answers (e.g. "ROS 2 introduction")still display a "Sources:" section in the UI. This indicates that either:- the LLM is emitting source-like text, or- the backend is merging sources into the answer payload incorrectly.This violates the hard RAG invariant:➡️ Answer text must NEVER contain or reference sources.➡️ Sources must be rendered ONLY as structured metadata.MANDATORY CHANGES:1. Absolute answer purity (src/backend/agent_core.py):   - Strip the final answer text of ANY source-related tokens:     ("Sources", "Source:", "References", "Citations").   - Answer text must be plain instructional prose only.   - If such tokens are detected, remove the entire trailing section.2. Backend-only source rendering:   - Sources must be attached ONLY as structured metadata:     `"sources": [{ "title": ..., "url": ... }]`   - The answer string must never include source labels or lists.3. Prompt hardening (src/backend/prompts.py):   - Explicitly instruct the LLM:     - “Do not mention sources, citations, references, or documents.”     - “Do not include any footer or attribution.”   - Remove any remaining wording that could cause attribution behavior.4. UI contract via tests:   - Add a test that FAILS if:     - The answer text contains the word "Sources".     - A colon-formatted source block appears in the answer.   - Test must cover:     - Successful retrieval (e.g., "ROS 2 introduction")     - Refusal pathsSTRICT RULES:- No answer text may contain "Sources" under any condition.- No duplicated rendering (text + metadata).- No frontend inference.- No HTTP 500s.Required outcome:A clean separation where:- Answer = pure educational content- Sources = optional structured metadata- UI can never display a malformed or duplicate Sources section ,

## Response snapshot

I have successfully enforced source-free answer text and backend-only source rendering. I have modified `src/backend/prompts.py` to remove source-related language from the `SYNTHESIS_PROMPT`, modified `src/backend/agent_core.py` to strip source-related tokens from the answer and ensure sources are only rendered as structured metadata, and added a test to `tests/test_chat_query.py` to verify that the answer text does not contain "Sources" and that sources are rendered correctly as structured metadata. All tests passed, so no regressions were introduced.

## Outcome

- ✅ Impact: The RAG system now correctly separates answer content from source metadata, preventing hallucinated or malformed source information in the UI.
- 🧪 Tests: Added a new test to verify the stripping of source-related keywords from the LLM's response. All 9 tests passed.
- 📁 Files: Modified `src/backend/prompts.py`, `src/backend/agent_core.py`, and `tests/test_chat_query.py`.
- 🔁 Next prompts: None
- 🧠 Reflection: The changes were straightforward and addressed the user's request. The addition of a specific test case for source stripping will help prevent future regressions.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
