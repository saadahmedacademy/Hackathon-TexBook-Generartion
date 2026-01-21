# Implementation Plan: Agentic RAG Backend

**Feature Branch**: `009-agentic-rag-backend`
**Feature Spec**: [spec.md](spec.md)
**Created**: 2025-12-22
**Status**: In Progress

## 1. Technical Context

### 1.1. High-Level Approach

The RAG agent will be exposed as a stateless FastAPI application, serving a `POST /chat/query` endpoint. This endpoint will receive user questions and optional code blocks. Internally, the application will orchestrate the following:
1.  **Retrieval**: Invoke the `retrieve_context` function from the **Retrieval and Validation Layer** (Feature `008-retrieval-validation-layer`) to fetch relevant textbook chunks based on the user's question.
2.  **Agent Orchestration**: Utilize the OpenAI Agent SDK to manage the conversational flow.
3.  **LLM Interaction**: A custom adapter will be implemented to translate OpenAI Agent SDK's model calls to the Gemini API, ensuring the agent uses Gemini for its reasoning.
4.  **Tool Use**: The agent will be equipped with tools for:
    -   Accessing the retrieved context.
    -   Potentially interacting with code execution environments (for Pytest generation/validation).
5.  **Response Generation**: Gemini will generate a grounded answer, including citations.
6.  **Validation & Refusal**: The application will validate the response for grounding and refuse to answer if retrieval fails or the answer is deemed out-of-scope/speculative.

### 1.2. Architecture Overview

-   **Client <-> FastAPI App**: Client sends requests to `/chat/query`.
-   **FastAPI App -> Agent Layer**: FastAPI routes the request to the agent logic.
-   **Agent Layer (OpenAI Agent SDK)**:
    -   Handles tool calling for retrieval.
    -   Orchestrates prompts for Gemini.
    -   Manages agent workflow (e.g., grounding, refusal logic).
-   **Agent Layer -> Gemini Adapter**: Agent SDK communicates with Gemini via a custom adapter.
-   **Gemini Adapter -> Gemini API**: Translates requests to Gemini's format.
-   **Agent Layer -> Retrieval Tool**: Invokes `008-retrieval-validation-layer`'s `retrieve_context` function.

### 1.3. Technology Choices

-   **Backend Framework**: FastAPI
-   **Agent Orchestration**: OpenAI Agent SDK
-   **LLM Provider**: Gemini API
-   **Retrieval**: `008-retrieval-validation-layer` module
-   **Data Validation**: Pydantic (implicitly used by FastAPI and for data models)
-   **Language**: Python 3.11+

### 1.4. Dependencies & Integration Points

-   **Upstream**: Retrieval and Validation Layer (Feature `008-retrieval-validation-layer`).
-   **Downstream**: Frontend Chat Integration (Feature `006-frontend-chat-integration`).
-   **External**: Gemini API, Qdrant (via retrieval layer).
-   **API Keys**: GEMINI_API_KEY will be managed via environment variables.

### 1.5. Unresolved Questions

-   None. All clarifications from the spec have been resolved.

## 2. Constitution Check (Pre-Design)

-   [X] **Spec-Driven Development**: This plan is based on the approved feature specification (`009-agentic-rag-backend/spec.md`).
-   [X] **Single Source of Truth**: The agent is explicitly designed to answer ONLY from the textbook content (via retrieval).
-   [X] **Zero Hallucination**: The agent's core responsibility is to refuse speculative or out-of-scope answers, directly addressing the zero hallucination principle.
-   [X] **Clear, Consistent Terminology**: Terminology (RAG, agent, citations) is consistent with the spec and overall project.

**Result**: No violations detected.

## 3. Implementation Phases

### Phase 0: Research

This phase will focus on understanding the specifics of integrating the chosen technologies.

-   **`research.md`**: A document will be generated to consolidate findings on:
    1.  **OpenAI Agent SDK Custom LLM Integration**: How to subclass or adapt existing interfaces in the OpenAI Agent SDK to use a non-OpenAI LLM provider (Gemini API) effectively. This will cover prompt formatting, response parsing, and error handling.
    2.  **OpenAI Agent SDK Tool Definition**: Best practices for defining and integrating custom tools (specifically for retrieval and potentially a Python code interpreter for Pytest generation) within the OpenAI Agent SDK.
    3.  **Prompt Engineering for Groundedness and Citations**: Strategies for crafting effective system prompts and few-shot examples for Gemini to ensure answers are strictly grounded, avoid speculation, and always include citations.
    4.  **Pytest Generation Best Practices**: How to prompt Gemini for robust and syntactically correct Pytest test cases, and considerations for providing necessary context (code, dependencies).

### Phase 1: Design and Contracts

This phase will produce the core design artifacts for the FastAPI application and agent.

-   **`data-model.md`**: Define Pydantic models for `ChatRequest`, `ChatResponse`, `Citation` (internal to `ChatResponse`), and potentially internal data structures for agent state or tools.
-   **`contracts/api.yaml`**: An OpenAPI 3.0 specification for the `POST /chat/query` and `GET /health` endpoints, including request/response schemas, examples, and error codes.
-   **`quickstart.md`**: A guide demonstrating how to start the FastAPI application and interact with the `/chat/query` endpoint using `curl` or a simple Python script.
-   **Agent Context Update**: Run `.specify/scripts/bash/update-agent-context.sh gemini` to add relevant technologies and concepts to the agent's knowledge base.

## 4. Risks & Mitigations

-   **Risk**: Custom adapter for Gemini API proves difficult to implement or limits OpenAI Agent SDK functionality.
    -   **Mitigation**: Prioritize the most critical features (grounded Q&A). If a full feature set is not achievable, document limitations and propose alternatives (e.g., using a different agent framework for advanced features).
-   **Risk**: Gemini API latency impacts the 5-second response time target.
    -   **Mitigation**: Implement asynchronous FastAPI endpoints. Optimize retrieval calls. Consider streaming responses if necessary (though the spec implies a single response).
-   **Risk**: Agent hallucination despite guardrails and system prompts.
    -   **Mitigation**: Implement a robust validation step post-Gemini response to re-check grounding against retrieved context before sending to the client. Fine-tune system prompts.
-   **Risk**: Complex Pytest generation.
    -   **Mitigation**: Start with simpler code examples. Provide clear instructions to Gemini. Manual validation of generated tests will be crucial.

## 5. Constitution Check (Post-Design)

-   [X] **Spec-Driven Development**: All design artifacts (data models, API contracts) directly reflect the requirements from `spec.md`.
-   [X] **Single Source of Truth**: The agent's core function is to derive answers strictly from the textbook content via the retrieval layer.
-   [X] **Zero Hallucination**: The design explicitly incorporates refusal logic and grounding instructions to mitigate hallucination.
-   [X] **Clear, Consistent Terminology**: Terminology in data models, API contracts, and quickstart guide is consistent with the spec and overall project.

**Result**: No violations detected. The plan is sound.