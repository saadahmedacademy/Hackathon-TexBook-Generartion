# Data Model: Frontend Chat Integration

This feature uses the existing `ChatMessage` entity defined in the feature specification.

## ChatMessage

A data structure representing a single message in the chat history.

-   **sender**: `string` - The sender of the message ("user" or "agent").
-   **text**: `string` - The content of the message.
-   **citations**: `Array<any>` - A list of citations for agent messages.
-   **status**: `string` - The status of the message (`success`, `system`, `refused`, `error`).

This model is represented in the frontend by the `ChatResponsePayload` interface, which will remain unchanged.