# Tasks for Feature: Fix Qdrant Retrieval Crash

This document outlines the tasks required to fix the Qdrant retrieval crash caused by a deprecated client API and to improve error handling.

## Implementation Strategy

The fix involves updating the `search_qdrant` function in `src/retrieval/vector_db.py` to use the current `qdrant-client` API. Error handling will be improved to prevent exceptions from propagating and causing HTTP 500 errors, ensuring that retrieval failures result in a structured refusal response.

## Dependencies

This is a self-contained fix with no dependencies on other user stories.

---

### Phase 1: Investigation

- [ ] T001 Review `src/retrieval/vector_db.py` to confirm the `search_qdrant` function signature and its usage of `QdrantClient.search`.

---

### Phase 2: Implementation

- [ ] T002 Update the `search_qdrant` function signature in `src/retrieval/vector_db.py` to use the current `QdrantClient.search(collection_name, query_vector, limit, with_payload)` API, removing deprecated parameters.
- [ ] T003 Modify the error handling in `search_qdrant` in `src/retrieval/vector_db.py` to log the error and return an empty list `[]` instead of re-raising the exception.
- [ ] T004 Review `src/backend/agent_core.py` and update the call to `search_qdrant` to match the new function signature.
- [ ] T005 Verify that `src/backend/agent_core.py` correctly handles an empty list from `search_qdrant` by returning a `ChatResponse` with a `refusal_reason`.

---

### Phase 3: Validation

- [ ] T006 Update unit tests in `tests/test_chat_query.py` to reflect the changes in `search_qdrant`.
- [ ] T007 Add a new test case to `tests/test_chat_query.py` that mocks `search_qdrant` to throw an exception, and assert that the `POST /chat/query` endpoint returns a 200 status with a refusal.
- [ ] T008 Run all tests to ensure the fix works and no regressions were introduced.
