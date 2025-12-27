# Data Model: Retrieval and Validation Layer

This document defines the primary Python data structures (using Pydantic for validation) that form the public interface of the retrieval module.

## 1. Query (Input)

This is the simple input to the retrieval function.

| Field | Type | Description |
| :--- | :--- | :--- |
| `query` | `str` | The user's question as a raw string. |

## 2. ContentChunk (Output Component)

This represents a single piece of content retrieved from the vector database, including its metadata and similarity score.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `doc_id` | `str` | The unique identifier for the source document. | `"module-2/chapter-1"` |
| `source_url` | `str` | The direct URL to the source page. | `"/docs/module-2/chapter-1"` |
| `text` | `str` | The actual text content of the chunk. | `"ROS 2 services are a form of..."` |
| `score` | `float` | The cosine similarity score from the Qdrant search. | `0.8123` |
| `metadata`| `dict` | The rest of the payload from Qdrant. | `{"section_heading": ...}`|

## 3. RetrievedContext (Output)

This is the main object returned by the retrieval module. It contains the original query and the list of retrieved chunks.

| Field | Type | Description |
| :--- | :--- | :--- |
| `query` | `str` | The original query string that was processed. |
| `chunks` | `List[ContentChunk]` | A ranked list of `ContentChunk` objects, ordered from most to least relevant. |