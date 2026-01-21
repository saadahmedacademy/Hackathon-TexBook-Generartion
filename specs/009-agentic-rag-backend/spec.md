# Feature Specification: Agentic RAG Backend

**Feature Branch**: `009-agentic-rag-backend`
**Created**: 2025-12-22
**Status**: Draft
**Input**: User description: "Build a grounded, agentic RAG backend using FastAPI and OpenAI Agent SDK. What I am building: - A stateless RAG agent API that answers questions using retrieved textbook context only Core capabilities (mandatory): A) Grounded Q&A with citations B) Code-aware reasoning over a highlighted code block C) Pytest unit test generation from textbook code Audience: - Students using the textbook - Hackathon judges evaluating rigor Success criteria: - Every answer includes citations - Out-of-scope questions result in refusal - No hallucinated APIs, concepts, or code - Agent passes a non-speculation test suite Constraints: - Agent framework: OpenAI Agent SDK - LLM: Gemini API - Backend: FastAPI - Agent must refuse when retrieval returns no context - Stateless per request Not building: - Embedding or ingestion logic - Frontend UI - Conversational memory"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Grounded Question Answering (Priority: P1)

As a student, I want to ask a question related to the textbook content and receive a concise, accurate answer with citations, so that I can quickly understand complex topics and verify the source of information.

**Why this priority**: This is the primary value proposition of the RAG chatbot and foundational for its utility.

**Independent Test**: The API can be tested by sending a POST request with a textbook-related question. The response should contain a relevant answer and verifiable citations from the textbook.

**Acceptance Scenarios**:

1.  **Given** a question directly answerable by the textbook content, **When** I send a POST request to `/chat/query`, **Then** I receive an answer that directly addresses the question and includes specific citations (URLs or section headings) to the source material.
2.  **Given** a question that is ambiguous or has multiple possible answers within the textbook, **When** I send a POST request, **Then** I receive an answer that acknowledges the ambiguity or provides a summary of different perspectives, with citations.

### User Story 2 - Code-Aware Context Reasoning (Priority: P2)

As a student, I want to provide a specific code block from the textbook along with a question, so that the agent can provide an answer that intelligently incorporates the context of that code.

**Why this priority**: This capability enhances the agent's utility for technical users and distinguishes it from a generic Q&A system.

**Independent Test**: The API can be tested by sending a POST request with a question and a relevant code block. The agent's response should demonstrate understanding of the provided code in its answer.

**Acceptance Scenarios**:

1.  **Given** a question about a code snippet and the code block itself, **When** I send a POST request to `/chat/query`, **Then** the agent's answer explains the code, suggests improvements, or clarifies its functionality based on the provided snippet.

### User Story 3 - Pytest Test Generation (Priority: P2)

As a student, I want to ask the agent to generate a Pytest unit test for a given code example from the textbook, so that I can easily verify its behavior and learn best practices for testing ROS 2 code.

**Why this priority**: This provides an advanced, practical tool that leverages the agent's code understanding to aid learning and development.

**Independent Test**: The API can be tested by requesting a Pytest test for a known textbook code example. The generated test should be syntactically correct, relevant to the code, and ideally executable (given necessary dependencies).

**Acceptance Scenarios**:

1.  **Given** a request to generate a Pytest for a code example (potentially inferred from context or explicitly provided), **When** I send a POST request to `/chat/query`, **Then** the agent returns a valid Pytest test function/file that logically tests the provided code.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST implement a FastAPI application to serve the RAG agent.
-   **FR-002**: The FastAPI application MUST expose a `POST /chat/query` endpoint.
-   **FR-003**: The `/chat/query` endpoint input MUST accept a `question` (string) and an optional `code_block` (string).
-   **FR-004**: The `/chat/query` endpoint output MUST return an `answer` (string), a list of `citations` (each with URL/section), and a `refusal_reason` (nullable string).
-   **FR-005**: The agent MUST be built using the OpenAI Agent SDK.
-   **FR-006**: The agent MUST use the Gemini API as its underlying Large Language Model (LLM).
-   **FR-007**: The agent MUST integrate with the **Retrieval and Validation Layer** (Feature `008-retrieval-validation-layer`) to fetch relevant context.
-   **FR-008**: The agent MUST refuse to answer if the retrieval layer returns no relevant context.
-   **FR-009**: The agent MUST operate in a stateless manner per request; no conversational memory is maintained by the backend.
-   **FR-010**: The agent MUST generate answers that are strictly grounded in the provided context from the retrieval layer.
-   **FR-011**: The agent MUST be capable of parsing and reasoning over provided `code_block` input.
-   **FR-012**: The agent MUST be capable of generating valid Pytest unit tests from code examples.
-   **FR-013**: The agent MUST ALWAYS provide specific citations for every piece of information in its answer.

### Key Entities

-   **ChatRequest**: Represents an incoming request to the chat endpoint. Attributes: `question` (str), `code_block` (Optional[str]).
-   **ChatResponse**: Represents the outgoing response from the chat endpoint. Attributes: `answer` (str), `citations` (List[str]), `refusal_reason` (Optional[str]).
-   **RetrievedContext**: Data structure provided by the retrieval layer (Feature `008-retrieval-validation-layer`), containing `query` and `chunks` (List of `ContentChunk`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: Grounding: 100% of answers provided by the agent MUST include verifiable citations directly from the textbook content.
-   **SC-002**: Non-speculation: For a test suite of out-of-scope questions, the agent refuses to answer 100% of the time, providing an appropriate `refusal_reason`.
-   **SC-003**: Fidelity: 0% of agent responses contain hallucinated APIs, concepts, or code not present in the provided context or core knowledge.
-   **SC-004**: Utility: Generated Pytest tests are syntactically valid and demonstrably relevant to the code examples (evaluated manually).
-   **SC-005**: Performance: The `POST /chat/query` endpoint responds within **Under 5 seconds** for typical queries.
-   **SC-006**: Availability: The FastAPI application maintains **99.5% (Two and a Half Nines)** uptime during hackathon evaluation.

## Dependencies

-   **Retrieval and Validation Layer** (Feature `008-retrieval-validation-layer`): Provides the `retrieve_context` function to fetch relevant textbook chunks.

## Constraints

-   **LLM Provider**: Gemini API ONLY.
-   **Agent Framework**: OpenAI Agent SDK ONLY.
-   **Backend Framework**: FastAPI ONLY.

## Unresolved Questions / Clarifications

-   **Agent Framework / LLM Compatibility**: The OpenAI Agent SDK will be adapted to work with the Gemini API by implementing a custom adapter/wrapper. This approach prioritizes control and flexibility, acknowledging the added development overhead.