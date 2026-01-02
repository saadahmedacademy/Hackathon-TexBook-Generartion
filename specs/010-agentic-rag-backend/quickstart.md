# Quickstart

This document describes test scenarios for the Cohere API fix.

## Scenario 1: Successful Embedding

1.  User submits a query.
2.  The `embed_query` function successfully generates an embedding.
3.  The agent proceeds with the RAG pipeline.

## Scenario 2: Embedding Failure with Graceful Degradation

1.  User submits a query.
2.  The `embed_query` function fails to generate an embedding after multiple retries.
3.  The `embed_query` function returns `None`.
4.  The `agent_core` receives `None` and returns a `ChatResponse` with a `refusal_reason` indicating the failure.
5.  The FastAPI app returns a 200 OK response with the refusal.

## Scenario 3: Cached Embedding

1.  User submits a query that has been made recently.
2.  The `@lru_cache` decorator on `embed_query` returns the cached embedding without calling the Cohere API.
3.  The agent proceeds with the RAG pipeline using the cached embedding.