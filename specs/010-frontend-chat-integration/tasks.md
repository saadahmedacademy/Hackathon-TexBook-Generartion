# Tasks: Frontend Chat Integration

This document outlines the actionable tasks to implement the chat widget for the ROS 2 Docusaurus textbook.

## Implementation Strategy

The implementation will be modular, centered around a `ChatWidget` component. We will use Docusaurus's "swizzling" feature to globally inject a `ChatButton` and a portal for the `ChatWidget` modal. The widget's functionality will be built in phases, starting with the basic UI, then integrating state management and API calls, and finally adding advanced features like contextual text selection and citation highlighting.

**MVP Scope**: The MVP for this feature is the completion of all tasks for User Story 1, resulting in a functional chat widget that can answer general questions with clickable citations.

---

## Phase 1: Project Setup & Component Scaffolding

**Goal**: Create the necessary files and folder structure for the chat components.

- [X] T001 Create a new directory for the chat components at `ros2-textbook/src/components/Chat/`.
- [X] T002 Create the following empty files inside the new directory: `ChatWidget.tsx`, `ChatButton.tsx`, `ChatMessage.tsx`, `useChat.ts` (for state management hook), `apiClient.ts`, and `styles.module.css`.
- [X] T003 Create a `.env.local` file in the `ros2-textbook/` directory with `REACT_APP_CHAT_API_URL=http://localhost:8000` to configure the backend URL.

---

## Phase 2: Foundational UI Components

**Goal**: Build the static UI components for the chat widget.

- [X] T004 [P] Implement the `ChatButton` component in `ros2-textbook/src/components/Chat/ChatButton.tsx`. It should render a floating button and accept an `onClick` prop.
- [X] T005 [P] Implement the `ChatMessage` component in `ros2-textbook/src/components/Chat/ChatMessage.tsx`. It should be able to render messages from both the 'user' and the 'agent', including text, citations, and loading/error states.
- [X] T006 Implement the basic layout of the `ChatWidget` component in `ros2-textbook/src/components/Chat/ChatWidget.tsx`. This includes the message history area, a text input, and a submit button. It should not have any state logic yet.

---

## Phase 3: User Story 1 - General Question Answering [US1]

**Goal**: Implement the core functionality for asking questions and receiving answers.
**Independent Test**: On a local dev server, open the chat, ask a question, and verify a mock response is displayed correctly with clickable citations.

### Implementation Tasks
- [X] T007 [US1] Implement the `useChat` custom hook in `ros2-textbook/src/components/Chat/useChat.ts`. This hook will manage the chat state: messages, loading status, error status, and input handling.
- [X] T008 [US1] Implement the `apiClient` in `ros2-textbook/src/components/Chat/apiClient.ts`. It should export a function that takes a `ChatRequestPayload` and makes a `fetch` POST request to the backend, handling the response and errors.
- [X] T009 [US1] Integrate the `useChat` hook and `apiClient` into `ros2-textbook/src/components/Chat/ChatWidget.tsx` to handle form submission, display conversation history, and manage loading/error states.
- [X] T010 [US1] Use Docusaurus swizzling to wrap the `@theme/Root` component. Create `ros2-textbook/src/theme/Root.tsx` to render the original `Root` component along with the `ChatButton` and the lazy-loaded `ChatWidget` (inside a `Suspense` boundary).
- [X] T011 [US1] Implement the citation click handler logic. This function, likely in a `utils.ts` file, will take a citation, find the corresponding element on the page, scroll to it, and apply a temporary highlight effect via a CSS class defined in `custom.css`.

---

## Phase 4: User Story 2 - Contextual Query from Selected Text [US2]

**Goal**: Enable users to ask questions about a specific piece of selected text.
**Independent Test**: Highlight text on a page, verify a "Chat about this" button appears, and confirm that using it sends the selected text to the backend.

### Implementation Tasks
- [X] T012 [P] [US2] Create a new React component, `SelectionListener`, that listens for text selection events on the page (`document.onselectionchange`).
- [X] T013 [P] [US2] When text is selected, the `SelectionListener` should display a small "Chat about this" button or tooltip near the selected text.
- [X] T014 [US2] When the "Chat about this" button is clicked, it should open the chat widget and pass the selected text into the chat state, to be included as the `code_block` in the next API request.
- [X] T015 [US2] Integrate the `SelectionListener` into the swizzled `ros2-textbook/src/theme/Root.tsx` so it is active on all pages.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goal**: Ensure the integration is robust, accessible, and well-styled.

- [X] T016 Add comprehensive styling to all chat components in `ros2-textbook/src/components/Chat/styles.module.css` and `ros2-textbook/src/css/custom.css`, ensuring a polished look in both light and dark modes.
- [X] T017 Implement graceful error handling in the UI for API failures (e.g., backend is down) and display clear messages to the user.
- [X] T018 Ensure the chat widget is accessible (e.g., keyboard navigation, ARIA attributes).
- [X] T019 Verify that the Docusaurus production build (`npm run build`) completes successfully without errors.

## Dependencies

-   **US1** depends on **Phase 1** and **Phase 2**.
-   **US2** depends on **US1** (as it extends the chat widget's functionality).
-   This entire feature is dependent on a running **Agentic RAG Backend** (Feature `009-agentic-rag-backend`).

## Parallel Execution

-   Within **Phase 2**, tasks T004 and T005 can be developed in parallel.
-   Within **Phase 3 [US1]**, task T008 (API client) can be developed in parallel with T007 (state hook).
-   Within **Phase 4 [US2]**, tasks T012 and T013 can be developed in parallel.
