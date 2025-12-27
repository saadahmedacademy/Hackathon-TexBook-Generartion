# Tasks: Retrieval and Validation Layer

This document outlines the actionable tasks to implement the retrieval and validation layer for the ROS 2 Docusaurus textbook.

## Implementation Strategy

The implementation will follow a modular, phased approach. We will first set up the project structure, define the necessary data models, and then build the core retrieval logic. Comprehensive testing will be integrated throughout the process to ensure the deterministic and robust behavior of the module.

**MVP Scope**: The MVP for this feature is the completion of all tasks defined below, resulting in a fully functional, independently testable Python module that can retrieve relevant content chunks from Qdrant given a user query.

---

## Phase 1: Project Setup

**Goal**: Initialize the project structure, dependencies, and configuration management.

- [X] T001 Create the root directory for the retrieval module at `src/retrieval/`.
- [X] T002 Update the global `requirements.txt` (or create a new one for this module) to add `qdrant-client`, `cohere`, `python-dotenv`, `pydantic`.
- [X] T003 Implement a configuration module in `src/retrieval/config.py` to load environment variables (COHERE_API_KEY, QDRANT_URL, QDRANT_COLLECTION_NAME) using `python-dotenv`.
- [X] T004 Create an `__init__.py` inside `src/retrieval/` to make it a Python package.

---

## Phase 2: Foundational Data Models and Utilities

**Goal**: Define the core data structures and utility functions.

- [X] T005 Create `src/retrieval/models.py` and define Pydantic models for `Query`, `ContentChunk`, and `RetrievedContext` based on `data-model.md`.
- [X] T006 Implement a retry decorator in `src/retrieval/retry_decorator.py` to handle transient network errors for external API calls, as detailed in `research.md`.

---

## Phase 3: User Story 1 - Deterministic Context Retrieval [US1]

**Goal**: Implement the core logic for query embedding, Qdrant search, and result filtering.
**Independent Test**: The module can be tested by providing a set of mock queries and validating the deterministic output of retrieved chunks against expected results, adhering to `top_k` and `score_threshold`.

### Test Tasks
- [X] T007 [US1] Create a test file `tests/test_retrieval.py` for the retrieval module. This test will use mock Cohere and Qdrant clients to verify:
    - Correct query embedding using `input_type="search_query"`.
    - Correct application of `top_k` and `score_threshold` filters.
    - Deterministic output for identical inputs.
    - Graceful handling of empty results.

### Implementation Tasks
- [X] T008 [P] [US1] Implement the `embedder` module in `src/retrieval/embedder.py`. This module will wrap the Cohere client, handle authentication, and expose a function to embed a single query string using the `embed-english-v3.0` model with `input_type="search_query"`. Apply the retry decorator.
- [X] T009 [P] [US1] Implement the `vector_db` module in `src/retrieval/vector_db.py`. This module will wrap the Qdrant client, handle client initialization, and expose a function to perform a similarity search (`qdrant_client.search()`) with configurable `limit`, `score_threshold`, and `with_payload=True`. Apply the retry decorator.
- [X] T010 [US1] Implement the main `retrieve_context` function in `src/retrieval/main.py`. This function will orchestrate the calls to the `embedder` and `vector_db` modules, process their results, and return a `RetrievedContext` object. It should validate the Qdrant collection's existence on startup.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Goal**: Add logging, comprehensive error handling, and documentation.

- [X] T011 [P] Add structured logging (e.g., using Python's `logging` module) to all modules to provide visibility into the retrieval process.
- [X] T012 Update `src/retrieval/main.py` (or create if not done) to include initialization logic for the Qdrant collection name and URL from `config.py`.
- [X] T013 Create a `README.md` in the `src/retrieval/` directory, documenting the module's purpose, setup, and usage, based on `quickstart.md`.

## Dependencies

- **US1** is dependent on the completion of **Phase 1** and **Phase 2**.
- `src/retrieval/main.py` (T010) is dependent on `src/retrieval/embedder.py` (T008) and `src/retrieval/vector_db.py` (T009).

## Parallel Execution

- Within **Phase 1** and **Phase 2**, tasks marked with `[P]` can be worked on concurrently.
- Within **Phase 3 [US1]**, tasks T008 and T009 can be developed in parallel as they are independent client wrappers.
