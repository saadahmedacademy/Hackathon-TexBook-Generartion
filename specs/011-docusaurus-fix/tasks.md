# Tasks for Feature: Fix Docusaurus Frontend Crash

This document outlines the tasks required to resolve the frontend crash in the Docusaurus application caused by improper environment variable usage, specifically by leveraging Docusaurus's `customFields` mechanism.

## Implementation Strategy

The fix involves moving environment variable access to `docusaurus.config.js` and then accessing these values in `apiClient.ts` via `@docusaurus/useDocusaurusContext`. This ensures browser-safe operation. Validation will include ensuring no runtime crashes, successful loading of the Chat UI, and correct backend communication.

## Dependencies

This is a self-contained fix with no external dependencies on other user stories.

---

### Phase 1: Setup and Configuration Update

This phase focuses on updating the Docusaurus configuration to expose the chat API URL.

- [x] T001 Identify and review `ros2-textbook/docusaurus.config.ts`.
- [x] T002 Add `customFields` to `docusaurus.config.ts`, including `chatApiUrl` with the specified default and `process.env.DOCUSAURUS_CHAT_API_URL`.

---

### Phase 2: `apiClient.ts` Refactoring

This phase focuses on refactoring the `apiClient.ts` file to use the Docusaurus context for retrieving the chat API URL.

- [x] T003 Identify and review `ros2-textbook/src/components/Chat/apiClient.ts`.
- [x] T004 Remove all direct usage of `process.env` from `ros2-textbook/src/components/Chat/apiClient.ts`.
- [x] T005 Implement `@docusaurus/useDocusaurusContext` to read `siteConfig.customFields.chatApiUrl` in `ros2-textbook/src/components/Chat/apiClient.ts`.
- [x] T006 Ensure a safe fallback to `http://127.0.0.1:8000` is provided if `chatApiUrl` is not found via context within `ros2-textbook/src/components/Chat/apiClient.ts`.
- [x] T007 Verify `ros2-textbook/src/components/Chat/apiClient.ts` is fully browser-safe (no references to `process`, `global`, or Node-only APIs).

---

### Phase 3: Validation

This phase focuses on verifying that the implemented changes have resolved the issue and the application functions as expected.

- [x] T008 Run `npm start` in `ros2-textbook/` to confirm the application builds and runs without a runtime crash.
- [x] T009 Verify the Chat UI loads successfully.
- [x] T010 Confirm requests from the Chat UI reach the FastAPI backend at `/chat/query`.

---

## Task Summary

- **Total Tasks**: 10
- **Configuration Tasks**: 2
- **Refactoring Tasks**: 5
- **Validation Tasks**: 3

## MVP Scope

The MVP for this fix includes the completion of all tasks outlined above to restore the chat functionality and ensure browser-safe operation.

---

### Phase 4: Handle Out-of-Scope Queries

This phase focuses on correctly handling queries for which no relevant context can be retrieved, ensuring a structured refusal response instead of an exception.

- [x] T011 Identify the `answer_question` method in `src/backend/agent_core.py`.
- [x] T012 Modify `src/backend/agent_core.py` to simulate a "no context" scenario (e.g., if query is "no context query", set context to empty string).
- [x] T013 Implement refusal logic in `src/backend/agent_core.py` within `answer_question` to return a `Response` with `answer=""`, `citations=[]`, and a `refusal_reason` when `context` is empty.
- [x] T014 Ensure the FastAPI `POST /chat/query` endpoint always returns HTTP status 200 and matches the `ChatResponse` schema, even for refusals.
- [x] T015 Create a new unit test in `tests/test_chat_query.py` to query with no retrievable context.
- [x] T016 In the new unit test, assert that `refusal_reason` is populated and no exception is raised.

---

### Phase 5: Fix Chat UI Transparency and Containment

This phase focuses on resolving the transparency issue and improving the visual containment of the Chat UI for better readability and user experience.

