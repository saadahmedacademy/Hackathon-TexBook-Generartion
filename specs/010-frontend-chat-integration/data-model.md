# Data Model: Frontend Chat Integration

This document defines the key data structures used within the React components for the chat widget.

## 1. ChatMessage (State Object)

This is the primary data structure used in the React state (`useState` or `useReducer`) to manage the conversation history.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | A unique identifier for the message (e.g., a timestamp or UUID). |
| `sender` | `'user' \| 'agent'` | Indicates who sent the message. |
| `text` | `string` | The message content to be displayed. |
| `citations` | `Array<Citation>` | (For agent messages only) A list of citations supporting the answer. |
| `isLoading`| `boolean` | (For agent messages only) A flag to indicate if the agent is currently "thinking". |
| `isError` | `boolean` | (For agent messages only) A flag to indicate if this message represents an error. |

## 2. Citation (State Object)

This is the data structure for a single citation, as received from the backend API.

| Field | Type | Description |
| :--- | :--- | :--- |
| `source_url` | `string` | The URL of the cited document page. |
| `section_heading` | `string` | The heading of the relevant section. |

## 3. ChatRequestPayload (API Payload)

This defines the JSON payload sent to the `POST /chat/query` backend endpoint.

| Field | Type | Description |
| :--- | :--- | :--- |
| `question` | `string` | The user's question. |
| `code_block`| `string \| null` | The optional code block or selected text context. |

## 4. ChatResponsePayload (API Payload)

This defines the expected JSON payload received from the `POST /chat/query` backend endpoint.

| Field | Type | Description |
| :--- | :--- | :--- |
| `answer` | `string` | The agent's response. |
| `citations`| `Array<Citation>` | A list of citation objects. |
| `refusal_reason` | `string \| null` | The reason for refusal, if any. |
