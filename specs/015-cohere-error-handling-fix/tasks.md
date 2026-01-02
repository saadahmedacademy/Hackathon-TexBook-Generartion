# Tasks for Feature: Fix Cohere Embedding Error Handling

This document outlines the tasks required to fix the Cohere embedding error handling and 429 retries in the `sp-hackathon` backend.

## Implementation Strategy

The fix involves updating `src/retrieval/embedder.py` to use the correct exception classes from the Cohere SDK and implementing a more robust error handling strategy within the `embed_query` function.

---

### Phase 1: Investigation

- [ ] T001 Review `src/retrieval/embedder.py` to locate the `try-except cohere.CohereError` block and the `client.embed()` call.

---

### Phase 2: Implementation

- [ ] T002 In `src/retrieval/embedder.py`, remove the old `except cohere.CohereError` block.
- [ ] T003 In `src/retrieval/embedder.py`, add imports for `TooManyRequestsError`, `CohereAPIError`, and `AuthenticationError` from `cohere.errors`.
- [ ] T004 In `src/retrieval/embedder.py`, wrap the `client.embed()` call with the new `try-except` structure that catches the specific Cohere errors and logs them appropriately.
- [ ] T005 In `src/retrieval/embedder.py`, add a log message `logging.info(f"Embedding query: {text[:50]}...")` before the `try` block in the `embed_query` function.

---

### Phase 3: Validation

- [ ] T006 Review the implementation to ensure the `@retry` decorator is still applied to `embed_query`.
- [ ] T007 Create or update unit tests for `embedder.py` to mock and verify the new exception handling for Cohere errors.
- [ ] T008 Run the updated tests to verify the new error handling logic and ensure no regressions were introduced.
