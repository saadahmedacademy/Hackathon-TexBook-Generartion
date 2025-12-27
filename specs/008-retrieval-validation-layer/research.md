# Research: Retrieval and Validation Layer

This document records the research and decisions made for implementing the retrieval module.

## 1. Qdrant Search with Cohere Embeddings

### Decision
We will use the `qdrant_client.search()` method. The `distance` metric for the collection should be `Cosine`, as this is standard for modern text embedding models like Cohere's. The search call will specify `limit` and `score_threshold` directly, as these are native parameters in Qdrant's search API. The `with_payload` parameter will be set to `True` to retrieve the full metadata stored with each vector.

### Rationale
This approach is the most direct and efficient way to leverage Qdrant for this task. Using the native parameters for filtering (`limit`, `score_threshold`) allows Qdrant to optimize the search process. Cosine similarity is the appropriate metric for comparing the orientation (and thus semantic similarity) of normalized embedding vectors.

### Alternatives Considered
- **Retrieving a large number of results and filtering in the client**: This would be inefficient, transferring unnecessary data over the network and adding complexity to the Python code. It's better to let the database do the filtering.

## 2. Cohere Query Embeddings

### Decision
We will use the Cohere `embed-english-v3.0` model. When generating embeddings for user queries, the `input_type` parameter will be set to `"search_query"`. This is distinct from the `"search_document"` input type used during the ingestion phase.

### Rationale
Cohere's documentation explicitly states that their models are optimized differently for documents (to be stored) versus queries (to be searched). Using `"search_query"` for user input is critical for achieving the highest possible retrieval quality.

### Alternatives Considered
- **Using the same `input_type` for documents and queries**: This would lead to a mismatch in the vector space, degrading the quality of the similarity search and returning less relevant results.

## 3. Error Handling for External Services

### Decision
The retrieval module's external API calls (to Cohere and Qdrant) will be wrapped in a retry mechanism. A simple decorator will handle transient network errors, retrying up to 3 times with exponential backoff. For persistent HTTP errors (like 4xx authentication/permission issues or 5xx server errors), the function will log the error and gracefully return an empty list of results to the caller.

### Rationale
This strategy makes the module resilient to temporary network blips. By catching persistent errors and returning an empty list, the module signals a retrieval failure to the downstream system (the RAG agent) in a predictable way. This allows the agent to execute its "refuse to answer" logic without crashing.

### Alternatives Considered
- **Propagating exceptions directly**: This would require the calling service to implement detailed error handling specific to both Cohere and Qdrant, coupling it tightly to the retrieval module's implementation. Returning a predictable, empty result is a cleaner contract.