# Implementation Plan: Cohere API Fix

**Branch**: `013-cohere-api-fix` | **Date**: 2025-12-28 | **Spec**: `specs/013-cohere-api-fix/spec.md`
**Input**: Feature specification from `/specs/013-cohere-api-fix/spec.md`

## Summary

This plan addresses critical issues in the Cohere API integration, focusing on robust error handling, rate-limit-aware retries, and performance improvements through caching. The goal is to create a production-safe embedding service that degrades gracefully and avoids application crashes.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Uvicorn, Cohere, Qdrant
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: single project
**Performance Goals**: Reduce redundant Cohere API calls, prevent cascading failures from rate limits.
**Constraints**: No modifications to Qdrant retrieval logic, no breaking API changes.
**Scale/Scope**: The fix is scoped to `src/retrieval/embedder.py` and `src/retrieval/retry_decorator.py`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- The proposed changes adhere to the principle of "Fail gracefully," as the system will no longer crash on embedding failures.
- The introduction of an LRU cache aligns with "Performance by design."
- The changes are minimal and targeted, respecting the "Smallest viable change" principle.

## Project Structure

### Documentation (this feature)

```text
specs/013-cohere-api-fix/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
```

### Source Code (repository root)
```text
src/
├── backend/
└── retrieval/
    ├── embedder.py
    └── retry_decorator.py
tests/
└── test_chat_query.py
```

**Structure Decision**: The existing single project structure is appropriate. Changes will be confined to the `retrieval` sub-package and corresponding tests.

---

## Phase 0: Research (Self-Contained in this Plan)

**1. Correct Cohere SDK Exceptions:**
   - **Decision**: Use `TooManyRequestsError` and `CohereAPIError` from `cohere.errors`.
   - **Rationale**: The existing code uses a non-existent `cohere.CohereError`. The official Cohere Python SDK documentation specifies these exception types for handling API errors, with `TooManyRequestsError` being crucial for rate-limiting.

**2. Rate-Limit-Aware Retry Logic:**
   - **Decision**: Implement a retry decorator with exponential backoff.
   - **Rationale**: A simple loop is insufficient. Exponential backoff is a standard strategy for handling rate limits, as it progressively increases the delay between retries, giving the API time to recover.

**3. Embedding Cache:**
   - **Decision**: Use `functools.lru_cache`.
   - **Rationale**: `lru_cache` is a standard, built-in Python decorator for caching function calls. It's efficient and perfectly suited for caching embedding results for identical queries, reducing API costs and latency.

---

## Phase 1: Design & Contracts

### `retry_decorator.py` Design

The `retry` decorator will be updated to:
- Accept `tries`, `delay`, and `backoff` as arguments.
- Catch `TooManyRequestsError` and other specified `CohereAPIError`s.
- In the `except` block, log a warning, wait for `delay`, and increment the delay by the backoff factor.
- If all retries fail, log a final error and return a default value (e.g., `None`).

### `embedder.py` Design

The `embed_query` function will be updated to:
- Be decorated with `@lru_cache(maxsize=128)`.
- Be decorated with the updated `@retry(...)`.
- The `try...except` block within `embed_query` will be simplified. The decorator handles retries. The function's `except` block will now only be responsible for catching the final exception from the decorator (if any) and returning `None`.

### `agent_core.py` Design

The `answer_question` method will be updated to:
- Check the return value of `embed_query`.
- If `embed_query` returns `None`, the agent should immediately return a `ChatResponse` with a `refusal_reason`, indicating a failure in the embedding service.

### Data Model & Contracts

- **`data-model.md`**: No changes are required.
- **`/contracts/`**: No changes are required.

### `quickstart.md`

A new scenario will be added to `quickstart.md` to document the graceful failure mode when the embedding service is unavailable.