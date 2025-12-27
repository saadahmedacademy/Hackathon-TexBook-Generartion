# Research: Agentic RAG Backend

This document records the research findings and decisions for implementing the RAG Backend.

## 1. OpenAI Agent SDK Custom LLM Integration (Gemini API)

### Decision
We will implement a custom `llm_chain.base.BaseLanguageModel` (or similar interface depending on the exact SDK version) wrapper that bridges the OpenAI Agent SDK's expectations with the Google Gemini API. This custom class will encapsulate the Gemini API client and translate requests and responses. Key aspects will include:
-   Mapping OpenAI Agent SDK's message format (roles, content) to Gemini's message format.
-   Handling Gemini's specific API parameters (e.g., `safety_settings`).
-   Converting Gemini's output (text, tool calls) back into a format consumable by the OpenAI Agent SDK.

### Rationale
This approach directly addresses the user's requirement to use OpenAI Agent SDK with the Gemini API, even though there is no native integration. Creating a thin wrapper allows us to leverage the orchestration capabilities of the OpenAI Agent SDK while adhering to the Gemini LLM constraint.

### Alternatives Considered
-   **Switching Agent Frameworks**: Ruled out by the "OpenAI Agent SDK ONLY" constraint.
-   **Using an existing community adapter**: Research (online search) did not immediately reveal a robust, actively maintained adapter specifically for this combination that matches the SDK's exact interface requirements. Building a minimal custom one provides more control and clarity.

## 2. OpenAI Agent SDK Tool Definition and Integration

### Decision
The retrieval functionality from Feature `008-retrieval-validation-layer` will be wrapped as a custom tool for the OpenAI Agent SDK. This tool will:
-   Accept a natural language query as input.
-   Call the `retrieve_context` function.
-   Return the `RetrievedContext` (list of `ContentChunk` objects) to the agent in a structured, parseable format (e.g., a string representation or JSON).

### Rationale
This aligns with the agentic paradigm, allowing the LLM to decide when and how to retrieve information. Providing structured output to the agent enhances its ability to reason over the retrieved context.

### Alternatives Considered
-   **Pre-retrieval**: Simply injecting the context into the prompt before the agent sees it. This bypasses the agent's ability to decide *when* retrieval is needed and makes the process less "agentic".

## 3. Prompt Engineering for Groundedness and Citations

### Decision
The system prompt for Gemini will explicitly instruct the agent to:
-   "Answer ONLY using the provided `CONTEXT`."
-   "If the `CONTEXT` does not contain enough information, state clearly that you cannot answer the question based on the available information."
-   "ALWAYS cite your sources from the `CONTEXT` by referencing the `source_url` and `section_heading` for each piece of information."
-   "For code-related questions, pay close attention to the provided `CODE_BLOCK` and explain/generate based on it."
A few-shot example will be used to demonstrate the desired output format, especially for citations.

### Rationale
Clear, unambiguous instructions in the system prompt are crucial for enforcing groundedness and citation requirements with LLMs. Few-shot examples help guide the model towards the desired output format, which is often more effective than instructions alone.

### Alternatives Considered
-   **Post-processing for citations**: Attempting to extract citations from a free-form answer after generation is brittle and prone to errors. It's more reliable to instruct the LLM to generate them directly.

## 4. Pytest Generation Best Practices

### Decision
For Pytest generation, the agent will be provided with:
-   The code snippet for which to generate tests (via the `code_block` input).
-   Instructions in the prompt to focus on unit tests using Pytest.
-   Guidance to generate tests that verify functionality, edge cases, and typical usage.
The agent might internally use a "code interpreter" tool (a tool that takes Python code and executes it, returning the output) to validate the generated tests (if feasible within the agent SDK).

### Rationale
Explicit instructions and relevant context (the code itself) are essential for generating high-quality code. The agent's ability to reason and potentially "test" its own generated tests (via a tool) would greatly improve the quality of the output.

### Alternatives Considered
-   **Generating tests without context**: Would likely lead to generic or incorrect tests.
-   **Relying solely on LLM to "know" Pytest**: While powerful, explicit guidance always yields better results.
