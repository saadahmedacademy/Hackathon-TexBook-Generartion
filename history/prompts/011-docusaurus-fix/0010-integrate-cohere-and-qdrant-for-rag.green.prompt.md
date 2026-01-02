---
id: 0010
title: Integrate Cohere and Qdrant for RAG
stage: green
date: 2025-12-28
surface: agent
model: gemini
feature: 011-docusaurus-fix
branch: 010-agentic-rag-backend
user: {{USER}}
command: /sp.implement Wire existing Cohere + Qdrant retrieval into the agent response path and remove all stubbed logic.
labels: [backend, rag, cohere, qdrant]
links:
  spec: specs/011-docusaurus-fix/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - src/backend/agent_core.py
 - src/backend/prompts.py
 - tests/test_chat_query.py
tests:
 - pytest tests/test_chat_query.py
---

## Prompt

Wire existing Cohere + Qdrant retrieval into the agent response path and remove all stubbed logic.

Context:
- Textbook content is already embedded using Cohere
- Vectors are stored in Qdrant
- Retrieval infrastructure exists and must be reused

Required backend changes:

1) agent_core.py
   - Remove any simulated or stubbed retrieval logic
   - Call the existing Qdrant retrieval function for every non-greeting query
   - Retrieve top-k textbook chunks (configurable, default k=5)
   - If retrieval returns empty:
       → return ChatResponse with refusal_reason
       → do NOT call Gemini

2) Gemini call
   - Pass retrieved textbook chunks as explicit context
   - Instruct Gemini:
       - Answer ONLY from provided context
       - Do not use external knowledge
       - Cite every factual claim
   - Remove any hardcoded or placeholder Gemini responses

3) Response construction
   - Build answer dynamically from Gemini output
   - Generate citations from retrieved chunks:
       - source_url
       - section_heading
   - Ensure different questions produce different answers

4) Preserve existing behaviors
   - Greeting handling remains unchanged
   - Out-of-scope questions still refuse
   - Stateless per request

5) Tests
   - Update unit tests to assert:
       - No stubbed text remains
       - Retrieval is invoked
       - Different queries → different answers
       - Empty retrieval → refusal

6) Documentation
   - Update PHR explaining:
       - Transition from stubbed agent to real Cohere + Qdrant grounded RAG
       - Why this was the final activation step

## Response snapshot

Successfully integrated the Cohere and Qdrant retrieval pipeline into the agent's response path, replacing all stubbed logic. The agent now uses real retrieval for non-greeting queries, with updated prompts and tests to validate the new behavior.

## Outcome

- ✅ Impact: The agent is now a fully functional RAG agent, providing grounded answers based on the textbook content.
- 🧪 Tests: All tests passed, verifying the new RAG implementation.
- 📁 Files: 
  - `src/backend/agent_core.py` (updated to use real retrieval)
  - `src/backend/prompts.py` (updated with stricter instructions for Gemini)
  - `tests/test_chat_query.py` (updated to test the new RAG pipeline)
- 🔁 Next prompts: The user can now proceed with final validation and deployment.
- 🧠 Reflection: 
  - This was the final activation step, transitioning the agent from a series of stubs to a live RAG pipeline. This marks a significant milestone in the project, as the agent is now capable of providing real, grounded answers.
  - The process involved identifying the existing retrieval and embedding functions, wiring them into the agent core, and updating the prompts and tests accordingly. This step-by-step approach ensured a smooth transition and a fully functional RAG agent.

## Evaluation notes (flywheel)

- Failure modes observed: Initial test failures were due to incorrect mocking strategies, which were resolved by patching the `gemini_client` attribute on the `agent_core` instance directly.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