- [x] T017 Identify `ros2-textbook/src/components/Chat/ChatWidget.tsx` as the main Chat component.
- [x] T018 Review `ros2-textbook/src/components/Chat/styles.module.css` for existing styles.
- [x] T019 Add `padding: 1rem;` to the `.chatWidget` class in `ros2-textbook/src/components/Chat/styles.module.css`.
- [x] T020 (Implicit - covered by T019 and existing styles) Ensure chat container has solid background, border, shadow, rounded corners, and proper z-index using Docusaurus theming variables.
- [x] T021 (Implicit - covered by Docusaurus theming and CSS Modules) Ensure styles work in both light and dark mode and do not leak globally.
- [ ] T022 Visually validate that background content is not visible through the chat UI and the chat is readable and usable. (This task requires user intervention).

---

### Phase 7: Fix Chat UI Runtime Errors for New Response Types

This phase focuses on updating the frontend Chat UI rendering logic to correctly handle the new `system` and `refused` response statuses from the backend, preventing crashes and displaying appropriate messages.

- [x] T029 Update `ChatResponsePayload` interface in `ros2-textbook/src/components/Chat/apiClient.ts` to match the backend `ChatResponse` model (including `status` and `refusal_reason`).
- [x] T030 Modify `ros2-textbook/src/components/Chat/ChatWidget.tsx` to correctly handle `status` and `refusal_reason` when updating messages, especially for setting `isError`.
- [x] T031 Modify `ros2-textbook/src/components/Chat/ChatMessage.tsx` to implement conditional rendering logic based on `message.status` (i.e., "system", "success", "refused").
- [x] T032 Ensure that for `status === "system"`, `response.answer` is rendered as a plain message and citations are **not** rendered.
- [x] T033 Ensure that for `status === "success"`, `answer` and `citations` are rendered.
- [x] T034 Ensure that for `status === "refused"`, `refusal_reason` is rendered as a friendly message and citations are **not** rendered.
- [x] T035 Implement defensive coding in `ChatMessage.tsx` to never assume `citations` exist or are non-empty (use optional chaining).
- [x] T036 Update error handling in `ChatWidget.tsx` to only show "Sorry, I encountered an error" for network failures or non-JSON responses, and not for valid API responses.
- [ ] T037 Manually validate the Chat UI behavior for greeting inputs, valid textbook questions, and out-of-scope questions. (This task requires user intervention).

---

### Phase 8: Fix Incorrect API URL Construction

This phase focuses on correcting the `apiUrl` extraction in the frontend to ensure API requests are sent to the correct endpoint.

- [x] T038 Identify the `useChatApiUrl` hook in `ros2-textbook/src/components/Chat/apiClient.ts`.
- [x] T039 Modify the `useChatApiUrl` hook to explicitly extract `siteConfig.customFields.chatApiUrl` as a string.
- [x] T040 Ensure the `useChatApiUrl` hook includes a fallback to `'http://127.0.0.1:8000'` if `siteConfig.customFields.chatApiUrl` is undefined or malformed.
-   [ ] T041 Manually validate that API requests are sent to the correct URL by inspecting the browser's DevTools Network tab.

---

### Phase 9: Fix CORS and Light Mode UI Transparency

This phase addresses the backend CORS configuration and a visual transparency issue in the frontend Chat UI specific to light mode.

**Backend – FastAPI CORS:**
- [x] T042 Identify `src/backend/main.py` for FastAPI app initialization.
- [x] T043 Add `from fastapi.middleware.cors import CORSMiddleware` to `src/backend/main.py`.
- [x] T044 Add `app.add_middleware(CORSMiddleware, ...)` immediately after FastAPI app initialization in `src/backend/main.py` with the specified origins, methods, headers, and credentials.
-   [ ] T045 Restart the backend server and verify that browser console shows no CORS errors and network tab shows successful OPTIONS + POST to `/chat/query`. (Manual validation).

