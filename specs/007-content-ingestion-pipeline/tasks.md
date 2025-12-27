# Tasks: Content Ingestion and Embedding Pipeline

This document outlines the actionable tasks to implement the content ingestion pipeline for the ROS 2 Docusaurus textbook.

## Implementation Strategy

The implementation will follow a modular, phased approach. We will first set up the project structure and dependencies. Then, we will build each component of the pipeline (crawler, parser, chunker, embedder, storage) as a separate, focused module. Finally, a main script will orchestrate these modules to perform the end-to-end ingestion process.

**MVP Scope**: The MVP for this feature is the completion of all tasks defined below, resulting in a fully functional, command-line-driven ingestion pipeline that populates a Qdrant collection from the live Docusaurus site.

---

## Phase 1: Project Setup

**Goal**: Initialize the project structure, dependencies, and configuration management.

- [X] T001 Create the root directory for the pipeline at `src/pipelines/ingestion/`.
- [X] T002 Create a `requirements.txt` file in the root directory and add `qdrant-client`, `cohere`, `requests`, `beautifulsoup4`, `markdownify`, `langchain`, `python-dotenv`, `typer`.
- [X] T003 [P] Implement a configuration module in `src/pipelines/ingestion/config.py` to load environment variables (VERCEL_URL, COHERE_API_KEY, QDRANT_URL, QDRANT_COLLECTION_NAME) using `python-dotenv`.
- [X] T004 [P] Create an empty `__main__.py` inside `src/pipelines/ingestion/` to make it a runnable module.

---

## Phase 2: Foundational Data Models

**Goal**: Define the core data structures that will be used throughout the pipeline.

- [X] T005 Create `src/pipelines/ingestion/models.py` and define Pydantic models for `PageContent`, `ContentChunk`, and the `QdrantPayload` based on `data-model.md`.

---

## Phase 3: User Story 1 - Automated Content Ingestion [US1]

**Goal**: Implement the full, end-to-end content ingestion pipeline.
**Independent Test**: Execute the main script against the live Vercel URL and verify that the specified Qdrant collection is populated with the correct number of vectors and that their metadata is accurate.

### Test Tasks
- [X] T006 [US1] Create an evaluation script `tests/validate_ingestion.py` that connects to Qdrant, fetches a sample of 10 random vectors, and validates that their payloads match the expected `QdrantPayload` schema.

### Implementation Tasks
- [X] T007 [P] [US1] Implement the `crawler` module in `src/pipelines/ingestion/crawler.py`. It should contain a function that fetches a sitemap or recursively finds all page URLs from the base VERCEL_URL.
- [X] T008 [P] [US1] Implement the `html_parser` module in `src/pipelines/ingestion/html_parser.py`. It should contain a function that takes HTML content and extracts the clean text and code blocks from the `<article>` tag, along with section headings.
- [X] T009 [US1] Implement the `chunker` module in `src/pipelines/ingestion/chunker.py`. This module will take Markdown text, use `RecursiveCharacterTextSplitter` to chunk it, and generate a deterministic ID for each chunk using the `hash(page_url + chunk_content)` strategy.
- [X] T010 [P] [US1] Implement the `embedder` module in `src/pipelines/ingestion/embedder.py`. This will be a wrapper around the Cohere client, handling authentication and exposing a function to embed a list of text chunks.
- [X] T011 [P] [US1] Implement the `storage` module in `src/pipelines/ingestion/storage.py`. This will be a wrapper around the `qdrant-client`, handling collection creation and batch upserting of `QdrantPoint` objects.
- [X] T012 [US1] Implement the main orchestration logic in `src/pipelines/ingestion/__main__.py`. This script will use `typer` to handle CLI arguments and will call the other modules in the correct sequence: Crawl -> Parse -> Chunk -> Embed -> Store.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Goal**: Add logging, error handling, and final documentation.

- [X] T013 [P] Add structured logging (e.g., using Python's `logging` module) to all modules to provide visibility into the pipeline's execution.
- [X] T014 [P] Implement robust error handling, including retries for network requests (in `crawler` and `embedder`) and graceful skipping of unparseable pages, as defined in `research.md`.
- [X] T015 Create a `README.md` in the `src/pipelines/ingestion/` directory, documenting the setup and execution steps from the `quickstart.md`.

## Dependencies

- **US1** is dependent on the completion of **Phase 1** and **Phase 2**.

## Parallel Execution

- Within **Phase 1** and **Phase 4**, tasks marked with `[P]` can be worked on concurrently.
- Within **Phase 3 [US1]**, the core modules (`crawler`, `html_parser`, `embedder`, `storage`) can be developed in parallel as they are self-contained units. The main orchestration script (`__main__.py`) should be implemented after the core modules have a defined interface.
