# Tasks for Feature: Fix Backend Vector Retrieval and Embedding

This document outlines the tasks required to fix the backend vector retrieval and embedding issues in the `sp-hackathon` project.

## Implementation Strategy

The fix involves two main parts: updating the Qdrant client usage to the correct API and improving the Cohere error handling to be more robust and resilient.

---

### Phase 1: Qdrant Client Fix

- [ ] T001 Review `src/retrieval/vector_db.py` to identify the `client.search()` call.
- [ ] T002 In `src/retrieval/vector_db.py`, replace the `client.search(...)` call with `client.collections.search(...)`.
- [ ] T003 In `src/retrieval/vector_db.py`, add logging within the `get_qdrant_client` function to log the client type and the availability of the `collections.search` method.
- [ ] T004 In `src/retrieval/vector_db.py`, add a startup assertion in the `get_qdrant_client` function: `assert hasattr(client.collections, "search"), "Qdrant client missing 'collections.search'"`.

---

### Phase 2: Cohere Error Handling Fix

- [ ] T005 Review `src/retrieval/embedder.py` to identify the `try-except cohere.CohereError` block.
- [ ] T006 In `src/retrieval/embedder.py`, import `TooManyRequestsError`, `CohereAPIError`, and `AuthenticationError` from `cohere.errors`.
- [ ] T007 In `src/retrieval/embedder.py`, replace the existing `try-except` block in the `embed_query` function with the new structure that catches the specific Cohere errors.

---

### Phase 3: Validation

- [ ] T008 Create or update unit tests for `src/retrieval/vector_db.py` to ensure `search_qdrant` works correctly with the new API call.
- [ ] T009 Create or update unit tests for `src/retrieval/embedder.py` to mock and verify the new exception handling for Cohere errors.
- [ ] T010 Run all backend tests to confirm that retrieval and embeddings work as expected and that errors are handled gracefully without crashing the application.
