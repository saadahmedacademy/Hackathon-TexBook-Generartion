# Data Model: Agentic RAG Backend

This document defines the core data entities for the Agentic RAG Backend, as referenced in `spec.md` and `plan.md`. These models are used for processing requests and generating responses within the FastAPI application.

## 1. Query

Represents an incoming user request to the `/chat/query` endpoint. It is the input data model.

**Source**: `src/backend/models.py` (as a Pydantic model)

| Field Name | Type | Description | Required |
|---|---|---|---|
| `question` | string | The user's primary question in natural language. | Yes |
| `code_block` | string (optional) | An optional block of code provided by the user for context-aware questions or test generation. | No |

### Example JSON

```json
{
  "question": "How do I create a ROS 2 node in Python?",
  "code_block": "class MyNode(Node):\n  def __init__(self):\n    super().__init__('my_node')"
}
```

## 2. Response

Represents the JSON response sent back to the user from the `/chat/query` endpoint. It is the output data model.

**Source**: `src/backend/models.py` (as a Pydantic model)

| Field Name | Type | Description | Required |
|---|---|---|---|
| `answer` | string | The generated answer to the user's question. If the system cannot answer, this field should contain an explanatory message. | Yes |
| `sources` | array[string] | A list of source identifiers (e.g., document IDs, page numbers) that were used to generate the answer. Empty if the answer is not grounded or if the system could not answer. | Yes |
| `status` | string | The status of the response. Can be "success", "error", or "no_answer". | Yes |

### Example JSON

```json
{
  "answer": "To create a ROS 2 node, you inherit from the `rclpy.node.Node` class and call the parent constructor within your `__init__` method.",
  "sources": [
    "ros2_textbook_v1:chapter_3_page_12"
  ],
  "status": "success"
}
```

## 3. Document

Represents an internal data structure for a chunk of retrieved textbook content. This entity is used by the `AgentCore` to provide context to the LLM. It is not directly exposed in the API.

**Source**: `src/backend/models.py` (can be a Pydantic model or a dataclass)

| Field Name | Type | Description |
|---|---|---|
| `id` | string | A unique identifier for the document chunk. |
| `content` | string | The raw text content of the document chunk. |
| `source_reference` | string | A string indicating the origin of the content (e.g., textbook chapter, page number). This is used to populate the `sources` field in the `Response` model. |