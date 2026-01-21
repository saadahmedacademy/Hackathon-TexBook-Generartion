---
id: 0019
title: Add Conversational Guard and Disable Sources Outside RAG
stage: green
date: 2026-01-21
surface: agent
model: gemini-1.5-flash
feature: 010-agentic-rag-backend
branch: (unset)
user: saad ahmed
command: /sp.implement Add conversational query guard and disable sources outside RAG (no analysis)
labels: [rag, routing, ui-fix, correctness]
files:
  - src/backend/agent_core.py
  - tests/test_chat_query.py
tests:
  - tests/test_chat_query.py
---

## Prompt

/sp.implement Add conversational query guard and disable sources outside RAG (no analysis):

Context:
Generic queries like "hello", "how are you", "your name", and "ros 2"
are being routed into the RAG pipeline, causing improper source rendering.

This violates the system contract:
➡️ Only textbook-grounded answers may include sources
➡️ Conversational answers must NEVER include sources
➡️ Generic queries must not trigger retrieval

MANDATORY CHANGES:

1. Conversational query guard (src/backend/agent_core.py):
   - BEFORE module detection and retrieval:
     - Detect conversational / identity / generic queries, including:
       - greetings ("hi", "hello")
       - system identity ("your name", "who are you")
       - vague terms ("ros", "ros 2", "robotics")
   - For these queries:
     - Return a canned response
     - Skip retrieval
     - Skip LLM RAG synthesis
     - Return `"sources": []`

2. Hard source gating:
   - Sources MUST ONLY be attached when:
     - Retrieval succeeded
     - AND retrieval returned at least one chunk
   - Any non-RAG response MUST return an empty sources list.

3. Regression tests:
   - Add tests that FAIL if:
     - "ros 2" returns sources
     - "hello" returns sources
     - "your name" returns sources
   - Tests must pass through FastAPI execution path.

STRICT RULES:
- No sources outside RAG
- No retrieval for conversational queries
- No UI-visible "Sources:" artifacts
- HTTP 200 only

Required outcome:
A clean UX where:
- Small talk works
- Identity questions work
- Only real textbook answers show sources
- UI never renders malformed or empty source sections

## Response

The implementation plan was successfully executed. The following changes were made:

1.  **Conversational Query Guard (src/backend/agent_core.py):**
    *   Added `identity_questions` and `vague_terms` sets to `AgentCore`.
    *   Implemented checks for these new categories at the beginning of the `answer_question` method.
    *   For conversational, identity, and vague queries, a canned response is returned with `status="system"` and an empty `citations` list.
2.  **Hard Source Gating (src/backend/agent_core.py):**
    *   Ensured that all non-RAG responses (greetings, identity questions, vague terms, invalid module queries, embedding failures, uninitialized knowledge base, empty retrieval, retrieval exceptions) explicitly return `citations=[]`.
3.  **Regression Tests (tests/test_chat_query.py):**
    *   Updated `test_chat_query_greeting` to assert `response_json["citations"] == []`.
    *   Updated `test_chat_query_invalid_module`, `test_chat_query_empty_retrieval_refusal`, and `test_chat_query_retrieval_exception` to assert `response_json["citations"] == []`.
    *   Added `test_chat_query_vague_term` to verify that vague queries like "ros 2" return a system response with no citations.
    *   Added `test_chat_query_identity_question` to verify that identity questions like "who are you" return a system response with no citations.

All tests in `tests/test_chat_query.py` passed after these modifications, confirming the correct behavior of the conversational guard and source gating.
