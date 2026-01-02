# Tasks: Agentic RAG Backend

**Input**: Design documents from `specs/010-agentic-rag-backend/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Phase 1: Setup

- [ ] T001 Verify project structure and dependencies are installed.

---

## Phase 2: Foundational

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [X] T002 Create `src/backend/models.py` and define `Query`, `Response`, and `Document` Pydantic models based on `data-model.md`.
- [X] T003 Create `src/backend/prompts.py` with initial prompt templates for Q&A.
- [X] T004 Create `src/backend/tools.py` for any future agent tools.
- [X] T005 Create `src/backend/config.py` for application settings.

---

## Phase 3: User Story 1 - Grounded Q&A with Citations (Priority: P1) 🎯 MVP

**Goal**: Implement the core Q&A functionality with citations.

**Independent Test**: Send a POST request to `/chat/query` with a question and verify the response contains an answer and citations.

### Implementation for User Story 1

- [X] T006 [US1] Implement the `GeminiClient` stub in `src/backend/gemini_client.py` with a `query_llm` method.
- [X] T007 [US1] Implement the `AgentCore` stub in `src/backend/agent_core.py` with an `answer_question` method that uses `GeminiClient`.
- [X] T008 [US1] Implement the `/chat/query` endpoint in `src/backend/main.py` which uses `AgentCore.answer_question`.

---

## Phase 4: User Story 2 - Code-Aware Reasoning (Priority: P2)

**Goal**: Enhance the agent to understand and reason about code blocks.

**Independent Test**: Send a POST request to `/chat/query` with a question and a `code_block`, and verify the answer is code-aware.

### Implementation for User Story 2

- [X] T009 [US2] Update the `answer_question` method in `src/backend/agent_core.py` to include the `code_block` in the prompt to the LLM.

---

## Phase 5: User Story 3 - Pytest Unit Test Generation (Priority: P3)

**Goal**: Add the capability to generate Pytest unit tests from a code block.

**Independent Test**: Send a POST request to `/chat/query` with a request for tests and a `code_block`, and verify the response contains Pytest code.

### Implementation for User Story 3

- [X] T010 [US3] Add a `generate_pytest` method to the `AgentCore` class in `src/backend/agent_core.py`.
- [X] T011 [US3] Update the `/chat/query` endpoint in `src/backend/main.py` to detect test generation requests and call `AgentCore.generate_pytest`.

---

## Phase N: Polish & Cross-Cutting Concerns

- [X] T012 Add structured logging to all modules.
- [X] T013 Implement comprehensive error handling in `main.py` and `agent_core.py`.
- [X] T014 Write docstrings for all public modules, classes, and functions.
- [X] T015 Validate the setup by running the server with `uvicorn main:app --reload` from `src/backend`.

---

## Dependencies & Execution Order

- **Foundational (Phase 2)** depends on **Setup (Phase 1)**.
- All **User Stories (Phases 3, 4, 5)** depend on **Foundational (Phase 2)**.
- User stories can be implemented sequentially or in parallel.
- **Polish (Phase N)** depends on the completion of all user stories.

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1 & 2.
2.  Complete Phase 3 (User Story 1).
3.  Validate the MVP by testing the `/chat/query` endpoint.

### Incremental Delivery

1.  Deliver the MVP.
2.  Incrementally add User Story 2 and User Story 3.
3.  Complete the Polish phase.
