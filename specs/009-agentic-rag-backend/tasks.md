# Tasks: Agentic RAG Backend

This document outlines the actionable tasks to implement the Agentic RAG Backend for the ROS 2 Textbook.

## Implementation Strategy

The implementation will follow a modular, phased approach, building from foundational components to the full agent functionality. We will prioritize the core grounded Q&A, then extend to code-aware reasoning and Pytest generation.

**MVP Scope**: The MVP for this feature includes all tasks necessary to achieve User Story 1 (Grounded Question Answering), along with the foundational components. User Stories 2 and 3 extend the agent's capabilities beyond the core Q&A.

---

## Phase 1: Project Setup

**Goal**: Initialize the FastAPI project structure and dependencies.

- [X] T001 Create the root directory for the backend at `src/backend/`.
- [X] T002 Create `src/backend/__init__.py` to make it a Python package.
- [X] T003 Update the global `requirements.txt` to add `fastapi`, `uvicorn`, `openai-agent-sdk`, `google-generativeai`, `python-dotenv`, `qdrant-client` (if not already there for retrieval).
- [X] T004 Create `src/backend/config.py` to load environment variables (GEMINI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_COLLECTION_NAME).
- [X] T005 Create `src/backend/main.py` as the entry point for the FastAPI application.

---

## Phase 2: Foundational Components

**Goal**: Implement core abstractions for LLM interaction and tool integration.

- [X] T006 Create `src/backend/models.py` and define Pydantic models for `ChatRequest`, `Citation`, `ChatResponse`, and `AgentToolInput` based on `data-model.md`.
- [X] T007 Implement the custom Gemini Adapter for OpenAI Agent SDK in `src/backend/llm_adapter.py`. This adapter will translate between the SDK's interface and the `google-generativeai` client.
- [X] T008 Implement the Retrieval Tool in `src/backend/tools.py`. This tool will wrap the `retrieve_context` function from `008-retrieval-validation-layer`, making it callable by the agent. It should accept a query and return structured context.
- [X] T009 Implement a `src/backend/agent_core.py` module to encapsulate agent initialization and core prompt management (system prompts, initial few-shot examples).

---

## Phase 3: User Story 1 - Grounded Question Answering [US1]

**Goal**: Implement the core RAG agent logic for grounded Q&A with citations.
**Independent Test**: Use `curl` or a Python client to query the `/chat/query` endpoint with textbook-related questions and verify responses are grounded, contain citations, and are not speculative.

### Test Tasks
- [X] T010 [US1] Create a test file `tests/test_chat_query.py`. Implement integration tests for `POST /chat/query` endpoint, verifying:
    - Successful response for valid questions.
    - Correct citation format and content.
    - Agent refusal for out-of-scope questions (mocking retrieval returning no context).

### Implementation Tasks
- [X] T011 [US1] Define the agent's initial prompt for grounded Q&A in `src/backend/prompts.py`, incorporating instructions for grounding and citation.
- [X] T012 [US1] Integrate the Retrieval Tool into the OpenAI Agent SDK configuration within `src/backend/agent_core.py`.
- [X] T013 [US1] Implement the `POST /chat/query` endpoint in `src/backend/main.py`. This endpoint will:
    - Receive `ChatRequest`.
    - Invoke the agent.
    - Process the agent's response, extracting answer and citations.
    - Format response into `ChatResponse`.
- [X] T014 [US1] Implement refusal logic within the agent and/or FastAPI endpoint to handle cases where retrieval yields no context, returning an appropriate `refusal_reason`.

---

## Phase 4: User Story 2 - Code-Aware Context Reasoning [US2]

**Goal**: Enhance the agent to reason over provided code blocks.
**Independent Test**: Query `/chat/query` with questions about provided code blocks and verify the agent's answers incorporate code context.

### Implementation Tasks
- [X] T015 [US2] Update the agent's system prompt in `src/backend/prompts.py` to instruct Gemini to reason over the provided `code_block`.
- [X] T016 [US2] Modify the `POST /chat/query` endpoint in `src/backend/main.py` to pass the `code_block` from `ChatRequest` to the agent's prompt/context.

---

## Phase 5: User Story 3 - Pytest Test Generation [US3]

**Goal**: Enable the agent to generate Pytest unit tests.
**Independent Test**: Query `/chat/query` requesting Pytest tests for given code examples and verify the generated tests are syntactically correct and relevant.

### Implementation Tasks
- [X] T017 [US3] Update the agent's system prompt in `src/backend/prompts.py` with instructions and examples for generating Pytest tests.
- [X] T018 [US3] (Optional) Implement a "code interpreter" tool for the agent in `src/backend/tools.py` if real-time code execution/validation is desired. (Skipped for hackathon scope).

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Add non-functional requirements and final documentation.

- [X] T019 Implement a `GET /health` endpoint in `src/backend/main.py`.
- [X] T020 Add structured logging to all backend modules (`src/backend/**/*.py`) to track retrieval, generation, and tool calls.
- [X] T021 Implement comprehensive error handling (e.g., Gemini API failures, rate limits) with appropriate logging and user-friendly responses.
- [X] T022 Ensure all API keys and sensitive configurations are loaded securely from environment variables.
- [X] T023 Create `src/backend/README.md` documenting setup, execution, and API usage based on `quickstart.md`.
- [X] T024 Verify OpenAPI schema generation is functional for `api.yaml`.

## Dependencies

- **Phase 2** (Foundational Components) is dependent on **Phase 1** (Project Setup).
- **Phase 3** (US1) is dependent on **Phase 2**.
- **Phase 4** (US2) is dependent on **Phase 3**.
- **Phase 5** (US3) is dependent on **Phase 3** (and potentially **Phase 4** for shared code handling).
- **Retrieval and Validation Layer** (`008-retrieval-validation-layer`) is a direct dependency for the Retrieval Tool (T008).

## Parallel Execution

- Within **Phase 1**, tasks T003-T005 can be started in parallel once T001-T002 are done.
- Within **Phase 2**, tasks T006-T009 can be developed with some parallelism, but T009 might depend on T007-T008 interfaces.
- Within **Phase 6**, tasks T019-T024 can mostly be done in parallel.
