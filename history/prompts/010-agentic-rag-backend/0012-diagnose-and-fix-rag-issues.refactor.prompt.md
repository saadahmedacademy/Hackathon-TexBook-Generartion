---
id: 0012
title: Diagnose and Fix RAG Issues
stage: refactor
date: 2026-01-11
surface: agent
model: gemini-pro
feature: 010-agentic-rag-backend
branch: 010-agentic-rag-backend
user: saadahmed
command: /sp.implement Diagnose and fix two remaining RAG issues...
labels: ["rag", "debugging", "ingestion", "prompt-engineering"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/010-agentic-rag-backend/tasks.md
  - src/pipelines/ingestion/html_parser.py
  - src/backend/prompts.py
  - src/backend/agent_core.py
  - tests/verify_module6.py
tests:
  - tests/verify_module6.py
---

## Prompt

/sp.implement Diagnose and fix two remaining RAG issues:

Verify whether ROS 2 Module 6 ("Vision, Language, and Action") content is present in the vector database. If missing, identify why it was not ingested (missing files, excluded paths, or ingestion filters). Document findings and, if possible, ingest the Module 6 content so it becomes retrievable.

Eliminate duplicate or malformed "Sources" output by enforcing a single source-rendering responsibility. Ensure that:

The LLM never emits the word "Sources" in fallback or refusal responses.

The backend/UI renders the "Sources" section exactly once and only when real source metadata exists.

Update tasks.md with these fixes and implement them.

## Response snapshot

I have diagnosed and fixed the two remaining RAG issues.

1.  **Missing Module 6 Content:** I discovered that the content for Module 6 was not being ingested because the HTML parser was looking for an `<article>` tag, which was not present on the Module 6 pages. I updated the parser to look for a `<main>` tag instead and re-ingested the content. I also created a verification script `tests/verify_module6.py` to confirm the fix.

2.  **Duplicate or Malformed "Sources" Output:** I updated the `SYNTHESIS_PROMPT` in `src/backend/prompts.py` to explicitly forbid the LLM from emitting the word "Sources". I also updated `src/backend/agent_core.py` to ensure the "Sources" section is rendered only once and only when real source metadata exists.

I have also updated the `tasks.md` file to reflect these changes.

## Outcome

- ✅ Impact: High. These changes fix critical bugs in the RAG system, improving content coverage and response formatting.
- 🧪 Tests: I created a verification script `tests/verify_module6.py` to confirm that the Module 6 content is now being ingested correctly.
- 📁 Files: 
  - `specs/010-agentic-rag-backend/tasks.md`
  - `src/pipelines/ingestion/html_parser.py`
  - `src/backend/prompts.py`
  - `src/backend/agent_core.py`
  - `tests/verify_module6.py`
- 🔁 Next prompts: The user can now test the improved RAG system.
- 🧠 Reflection: The debugging process was effective in identifying the root cause of the missing content. The fix was straightforward once the problem was identified. The changes to the prompt and the agent core will make the output more robust and reliable.

## Evaluation notes (flywheel)

- Failure modes observed: The initial assumption that Module 6 content was missing was correct, but the root cause was not immediately obvious. The verification script was crucial in confirming the fix.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the RAG system with a wider range of queries to ensure the fixes have not introduced any regressions.
