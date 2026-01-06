---
description: "Task list for fixing FastAPI runtime stability issues"
---

# Tasks: 013-fastapi-runtime-fix

**Goal**: Identify and fix the root cause of FastAPI runtime failures that occur during manual HTTP requests, despite automated tests passing.

---

## Phase 1: Enhanced Logging and Deterministic Reproduction

**Purpose**: To get a clear traceback and reliably reproduce the error outside of a mocked test environment.

- [X] T001 In `src/backend/main.py`, add more detailed logging around the `agent_core` instantiation and within the `/chat/query` endpoint's `try...except` block to log the full exception before raising an HTTPException.
- [X] T002 In `src/backend/agent_core.py`, add detailed logging at the beginning and end of the `answer_question` method, before and after the `embed_query` call, and before and after the `search_qdrant` call.
- [ ] T003 Run the FastAPI server in the foreground **without** `--reload` to ensure a single, stable process for debugging. The command will be `uvicorn src.backend.main:app --host 0.0.0.0 --port 8000`.
- [ ] T004 Send a `curl` request to `http://localhost:8000/chat/query` and capture the full, verbose log output from the running Uvicorn server to identify the exact point of failure.

**Checkpoint**: At this point, we should have a complete traceback from the server that explains the HTTP 500 error.

---

## Phase 2: Analysis and Implementation of Fix

**Purpose**: Address the root cause identified in the traceback from Phase 1. The likely cause is an async-related issue with a client library not being suitable for a multi-worker environment or being used incorrectly in an async context.

- [X] T005 Analyze the traceback. If the error points to a Qdrant or SentenceTransformer client issue, investigate its compatibility with FastAPI's async event loop and Uvicorn's multi-worker model.
- [X] T006 Based on the analysis, implement a fix. A likely solution is to manage the client lifecycles with FastAPI's `lifespan` context manager. Modify `src/backend/main.py` to create and manage the `AgentCore` instance (and its clients) within a `lifespan` function. This ensures clients are initialized correctly in each worker process.
- [ ] T007 If the issue is a blocking I/O call inside an async function, wrap the blocking call with `fastapi.concurrency.run_in_threadpool` to prevent it from stalling the event loop.

**Checkpoint**: The proposed fix is implemented in the codebase.

---

## Phase 3: Verification

**Purpose**: To confirm that the fix has resolved the runtime error and the API is now stable.

- [ ] T008 Re-run the server in the foreground using `uvicorn src.backend.main:app --host 0.0.0.0 --port 8000`.
- [ ] T009 Execute the `curl` command again against `http://localhost:8000/chat/query`.
- [ ] T010 Verify that the `curl` command now returns a HTTP 200 OK status with a valid JSON response body, not an internal server error.
- [ ] T011 Check the server logs to confirm there are no new errors or tracebacks.

**Checkpoint**: The FastAPI server is stable and responds correctly to manual HTTP requests.

---

## Phase 4: Cleanup and Finalization

**Purpose**: Remove debugging artifacts and prepare the code for commit.

- [X] T012 Remove any excessive or temporary logging added during the debugging phase.
- [ ] T013 Create a commit that summarizes the fix for the FastAPI runtime instability.