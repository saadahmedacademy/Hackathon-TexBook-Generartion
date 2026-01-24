# API Contract: Hugging Face Gradio Endpoint

This document specifies the contract for the production Agentic RAG backend deployed on Hugging Face Spaces. The frontend `apiClient.ts` will be updated to conform to this contract.

## Endpoint

-   **URL**: `{HF_SPACE_URL}/run/predict` (Resolved via `docusaurus.config.ts`)
-   **Method**: `POST`
-   **Headers**:
    -   `Content-Type`: `application/json`

## Request Payload

The request body must be a JSON object with a `data` field, which is an array containing the user's question as a single string element.

```json
{
  "data": [
    "What is a ROS 2 node?"
  ]
}
```

## Response Payload

The response from the Gradio API is a JSON object containing a `data` field. This field is an array where the first element (`json.data[0]`) is the JSON string of the `ChatResponsePayload`. The frontend client must parse this nested JSON string to get the final chat message object.

### Example Raw Response

```json
{
  "data": [
    "{\"status\":\"success\",\"message\":\"A ROS 2 node is...\",\"citations\":[{\"source\":\"/docs/module-2/...\"}]}"
  ],
  "event_id": "...",
  "fn_index": 0,
  "is_generating": false,
  "session_hash": "..."
}
```

### Unwrapped `ChatResponsePayload`

The inner JSON string (`data[0]`) will be parsed into the existing `ChatResponsePayload` interface in the frontend.

```typescript
interface ChatResponsePayload {
  status: 'success' | 'system' | 'refused' | 'error';
  message: string;
  citations: {
    source: string;
    content: string;
  }[];
}
```
