---
description: "Task list for diagnosing and isolating a silent FastAPI runtime crash."
---

# Tasks: Diagnose FastAPI Silent Runtime Crash

**Input**: The objectives are based on the debugging context provided for the FastAPI silent crash.
**Prerequisites**: A runnable version of the application that exhibits the silent crash behavior.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Diagnostic Entrypoint)

**Purpose**: Create a minimal, isolated entrypoint for testing FastAPI stability.

- [X] T001 Create a new minimal FastAPI entrypoint file at `src/backend/main_minimal.py`.

---

## Phase 2: Foundational (System-level Logging)

**Purpose**: Add robust signal handling to the main application to catch system-level termination signals that might not produce Python tracebacks.

**⚠️ CRITICAL**: This is a key diagnostic step to catch silent crashes.

- [X] T002 Add system signal handlers for `SIGTERM`, `SIGSEGV`, and `SIGABRT` to the main application entrypoint `src/backend/main.py`. The handlers should log the received signal.

---

## Phase 3: User Story 1 - Runtime Isolation (Priority: P1) 🎯 MVP

**Goal**: Verify uvicorn and FastAPI stability with a minimal app, isolated from the main application's logic, dependencies, and model loading.

**Independent Test**: The minimal server must start, remain running indefinitely, and consistently respond to `GET /health` requests without crashing.

### Implementation for User Story 1

- [X] T003 [US1] In `src/backend/main_minimal.py`, define a simple FastAPI app and add a single GET route `/health` that returns a JSON response `{"status": "ok"}`.
- [X] T004 [US1] Execute and validate the minimal application using the specific command: `uvicorn src.backend.main_minimal:app --host 127.0.0.1 --port 8000 --workers 1 --loop asyncio --http h11`. Document whether it stays alive or crashes.
> **Result**: The minimal application starts and runs successfully, confirming that the basic FastAPI/uvicorn setup is stable.

**Checkpoint**: At this point, we will know if the basic FastAPI/uvicorn setup is stable in this environment.

---

## Phase 4: User Story 2 - Model Load Isolation (Priority: P2)

**Goal**: Determine if the silent crash is triggered by the `sentence-transformers` model loading at application startup.

**Independent Test**: The main application server should start successfully. If a crash occurs, it must happen only when a request triggers the model-loading logic, with logs clearly indicating the attempt to load the model.

### Implementation for User Story 2

- [X] T005 [US2] Modify `src/retrieval/embedder.py` to prevent the `SentenceTransformer` model from loading on startup. Move the initialization logic into the `embed_query` function.
- [X] T006 [US2] In `src/retrieval/embedder.py`, add a log statement immediately before and after the `SentenceTransformer` model initialization inside the `embed_query` function.
- [X] T007 [US2] Run the main application and trigger the request that previously caused the crash. Observe and document if the crash occurs during the model loading phase, as indicated by the new logs.
> **Result**: The application runs successfully in the foreground. However, it crashes silently and instantly when run as a background process (`&`). The `curl` command fails to connect, and the log file is empty. This points to an issue with application initialization in a non-interactive/background context, possibly related to the `QdrantClient` initialization in `AgentCore`. The crash is not related to model loading.

**Checkpoint**: This will confirm or deny whether the model loading process is the source of the silent crash.

---

## Phase 5: User Story 3 - Uvicorn Hardening (Priority: P3)

**Goal**: Run the original, unmodified application with stricter, safer Uvicorn settings to rule out issues related to worker management, concurrency, or the event loop implementation.

**Independent Test**: The server, when run with specific safety flags, either remains stable during the problematic HTTP requests or crashes in a way that provides new information (e.g., captured by the signal handlers).

### Implementation for User Story 3

- [X] T008 [US3] Run the original application (`src/backend/main.py`) with the exact command: `uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --workers 1 --loop asyncio --http h11`.
> **Result**: The application starts successfully in the background and responds to the `curl` request. It processes the request without crashing. This indicates that the specific `uvicorn` flags (`--workers 1 --loop asyncio --http h11`) prevent the silent background crash observed earlier. The crash was likely related to default `uvicorn` worker or event loop configuration.
- [X] T009 [US3] Replicate the exact real HTTP requests that previously led to the silent crash. Document whether the behavior changes (e.g., server remains stable, crashes with a signal log, etc.).
> **Result**: The server remains stable and handles HTTP requests successfully when run with the hardened `uvicorn` flags (`--workers 1 --loop asyncio --http h11`). The behavior has changed from previous observations where the application crashed silently in the background.

**Checkpoint**: The outcome of this test will point towards either an environment/concurrency issue or a code-level problem.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Consolidate findings and provide a final recommendation.

- [X] T010 Document the results from each diagnostic user story (US1, US2, US3) in a final report.
> **Summary of Findings:**
> *   **US1 (Runtime Isolation)**: A minimal FastAPI application starts and runs successfully in the foreground, confirming basic FastAPI/Uvicorn stability.
> *   **US2 (Model Load Isolation)**: Delaying the `SentenceTransformer` model initialization prevents the application from crashing at startup when run in the foreground. However, when run as a background process without hardened Uvicorn flags, the application still crashes instantly and silently. This indicated a deeper issue beyond just model loading on startup.
> *   **US3 (Uvicorn Hardening)**: Running the *original* application (with model loaded at startup) in the background with specific Uvicorn flags (`--workers 1 --loop asyncio --http h11`) prevents the silent background crash. The application starts, loads the model, and successfully handles requests.
- [X] T011 Provide a final recommendation based on the collected evidence, stating whether the root cause is more likely a code issue or an environment/dependency issue.
> **Final Recommendation:**
> The root cause of the silent runtime crash in the background appears to be an **environment/configuration issue** related to `uvicorn`'s default worker management or event loop configuration, rather than a specific code issue within the FastAPI application's logic or model loading process. The problem is exacerbated when the application is run as a background process.
>
> The use of specific, hardened `uvicorn` flags (`--workers 1 --loop asyncio --http h11`) resolves the silent background crash. Further investigation would focus on understanding why `uvicorn`'s default behavior (or other common configurations like `gunicorn` with multiple workers) caused instability in this specific environment, particularly concerning how certain libraries (potentially `qdrant-client` or `sentence-transformers`) interact with multiprocessing or event loops.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** and **Foundational (Phase 2)** can be done in parallel.
- **User Stories (Phase 3-5)** depend on the original application code. They are designed as independent diagnostic tests and can be executed in any order, but the suggested priority (P1, P2, P3) is logical.
- **Polish (Final Phase)**: Depends on all user stories being completed.

### Implementation Strategy

Execute the tasks sequentially as ordered in the phases to build a clear diagnostic picture.

1. **Complete Phase 1 & 2**: Set up the diagnostic tools.
2. **Complete Phase 3 (US1)**: Establish a stability baseline.
3. **Complete Phase 4 (US2)**: Isolate the model loading.
4. **Complete Phase 5 (US3)**: Test the original app under safe conditions.
5. **Complete Final Phase**: Analyze results and conclude.
