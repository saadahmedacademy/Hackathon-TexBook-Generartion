# Research: Retrieval and Validation Layer

This document records the research and decisions made for implementing the retrieval module.

## 1. Qdrant Search with Sentence-Transformer Embeddings

### Decision
We will use the `qdrant_client.search()` method. The `distance` metric for the collection should be `Cosine`, as this is standard for modern text embedding models. The search call will specify `limit` and `score_threshold` directly, as these are native parameters in Qdrant's search API. The `with_payload` parameter will be set to `True` to retrieve the full metadata stored with each vector.

### Rationale
This approach is the most direct and efficient way to leverage Qdrant for this task. Using the native parameters for filtering (`limit`, `score_threshold`) allows Qdrant to optimize the search process. Cosine similarity is the appropriate metric for comparing the orientation (and thus semantic similarity) of normalized embedding vectors.

### Alternatives Considered
- **Retrieving a large number of results and filtering in the client**: This would be inefficient, transferring unnecessary data over the network and adding complexity to the Python code. It's better to let the database do the filtering.

## 2. Sentence-Transformer Query Embeddings

### Decision
We will use the `all-MiniLM-L6-v2` model from `sentence-transformers`.

### Rationale
This is a lightweight, high-performance model suitable for symmetric semantic search (where the query and the documents have similar lengths and content). It runs locally, avoiding network latency and API costs.

### Alternatives Considered
- **Using a larger, more powerful model**: While models like `all-mpnet-base-v2` might provide slightly better accuracy, `all-MiniLM-L6-v2` offers an excellent balance of speed and quality for this application.

## 3. Error Handling for External Services

### Decision
The retrieval module's external API calls (to Qdrant) will be wrapped in a retry mechanism. A simple decorator will handle transient network errors, retrying up to 3 times with exponential backoff. For persistent HTTP errors (like 4xx authentication/permission issues or 5xx server errors), the function will log the error and gracefully return an empty list of results to the caller.

### Rationale
This strategy makes the module resilient to temporary network blips. By catching persistent errors and returning an empty list, the module signals a retrieval failure to the downstream system (the RAG agent) in a predictable way. This allows the agent to execute its "refuse to answer" logic without crashing.

### Alternatives Considered
- **Propagating exceptions directly**: This would require the calling service to implement detailed error handling specific to Qdrant, coupling it tightly to the retrieval module's implementation. Returning a predictable, empty result is a cleaner contract.