# Research: Agentic RAG Backend

This document outlines the key research areas for building the agentic RAG backend. Although the initial implementation will use stubs, this research informs the design for a future production-ready system.

## 1. Gemini API Integration

**Decision**: For the initial implementation, a stubbed `GeminiClient` will be used. For a full implementation, the official Google Generative AI SDK for Python (`google-generativeai`) would be integrated.

**Rationale**: The feature specification requires a runnable stub implementation. Using the actual SDK would introduce external dependencies and authentication requirements (API keys) that are out of scope for the initial, local-only setup. The stub allows for development and testing of the agent's logic without incurring API costs or dealing with network latency.

**Alternatives considered**:
- **Direct HTTP requests**: Using libraries like `requests` or `httpx` to call the Gemini REST API. This was rejected as the official SDK provides better abstractions, error handling, and is the recommended approach by Google.

**Key Research Points for Full Integration**:
- **Authentication**: How to manage API keys securely. The best practice is to use environment variables (e.g., via a `.env` file and `python-dotenv`) and never hardcode keys in the source code.
- **Error Handling**: Investigating the specific error types the Gemini API can return (e.g., rate limiting, content filtering, server errors) and implementing robust retry logic (e.g., with exponential backoff).
- **Tool Calling**: Understanding how to use the tool calling/function calling feature of the Gemini API to ground answers and generate citations.

## 2. AgentCore Architecture (inspired by OpenAI Agent SDK)

**Decision**: The `AgentCore` class will be a simple, stateless processor that orchestrates the interaction between the user query, the (stubbed) retrieval mechanism, and the (stubbed) LLM. It will not be a direct copy of the OpenAI SDK but will follow similar principles of separating concerns.

**Rationale**: The feature spec requires a custom agent framework. A simple, stateless class is sufficient to meet the requirements and avoids pulling in a large third-party library. The key methods (`answer_question`, `generate_pytest`) directly map to the user stories.

**Alternatives considered**:
- **LangChain or LlamaIndex**: These are powerful agent frameworks. They were rejected because the spec explicitly asks for a custom implementation to keep the stack minimal and focused. For a production system, using one of these frameworks would be a serious consideration to accelerate development.

## 3. Grounding and Citation Mechanism

**Decision**: The `AgentCore` will receive a list of `Document` objects (representing retrieved context) along with the user's query. When the `GeminiClient` stub is called, it will be passed this context. The stub's response will include a hardcoded citation to demonstrate the required output format.

**Rationale**: This approach simulates the core RAG pattern: retrieve, then generate. The citation mechanism is a critical feature, and even in the stubbed implementation, the data structures and API responses must account for it.

**Key Research Points for Full Integration**:
- **Context Chunking**: How to split the retrieved documents into chunks that fit within the LLM's context window.
- **Citation Accuracy**: Developing a reliable method to trace which part of the generated answer came from which specific source document. This might involve post-processing the LLM's output or using tool calling to force the model to cite its sources.
- **Handling "I don't know"**: Designing a prompt that encourages the LLM to state when it cannot answer a question from the provided context, fulfilling the "Zero Hallucination" principle.