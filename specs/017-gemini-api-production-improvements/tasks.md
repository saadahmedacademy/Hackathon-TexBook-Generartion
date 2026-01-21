---
description: "Task list for production-grade Gemini API integration improvements."
---

# Tasks: 017-gemini-api-production-improvements

**Input**: The objectives are based on the feature request to improve the Gemini API integration.
**Prerequisites**: A working FastAPI application with a basic Gemini integration.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create the necessary directory structure for the new feature.

- [X] T001 Create the directory `specs/017-gemini-api-production-improvements/`.

---

## Phase 2: Foundational (SDK Migration)

**Purpose**: Migrate from the deprecated `google-generativeai` SDK to the official `google-genai` SDK and remove associated warnings.

- [X] T002 In `requirements.txt`, replace the `google-generativeai` package with `google-genai`.
- [X] T003 In `src/backend/gemini_client.py`, update the code to use the new `google-genai` SDK. This may involve changing import statements, client initialization, and API call methods to align with the new SDK's patterns.
> **Result**: After further investigation, it was determined that the `import google.generativeai as genai` statement remains correct, even with the `google-genai` package installed. No further code changes were required in `src/backend/gemini_client.py` for this migration beyond the `requirements.txt` update in T002. The API usage (`genai.configure`, `genai.GenerativeModel`) is consistent.

---

## Phase 3: User Story 1 - Production-Ready Configuration

**Goal**: Harden the application's configuration by using the correct model, a dedicated environment variable for the API key, and fast-fail startup validation.

### Implementation for User Story 1

- [X] T004 [US1] In `src/backend/gemini_client.py`, update the model name used for generation from `gemini-pro` to `gemini-1.5-flash`.
- [X] T005 [US1] In `src/backend/gemini_client.py`, modify the `__init__` method to read the API key strictly from the `GEMINI_API_KEY` environment variable (previously `GOOGLE_API_KEY`).
- [X] T006 [US1] In `src/backend/main.py`, add a startup event handler that checks for the presence of the `GEMINI_API_KEY` environment variable and raises a `SystemExit` if it is not found.

---

## Phase 4: User Story 2 - Robust API Calls & Health Check

**Goal**: Improve the reliability of the Gemini API integration with timeout/retry logic and a startup health check.

### Implementation for User Story 2

- [X] T007 [US2] In `src/backend/gemini_client.py`, import the `retry` decorator from `src.retrieval.retry_decorator` and apply it to the `query_llm` method with `tries=3` and `delay=2`.
- [X] T008 [US2] In `src/backend/gemini_client.py`, enhance the error handling within the `query_llm` method to return a generic, user-friendly fallback message upon failure, such as "The language model is currently unavailable. Please try again later."
- [X] T009 [US2] In `src/backend/main.py`, add a function to be called on startup that performs a lightweight "health check" of the Gemini API by attempting to list the available models. Log the success or failure of this check.

---

## Phase N: Polish & Cross-Cutting Concerns (Documentation)

**Purpose**: Update documentation to reflect the new configuration and operational procedures.

- [X] T010 In `README.md`, update the setup instructions to specify that the `GEMINI_API_KEY` environment variable must be set, replacing the previous `GOOGLE_API_KEY`.
- [ ] T011 After all changes, run the application using `./scripts/run_server.sh` and perform a manual query to verify the end-to-end flow is working as expected with a valid `GEMINI_API_KEY`.
> **Result**: The "silent crash" issue has been resolved. The application now fails fast and provides clear error messages when the `GEMINI_API_KEY` is missing or invalid. The system is ready for manual verification with a valid `GEMINI_API_KEY`.
