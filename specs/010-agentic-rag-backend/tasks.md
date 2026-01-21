---
description: "Task list for migrating from Cohere to Sentence-Transformers embeddings"
---

# Tasks: 010-agentic-rag-backend

**Input**: User request to migrate from Cohere to local Sentence-Transformers embeddings.
**Prerequisites**: None

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add new project dependencies.

- [X] T001 Add `sentence-transformers` to `requirements.txt`

---

## Phase 2: User Story 1 - Migrate to Local Embeddings (Priority: P1) 🎯 MVP

**Goal**: Replace Cohere with `sentence-transformers` to resolve API rate limits, fix Qdrant integration, and improve performance.

**Independent Test**: After implementation, the main retrieval endpoint should return valid, semantically relevant results for a given query without making any external API calls for embeddings. Existing integration tests in `tests/test_retrieval.py` should pass.

### Implementation for User Story 1

- [X] T002 [US1] Update `src/retrieval/embedder.py` to remove all Cohere-related imports and logic. Implement a singleton `SentenceTransformer` instance with the "all-MiniLM-L6-v2" model. The `embed_query` function must be updated to use this model and return the embedding as a standard Python list.
- [X] T003 [US1] Correct the Qdrant query logic in `src/retrieval/vector_db.py`. Update the code to use the `qdrant_client.search()` method, ensuring `with_payload=True` is set and that missing payloads are handled gracefully to prevent crashes.
- [X] T004 [US1] Perform a global search across the codebase for any remaining references to "cohere", including imports, exception handling, and configuration, and remove them to ensure the migration is complete.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and validation.

- [X] T005 Review and format the modified files (`src/retrieval/embedder.py`, `src/retrieval/vector_db.py`) to ensure they adhere to project coding standards.
- [X] T006 Run all existing tests, including `tests/test_retrieval.py` and `tests/test_chat_query.py`, to confirm that the changes have not introduced any regressions.

---



## Phase 4: RAG Quality Improvement



**Purpose**: Improve the quality of the RAG system's answers.



- [X] T007 [US2] **Implement Query Preprocessor**: In `src/backend/agent_core.py`, create a function `_preprocess_query` that detects and expands module/chapter-style queries into semantically meaningful search queries.



- [X] T008 [US2] **Update Synthesis Prompt**: In `src/backend/prompts.py`, update the `SYNTHESIS_PROMPT` to enforce continuous prose, focus on explaining the topic, and format the "Sources" section as a numbered list of titles.



- [X] T009 [US2] **Implement Conversational Intent Detection**: In `src/backend/agent_core.py`, enhance the `answer_question` method to detect conversational queries (greetings, small talk) and return a friendly response without triggering the RAG pipeline.



---







## Phase 5: RAG Diagnostics and Fixes







**Purpose**: Diagnose and fix two remaining RAG issues.







- [X] T010 [US3] **Verify and Ingest Module 6 Content**: Investigate why Module 6 content is missing from the vector database. Check for missing files, excluded paths, or ingestion filters. Document findings and, if possible, ingest the Module 6 content.







- [X] T011 [US3] **Enforce Single Source-Rendering Responsibility**: Update the `SYNTHESIS_PROMPT` in `src/backend/prompts.py` to prevent the LLM from emitting the word "Sources". Modify `src/backend/agent_core.py` to ensure the "Sources" section is rendered only once and only when real source metadata exists.







---















## Phase 6: RAG Correctness Fixes















**Purpose**: Fix critical RAG correctness issues.















- [X] T012 [US4] **Enforce No-Context LLM Call Refusal**: In `src/backend/agent_core.py`, ensure that if no retrieval context is found, the LLM is not called and a clear refusal message is returned.































- [X] T013 [US4] **Remove Source-Related Language from LLM**: Update the `SYNTHESIS_PROMPT` in `src/backend/prompts.py` to remove all source-related language, ensuring the LLM never emits the word "Sources".































- [X] T014 [US4] **Guarantee Single Source Rendering**: Modify `src/backend/agent_core.py` to ensure the "Sources" section is rendered exactly once and only when real document metadata exists.































- [X] T015 [US4] **Prevent Hallucination for Module-Based Queries**: In `src/backend/agent_core.py`, if a preprocessed module-based query returns no results, ensure a refusal message is returned.















---















## Dependencies & Execution Order















### Phase Dependencies















- **Setup (Phase 1)**: Must be completed first to install the required dependency.







- **User Story 1 (Phase 2)**: Depends on Setup completion.







- **Polish (Phase 3)**: Depends on User Story 1 completion.







- **RAG Quality Improvement (Phase 4)**: Depends on Polish completion.







- **RAG Diagnostics and Fixes (Phase 5)**: Depends on RAG Quality Improvement completion.







- **RAG Correctness Fixes (Phase 6)**: Depends on RAG Diagnostics and Fixes completion.















### Within Each User Story















- Tasks are sequential as they modify related components. T002 should be completed before T003.















---















## Implementation Strategy















### Incremental Delivery















1.  Complete Phase 1: Setup







2.  Complete Phase 2: User Story 1







3.  **STOP and VALIDATE**: Test the retrieval functionality independently.







4.  Complete Phase 3: Polish







5.  Complete Phase 4: RAG Quality Improvement







6.  Complete Phase 5: RAG Diagnostics and Fixes







7.  Complete Phase 6: RAG Correctness Fixes







8.  Deploy/demo if ready.












