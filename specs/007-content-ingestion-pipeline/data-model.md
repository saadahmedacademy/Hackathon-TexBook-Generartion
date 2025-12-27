# Data Model: Content Ingestion Pipeline

This document defines the key data structures used during the ingestion pipeline.

## 1. PageContent

This object represents the raw, cleaned content extracted from a single URL before it is chunked.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `url` | `str` | The canonical URL of the source page. | "https://ros2-textbook.vercel.app/docs/intro" |
| `html_content` | `str` | The raw HTML content of the `<article>` tag. | "<article><h1>Introduction</h1>..." |
| `markdown_content` | `str` | The content after being converted to Markdown. | "# Introduction\n..." |
| `title` | `str` | The main title of the page, usually from the `<h1>`. | "Introduction" |

## 2. ContentChunk

This object represents a single chunk of text ready for embedding. It contains the text and the metadata that will eventually be stored in the Qdrant payload.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `text` | `str` | The actual text content of the chunk. | "A ROS 2 node is the..." |
| `metadata` | `dict` | A dictionary containing the payload for Qdrant. | `{"source_url": "...", "module": "..."}` |

## 3. QdrantPoint (Payload Structure)

This defines the structure of the metadata payload that will be attached to each vector in Qdrant.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `source_url` | `str` | The full URL of the page the chunk came from. | "https://ros2-textbook.vercel.app/docs/intro" |
| `module` | `str` | The parent module name, derived from the URL. | "module-1-ros-foundations" |
| `chapter` | `str` | The chapter name, derived from the URL. | "chapter-2" |
| `section_heading` | `str` | The nearest preceding heading for the chunk. | "Understanding ROS 2 Nodes" |
| `content_type` | `str` | The type of content ('text' or 'code'). | "text" |
| `original_text` | `str` | The original text of the chunk being embedded. | "A ROS 2 node is the..." |
