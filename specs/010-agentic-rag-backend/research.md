# Research: Cohere API Error Handling and Caching

## Correct Cohere SDK Exceptions

-   **Decision**: Use `TooManyRequestsError` and `CohereAPIError` from `cohere.errors`.
-   **Rationale**: The existing code uses a non-existent `cohere.CohereError`. The official Cohere Python SDK documentation specifies these exception types for handling API errors, with `TooManyRequestsError` being crucial for rate-limiting.

## Rate-Limit-Aware Retry Logic

-   **Decision**: Implement a retry decorator with exponential backoff.
-   **Rationale**: A simple loop is insufficient. Exponential backoff is a standard strategy for handling rate limits, as it progressively increases the delay between retries, giving the API time to recover.

## Embedding Cache

-   **Decision**: Use `functools.lru_cache`.
-   **Rationale**: `lru_cache` is a standard, built-in Python decorator for caching function calls. It's efficient and perfectly suited for caching embedding results for identical queries, reducing API costs and latency.