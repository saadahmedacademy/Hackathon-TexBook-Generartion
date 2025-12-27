# Feature Specification: Agentic RAG Backend

**Feature Branch**: `[005-agentic-rag-backend]`
**Created**: 2025-12-22
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Grounded Question Answering (Priority: P1)

As a user, I want to ask a question and receive a direct answer that is strictly based on the retrieved textbook content, including citations, so that I can trust the information is accurate.

**Why this priority**: This is the primary function of the TA chatbot, delivering trustworthy, grounded answers.

**Independent Test**: The API can be tested by sending POST requests with a question and mock retrieved context, then validating that the response is correctly generated and includes citations.

**Acceptance Scenarios**:

1.  **Given** a question and relevant context chunks, **When** I send a request to the `/chat/query` endpoint, **Then** I receive a synthesized answer and a list of source citations from the context.
2.  **Given** a question but the retrieval process returns no context, **When** I send a request to the `/chat/query` endpoint, **Then** I receive a response indicating the agent cannot answer, along with a `refusal_reason`.
3.  **Given** a question about a topic outside the textbook, **When** I send a request, **Then** the agent refuses to answer, stating the query is out of scope.

### User Story 2 - Code-Aware Context Reasoning (Priority: P2)

As a user, I want to provide a code block along with my question, so that the agent can use the code as context to provide a more accurate and relevant answer.

**Why this priority**: Enhances the chatbot's utility for developers and students working with code examples from the textbook.

**Independent Test**: Send POST requests that include a `code_block` and validate the agent's answer correctly incorporates or references the provided code.

**Acceptance Scenarios**:

1.  **Given** a question and a code block, **When** I send a request to `/chat/query`, **Then** the agent's answer considers the code block in its reasoning.

### User Story 3 - Pytest Test Generation (Priority: P2)

As a user, I want to ask the agent to generate a Pytest test for a code example from the textbook, so that I can quickly verify the code's functionality.

**Why this priority**: Provides a powerful, value-add capability that leverages the agent's understanding of code and the textbook's content.

**Independent Test**: Send a request asking for a pytest test for a specific function found in the textbook, and validate that the response contains valid, runnable Pytest code.

**Acceptance Scenarios**:

1.  **Given** a request to generate a test for a function in the textbook, **When** the agent has the function's code in its context, **Then** it returns a valid Pytest test file as part of its answer.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide a FastAPI backend.
-   **FR-002**: The backend MUST expose a stateless `/chat/query` endpoint via a POST request.
-   **FR-003**: The `/chat/query` input MUST accept a `question` (string) and an optional `code_block` (string).
-   **FR-004**: The `/chat/query` output MUST return `answer` (string), `citations` (list), and a nullable `refusal_reason` (string).
-   **FR-005**: The agent MUST be built using the OpenAI Agent SDK and the Gemini API.
-   **FR-006**: The agent MUST refuse to answer if the retrieval step fails or returns no context.
-   **FR-007**: 100% of generated answers MUST be accompanied by citations from the retrieved context.
-   **FR-008**: The agent MUST NOT hallucinate APIs, functions, or code that are not present in the provided context.

### Key Entities

-   **ChatQuery**: Represents an incoming request. Attributes: `question`, `code_block`.
-   **ChatResponse**: Represents an outgoing response. Attributes: `answer`, `citations`, `refusal_reason`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 100% of generated answers are accompanied by one or more citations.
-   **SC-002**: 100% of out-of-scope questions (as determined by the retrieval layer) result in a polite refusal to answer.
-   **SC-003**: In a sample set of generated code (e.g., Pytest tests), 0% contain hallucinated or non-existent APIs/functions.
-   **SC-004**: An OpenAPI schema is successfully generated and accurately reflects the API structure.