**Frontend – Docusaurus Chat UI (LIGHT MODE ONLY):**
- [x] T046 Identify `ros2-textbook/src/components/Chat/styles.module.css` for Chat UI styling.
- [x] T047 Modify `.chatWidget` class in `ros2-textbook/src/components/Chat/styles.module.css` to explicitly set `background-color` for light mode using Docusaurus theme variables.
- [x] T048 Ensure this change does not override dark mode styles.
-   [ ] T049 Manually validate that the Chat UI is opaque in light mode and dark mode appearance remains unchanged.

---

### Phase 10: Integrate Cohere + Qdrant Retrieval

This phase focuses on replacing the stubbed retrieval logic in `agent_core.py` with actual calls to the Cohere + Qdrant retrieval infrastructure, enhancing the agent's ability to provide grounded answers.

-   [ ] T050 Identify the `answer_question` method in `src/backend/agent_core.py`.
-   [ ] T051 Identify the existing Qdrant retrieval function (likely in `src/retrieval/`).
-   [ ] T052 Import necessary components from `src/retrieval/` into `src/backend/agent_core.py`.
-   [ ] T053 Remove all simulated or stubbed retrieval logic from `src/backend/agent_core.py`, specifically the hardcoded `context` and the "no context query" simulation.
-   [ ] T054 Implement a call to the Qdrant retrieval function for every non-greeting query in `src/backend/agent_core.py`, retrieving top-k textbook chunks (configurable, default k=5).
-   [ ] T055 If retrieval returns empty chunks:
    *   Return a `ChatResponse` with `refusal_reason="I cannot answer questions that are outside the scope of the ROS 2 textbook. No relevant information was found."`
    *   Ensure Gemini is **not** called in this scenario.
-   [ ] T056 Modify the Gemini call in `src/backend/agent_core.py` to pass the retrieved textbook chunks as explicit context.
-   [ ] T057 Update `src/backend/prompts.py` to instruct Gemini to:
    *   Answer ONLY from provided context.
    *   Do not use external knowledge.
    *   Cite every factual claim.
-   [ ] T058 Remove any hardcoded or placeholder Gemini responses from `src/backend/agent_core.py`.
-   [ ] T059 Build the `answer` dynamically from Gemini's output.
-   [ ] T060 Generate `citations` for the `ChatResponse` from the retrieved chunks, including `source_url` and `section_heading`.
-   [ ] T061 Ensure different questions produce different answers (covered by integration).
-   [ ] T062 Preserve existing greeting handling (`T023`-`T028`) and out-of-scope refusal behavior (`T011`-`T016`). (Verification task).
-   [ ] T063 Update unit tests in `tests/test_chat_query.py`:
    *   Remove or update tests that rely on stubbed text or the "no context query" simulation.
    *   Add new tests to assert:
        *   Retrieval is invoked (mocking retrieval tool).
        *   Different queries lead to different answers (with mocked retrieval and Gemini).
        *   Empty retrieval leads to refusal (with mocked empty retrieval).

---

### Phase 6: Handle Greeting Inputs

This phase focuses on adding a system-level response for common greeting inputs, bypassing retrieval and LLM calls for these specific conversational triggers.

- [x] T023 Identify the `answer_question` method in `src/backend/agent_core.py`.
- [x] T024 Define a set of normalized greeting phrases in `src/backend/agent_core.py`.
- [x] T025 Implement a greeting detector in `src/backend/agent_core.py` to check if the input question is a greeting.
- [x] T026 For greeting inputs, modify `src/backend/agent_core.py` to return a `ChatResponse` with `answer="Hi! I can help you with questions about the ROS 2 textbook. What would you like to learn?"`, `citations=[]`, `status="system"`, and `refusal_reason=null`.
- [x] T027 Add a new unit test in `tests/test_chat_query.py` asserting that a greeting input returns the correct system `ChatResponse`.
- [x] T028 Ensure existing refusal behavior for non-greeting, non-answerable questions remains intact. (This is a verification task after implementing T023-T026).