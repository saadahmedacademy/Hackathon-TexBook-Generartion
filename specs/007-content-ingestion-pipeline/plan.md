# Implementation Plan: Content Ingestion and Embedding Pipeline

**Feature Branch**: `007-content-ingestion-pipeline`
**Feature Spec**: [spec.md](spec.md)
**Created**: 2025-12-22
**Status**: In Progress

## 1. Technical Context

### 1.1. High-Level Approach

The pipeline will be a Python script that orchestrates the end-to-end process of getting content from the live Docusaurus website into the Qdrant vector database. The process is as follows:
1.  **Crawl**: Fetch the sitemap or recursively crawl the deployed Vercel URL to discover all textbook pages.
2.  **Parse**: For each page, parse the HTML to extract the main article content, stripping away navigation, sidebars, and footers.
3.  **Convert**: Convert the cleaned HTML for each page into Markdown format to restore a structured text representation.
4.  **Chunk**: Segment the Markdown text into deterministic chunks of 512 tokens with a 50-token overlap.
5.  **Embed**: Generate embeddings for each chunk using `sentence-transformers`.
6.  **Store**: Upsert the vectors and their rich metadata into a versioned Qdrant collection.

This approach is chosen because it decouples the ingestion pipeline from the Docusaurus source code repository, treating the deployed website as the canonical source of truth, per the user's constraint.

### 1.2. Technology Choices

-   **Language**: Python 3.10+
-   **Web Crawling/Parsing**: `requests` for HTTP calls, `BeautifulSoup4` for HTML parsing.
-   **HTML to Markdown**: `markdownify` library to convert HTML back to structured Markdown.
-   **Chunking**: LangChain's `RecursiveCharacterTextSplitter` for deterministic, token-based chunking.
-   **Embedding**: `sentence-transformers` Python SDK.
-   **Vector Database Client**: `qdrant-client` Python SDK.

### 1.3. Dependencies & Integration Points

-   **Upstream**: A publicly accessible URL for the deployed Docusaurus textbook on Vercel.
-   **Downstream**: The Qdrant collection produced by this pipeline will be consumed by the `008-retrieval-validation-layer`.
-   **External**: Requires network access to the Vercel URL and the Qdrant database. API keys and URLs will be managed via environment variables.

### 1.4. Unresolved Questions

-   None. The feature specification is clear.

## 2. Constitution Check (Pre-Design)

-   [X] **Spec-Driven Development**: This plan is derived directly from a validated feature spec (`007-content-ingestion-pipeline/spec.md`).
-   [X] **Single Source of Truth**: The plan treats the deployed textbook as the single source of truth for ingestion.
-   [X] **Zero Hallucination**: This pipeline does not generate content; it only processes existing content.
-   [X] **Clear, Consistent Terminology**: Terminology aligns with the spec (chunk, embedding, Qdrant).

**Result**: No violations detected.

## 3. Implementation Phases

### Phase 0: Research

This phase will confirm best practices for the chosen pipeline stages.

-   **`research.md`**: A document will be created to record findings on:
    1.  **Docusaurus Content Extraction**: Best CSS selectors to isolate the main content (`<main>`, `article`, etc.) from a Docusaurus page structure.
    2.  **Deterministic ID Generation**: A strategy for creating a unique, deterministic ID for each chunk to ensure idempotency when re-running the pipeline (e.g., hash of page URL + chunk content).
    3.  **Qdrant Batch Upsert**: Optimal batch sizes for inserting points into Qdrant to balance speed and memory usage.

### Phase 1: Design and Contracts

This phase will produce the core design artifacts.

-   **`data-model.md`**: This file will define the Python data classes for `ContentChunk` (before embedding) and the `QdrantPoint` structure, including the vector and its metadata payload (`source_url`, `module`, `chapter`, `section_heading`).
-   **API Contracts**: Not applicable. This feature is a standalone script.
-   **`quickstart.md`**: A guide detailing the setup (environment variables) and execution of the main ingestion script from the command line.
-   **Agent Context Update**: `.specify/scripts/bash/update-agent-context.sh gemini` will be run.

## 4. Risks & Mitigations

-   **Risk**: The Docusaurus website's HTML structure changes, breaking the parsing logic.
    -   **Mitigation**: The script will have robust error handling. If a page cannot be parsed, it will be logged and skipped, allowing the rest of the ingestion to complete. The CSS selectors will be configurable.
-   **Risk**: Inaccurate token counting leading to chunks larger than the model's limit.
    -   **Mitigation**: Use a tokenizer library that closely matches the `sentence-transformers` model's tokenization to ensure chunk size limits are respected.

## 5. Constitution Check (Post-Design)

-   [X] **Spec-Driven Development**: The design artifacts directly reflect the requirements from the approved `spec.md`.
-   [X] **Single Source of Truth**: The plan is designed to ingest from the deployed textbook, treating it as the canonical source.
-   [X] **Zero Hallucination**: The pipeline is deterministic and does not generate or alter content, only process it.
-   [X] **Clear, Consistent Terminology**: The `data-model.md` and `quickstart.md` use the terminology established in the spec.

**Result**: No violations detected. The plan is sound.