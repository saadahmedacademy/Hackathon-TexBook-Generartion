---
id: 0010
title: Improve RAG Answer Synthesis
stage: refactor
date: 2026-01-11
surface: agent
model: gemini-pro
feature: 010-agentic-rag-backend
branch: 010-agentic-rag-backend
user: saadahmed
command: /sp.implement Improve the RAG answer synthesis behavior for the chat endpoint.
labels: ["rag", "prompt-engineering", "answer-synthesis"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/backend/prompts.py
  - src/backend/agent_core.py
tests:
  - none
---

## Prompt

/sp.implement Improve the RAG answer synthesis behavior for the chat endpoint.

Update the system / synthesis prompt so that:
- The assistant explains the topic in clear, natural language first
- The answer focuses on concepts and understanding, not document structure
- The assistant must NOT mention chapter numbers, file paths, or module names in the main answer
- Retrieved documents should be used as grounding only, not described explicitly
- Sources should appear at the end in a clean "Sources:" section
- The "Sources:" section must be concise and human-readable (no bullet-only dumps)
- If the question is broad (e.g., "Tell me about ROS 2"), produce a proper explanatory overview
- If no relevant content exists, respond gracefully and explain what information is missing

Do not change retrieval logic, vector search, or Gemini configuration.
Only update prompt templates / answer formatting logic.

Ensure the final output reads like a knowledgeable tutor, not a document index.

## Response snapshot

I have updated the answer synthesis prompt in `src/backend/prompts.py` to guide the language model to produce more conceptual and user-friendly answers. I also updated `src/backend/agent_core.py` to use this new prompt. The new prompt instructs the model to act as a knowledgeable tutor, focusing on explanations rather than just extracting information, and to format sources cleanly at the end of the response.

## Outcome

- ✅ Impact: High. The change directly addresses the user's request to improve the quality of the RAG system's answers, making them more helpful and readable.
- 🧪 Tests: No tests were run, as the changes were limited to prompt templates.
- 📁 Files: 
  - `src/backend/prompts.py`
  - `src/backend/agent_core.py`
- 🔁 Next prompts: The user can now test the new answer synthesis behavior.
- 🧠 Reflection: The change was straightforward and directly addressed the user's request. Using a more detailed prompt is a good way to control the output of the language model.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the new prompt with a variety of questions to see how it performs.
