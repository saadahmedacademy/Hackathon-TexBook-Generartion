# Implementation Plan: Frontend Chat Integration

**Feature Branch**: `010-frontend-chat-integration`
**Feature Spec**: [spec.md](spec.md)
**Created**: 2025-12-22
**Status**: In Progress

## 1. Technical Context

### 1.1. High-Level Approach
The chat widget will be developed as a self-contained set of React components within the existing Docusaurus `ros2-textbook` project. It will be globally available but will be lazy-loaded to ensure no impact on initial page load times. The integration will be achieved by "swizzling" a Docusaurus theme component (e.g., the root layout) to add a floating chat button and a portal for the chat modal itself. State management for the chat (messages, loading state, visibility) will be handled using React hooks (`useState`, `useReducer`, or `useContext`).

### 1.2. Architecture Overview
1.  **Chat Button**: A floating action button will be added to the UI, likely through Docusaurus's `Layout` component.
2.  **Lazy Loading**: The main chat widget component will be loaded dynamically only when the user first clicks the chat button, using `React.lazy()` and `Suspense`.
3.  **Chat Widget**: A modal or slide-in panel containing the chat interface. This will include:
    -   A message display area.
    -   A text input field with a submit button.
    -   Loading and error state indicators.
4.  **API Client**: A simple, lightweight client will be created to handle `fetch` requests to the `POST /chat/query` endpoint of the backend. It will manage request/response formats and error handling.
5.  **State Management**: Local component state will manage the conversation history, input values, and UI states (e.g., `loading`, `error`).
6.  **Citation Handling**: A utility function will be created to parse citations from the API response and render them as clickable links that use JavaScript to scroll to and highlight the corresponding element on the page.

### 1.3. Technology Choices
-   **Framework**: React (as part of Docusaurus)
-   **Styling**: CSS Modules (`.module.css`) to keep component styles scoped, supplemented by global styles in `custom.css` for the highlighting effect.
-   **API Communication**: Browser's native `fetch` API.

### 1.4. Dependencies & Integration Points
-   **Upstream**: A running instance of the **Agentic RAG Backend** (Feature `009-agentic-rag-backend`) accessible via a URL.
-   **Docusaurus Integration**: The implementation will use Docusaurus's "swizzling" feature to safely override theme components and add the chat functionality globally.

### 1.5. Unresolved Questions
-   None. The specification is clear and provides a solid foundation for the plan.

## 2. Constitution Check (Pre-Design)
-   [X] **Spec-Driven Development**: This plan is directly derived from the validated `spec.md`.
-   [X] **Single Source of Truth**: The feature is designed to consume information from the RAG backend, which is grounded in the textbook.
-   [X] **Zero Hallucination**: The UI will clearly display refusal messages from the backend, reinforcing the zero-hallucination principle to the user.
-   [X] **Clear, Consistent Terminology**: UI elements (Chat, Citations) will use terminology consistent with the project specs.

**Result**: No violations detected.

## 3. Implementation Phases

### Phase 0: Research
-   **`research.md`**: A document will be created to consolidate findings on:
    1.  **Docusaurus Swizzling**: The exact procedure for swizzling the `Layout` or `Root` component to add a global floating element without breaking future Docusaurus updates.
    2.  **React Lazy Loading**: Best practices for implementing `React.lazy()` with `Suspense` for the chat widget to ensure a smooth loading experience on first click.
    3.  **Scroll & Highlight**: A robust JavaScript technique to find an element on the page based on a citation's text/URL and smoothly scroll to it, applying a temporary highlight effect.

### Phase 1: Design and Contracts
-   **`data-model.md`**: This will define the frontend-specific data structures, such as the `ChatMessage` object used for rendering the conversation history in the React state.
-   **API Contracts**: Not applicable for the frontend, as it is a consumer of the backend API contract already defined in `specs/009-agentic-rag-backend/contracts/api.yaml`.
-   **`quickstart.md`**: This guide will provide instructions on how to run the Docusaurus site locally with the chat feature enabled, including how to set the backend API URL via an environment variable.

## 4. Risks & Mitigations
-   **Risk**: Docusaurus updates break the "swizzled" components.
    -   **Mitigation**: Follow Docusaurus's official swizzling guide, which encourages wrapping components rather than ejecting them completely. This makes the integration more resilient to upstream changes. Add comments to the code linking to the relevant Docusaurus documentation.
-   **Risk**: CORS issues when communicating between the Vercel-hosted frontend and the backend API.
    -   **Mitigation**: The backend FastAPI application (from Spec 3) must be configured with the correct CORS middleware to allow requests from the Vercel domain. This needs to be documented in both the backend and frontend `README.md` files.
-   **Risk**: The scroll-to-highlight feature is brittle if page content or structure changes.
    -   **Mitigation**: The highlighting logic should be as robust as possible, potentially relying on specific `id` attributes that can be added to section headings in the Docusaurus Markdown files, or by searching for text content if IDs are not available.

## 5. Constitution Check (Post-Design)



-   [X] **Spec-Driven Development**: The design artifacts directly reflect the requirements from the approved `spec.md`, including lazy-loading and citation handling.

-   [X] **Single Source of Truth**: The frontend is designed as a pure consumer of the RAG backend, which is grounded in the textbook.

-   [X] **Zero Hallucination**: The UI plan includes specific handling to display refusal messages from the backend, making the system's limitations clear to the user.

-   [X] **Clear, Consistent Terminology**: Frontend data models (`ChatMessage`) and UI elements are consistent with the project's terminology.



**Result**: No violations detected. The plan is sound.