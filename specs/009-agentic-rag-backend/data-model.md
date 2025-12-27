# Data Model: Agentic RAG Backend

This document defines the Pydantic models for the FastAPI application's request/response payloads and key internal data structures.

## 1. ChatRequest (Input)

Represents the incoming request body for the `POST /chat/query` endpoint.

| Field | Type | Description |
| :--- | :--- | :--- |
| `question` | `str` | The user's natural language question. |
| `code_block` | `Optional[str]` | An optional code snippet provided by the user for context. |

## 2. Citation (Internal & Output Component)

Represents a single source citation, linking to the textbook.

| Field | Type | Description |
| :--- | :--- | :--- |
| `source_url` | `str` | The full URL of the cited page/section. |
| `section_heading` | `str` | The specific heading within the source material. |

## 3. ChatResponse (Output)

Represents the outgoing response body from the `POST /chat/query` endpoint.

| Field | Type | Description |
| :--- | :--- | :--- |
| `answer` | `str` | The agent's generated answer to the question. |
| `citations` | `List[Citation]` | A list of sources supporting the answer. Empty if no answer provided. |
| `refusal_reason` | `Optional[str]` | If the agent refused to answer, this field explains why. Null otherwise. |

## 4. AgentToolInput (Internal)

Represents the input structure for tools the agent might use internally (e.g., the retrieval tool).

| Field | Type | Description |
| :--- | :--- | :--- |
| `query` | `str` | The query for the tool. |
| `metadata` | `Dict[str, Any]` | Additional metadata for the tool (e.g., `top_k`, `score_threshold`). |
