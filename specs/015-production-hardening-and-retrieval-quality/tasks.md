---
description: "Task list for production hardening and improving retrieval quality."
---

# Tasks: 015-production-hardening-and-retrieval-quality

**Input**: The objectives are based on the feature request for production hardening.
**Prerequisites**: A stabilized FastAPI application where the silent crash is resolved.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create the necessary directory structure for the new feature.

- [X] T001 Create the directory `specs/015-production-hardening-and-retrieval-quality/`.
- [X] T002 Create empty files `constitution.md`, `specification.md`, and `plan.md` in `specs/015-production-hardening-and-retrieval-quality/`.

---

## Phase 2: Foundational (Canonical Run Command)

**Purpose**: Create a single, stable, and reliable script to run the server, preventing future runtime issues.

- [X] T003 Create a new script file at `scripts/run_server.sh`.
- [X] T004 Add the canonical `uvicorn` command to `scripts/run_server.sh`: `uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --workers 1 --loop asyncio --http h11`.
- [X] T005 Make the `scripts/run_server.sh` script executable using `chmod +x scripts/run_server.sh`.

---

## Phase 3: User Story 1 - Improve Retrieval Quality

**Goal**: Make retrieval parameters configurable and ensure graceful fallbacks.

### Implementation for User Story 1

- [X] T006 [US1] In `src/backend/config.py`, add default retrieval parameters: `DEFAULT_TOP_K = 5` and `DEFAULT_SCORE_THRESHOLD = 0.5`.
- [X] T007 [US1] In `src/backend/agent_core.py`, import `DEFAULT_TOP_K` and `DEFAULT_SCORE_THRESHOLD` from `src.backend.config` and use them in the `search_qdrant` call instead of hardcoded values.
- [X] T008 [US1] In `src/backend/agent_core.py`, verify that the existing logic correctly handles cases where `search_qdrant` returns no chunks by returning a `ChatResponse` with `status="refused"`.

---

## Phase 4: User Story 2 - Add Retrieval Logging

**Goal**: Add lightweight, informative logging to the retrieval process for better observability.

### Implementation for User Story 2

- [X] T009 [US2] In `src/backend/agent_core.py`, after the call to `search_qdrant`, add a log statement that logs the user's query, the number of chunks retrieved, and a list of the `doc_id`s from the retrieved chunks. Avoid logging full payloads.

---

## Phase 5: User Story 3 - Streaming-Ready Response

**Goal**: Prepare the API response structure for future implementation of streaming responses without enabling streaming yet.

### Implementation for User Story 3

- [X] T010 [US3] In `src/backend/models.py`, modify the `ChatResponse` model to include a new optional field: `stream_id: Optional[str] = None`.

---

## Phase N: Polish & Cross-Cutting Concerns (Documentation)

**Purpose**: Update documentation to reflect the new operational procedures and known constraints.

- [X] T011 Update `README.md` with a new section explaining how to run the server using the canonical `scripts/run_server.sh` script.
- [X] T012 In `README.md`, add a subsection under the new run instructions that explains the known constraints of the current setup, including why `uvicorn` workers must be set to 1 and potential issues when running on certain environments like WSL without the hardened flags.
