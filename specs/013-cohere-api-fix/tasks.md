# Tasks for Feature: Fix Cohere API Integration Issues

This document outlines the tasks required to fix the Cohere API integration, including incorrect exception handling, blind retry logic, and lack of caching.

## Implementation Strategy

The fix involves updating the retry decorator to be rate-limit-aware with exponential backoff, adding an LRU cache to the embedding function to reduce API calls, and improving exception handling and logging to prevent app crashes and provide clear error messages.

## Dependencies

This is a self-contained fix with no dependencies on other user stories.

---

### Phase 1: Investigation

- [ ] T001 Review `src/retrieval/embedder.py` to understand the current `embed_query` implementation.
- [ ] T002 Review `src/retrieval/retry_decorator.py` to understand the existing retry logic.

---

### Phase 2: Implementation - `retry_decorator.py`

- [ ] T003 Import `TooManyRequestsError` and `CohereAPIError` from `cohere.errors` in `src/retrieval/retry_decorator.py`.
- [ ] T004 Modify the `retry` decorator in `src/retrieval/retry_decorator.py` to specifically catch `TooManyRequestsError` and other transient `CohereAPIError`s.
- [ ] T005 Implement exponential backoff in the retry logic.
- [ ] T006 Add logging to the decorator to provide clear messages for retries and final failure.

---

### Phase 3: Implementation - `embedder.py`

- [ ] T007 Import `lru_cache` from `functools` in `src/retrieval/embedder.py`.
- [ ] T008 Apply the `@lru_cache(maxsize=128)` decorator to the `embed_query` function.
- [ ] T009 Update the `embed_query` function in `src/retrieval/embedder.py` to correctly handle exceptions and return `None` on failure instead of re-raising.
- [ ] T010 Improve logging within `embed_query` to differentiate between INFO, WARNING, and ERROR.

---

### Phase 4: Integration and Validation

- [ ] T011 Review `src/backend/agent_core.py` and ensure it gracefully handles a `None` return from `embed_query` by returning a `ChatResponse` with a `refusal_reason`.
- [ ] T012 Update `tests/test_chat_query.py` to include tests for the new embedding failure scenario. The test should mock `embed_query` to return `None` and assert that a refusal is returned.
- [ ] T013 Run all tests to ensure the fix works and no regressions were introduced.
