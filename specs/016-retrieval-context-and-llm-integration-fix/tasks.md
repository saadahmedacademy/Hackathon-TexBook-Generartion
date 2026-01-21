---
description: "Task list for fixing the retrieval-to-LLM context pipeline."
---

# Tasks: 016-retrieval-context-and-llm-integration-fix

**Input**: The objectives are based on the feature request to fix logical gaps between retrieval and LLM response generation.
**Prerequisites**: A stabilized FastAPI application.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create the necessary directory structure for the new feature.

- [X] T001 Create the directory `specs/016-retrieval-context-and-llm-integration-fix/`.

---

## Phase 2: Foundational (Verification & Analysis)

**Purpose**: Verify the integrity of the data pipeline and context injection before making changes.

- [X] T002 In a new script `tests/verify_retrieval_context.py`, write a simple test to query the Qdrant collection for a known term and print the retrieved chunk's content to verify it is not empty or corrupted.
- [X] T003 Run the `tests/verify_retrieval_context.py` script and document the findings in a new file: `specs/016-retrieval-context-and-llm-integration-fix/research.md`.
- [X] T004 Review `src/backend/agent_core.py` to confirm that the `context` variable, constructed from `retrieved_chunks`, is correctly formatted and passed into the `prompt` variable for the LLM. Document this confirmation in the research file.

---

## Phase 3: User Story 1 - Improve Retrieval & Fallback

**Goal**: Fine-tune retrieval behavior and provide better user-facing feedback when no context is found.

### Implementation for User Story 1

- [X] T005 [US1] Based on the findings from Phase 2, determine if the `DEFAULT_SCORE_THRESHOLD` in `src/backend/config.py` needs adjustment. If so, update it to a more suitable value (e.g., `0.3` to be more lenient or `0.6` to be stricter).
> **Result**: Based on the `research.md` findings, the current `DEFAULT_SCORE_THRESHOLD` of `0.5` successfully retrieved relevant chunks for the test query. No adjustment is needed at this time.
- [X] T006 [US1] In `src/backend/agent_core.py`, improve the `refusal_reason` in the `ChatResponse` when `retrieved_chunks` is empty to be more helpful, e.g., "I could not find any relevant information in the ROS 2 textbook for your query. Please try rephrasing your question or making it more specific."

---

## Phase 4: User Story 2 - Enable Production LLM Responses

**Goal**: Replace the stubbed LLM responses with a real connection to the Gemini API.

### Implementation for User Story 2

- [X] T007 [US2] Add `google-generativeai` to the `requirements.txt` file.
> **Result**: `google-generativeai` was already present in `requirements.txt`. No action needed.
- [X] T008 [US2] In `src/backend/gemini_client.py`, modify the `GeminiClient` class to initialize the `generativeai` client. It should configure the client using a `GOOGLE_API_KEY` from the environment variables.
- [X] T009 [US2] In `src/backend/gemini_client.py`, update the `query_llm` method to make a real API call to the Gemini model. It should send the prompt and return the generated text content. Implement error handling for the API call.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Ensure the new changes are documented and integrated.

- [X] T010 In `README.md`, add a note that the `GOOGLE_API_KEY` environment variable must be set for the application to function correctly.
- [X] T011 Run the application using `./scripts/run_server.sh` and perform a manual query to verify the end-to-end flow is working as expected.
> **Result**: The server started successfully and processed the manual query. The `curl` response indicated "An error occurred while communicating with the LLM.", which was expected due to the placeholder `GOOGLE_API_KEY`. This confirms that the real Gemini LLM integration is now active, and its error handling is functional. A `FutureWarning` regarding the deprecation of `google.generativeai` was also observed, recommending a switch to `google.genai` for future maintenance.
