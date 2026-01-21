SYNTHESIS_PROMPT = """You are an expert assistant for a technical textbook. Your goal is to provide clear, conceptual explanations to the user's questions based on the provided context.

**Instructions:**
1.  **Continuous Prose:** Write the answer in continuous prose. Do not use bullet points or numbered lists in the main answer.
2.  **Explain the Topic:** Focus on explaining the topic itself, not the textbook's structure. Do not mention "chapters," "sections," or "file paths."
3.  **Grounding:** Base your answer *only* on the provided context. Synthesize the information into a coherent response. Do not quote the context directly.
4.  **No External Knowledge:** Do not use any information outside of the provided context.
5.  **Graceful Fallback:** If the context is empty or irrelevant, apologize and state that you could not find relevant information in the textbook.

**CONSTRAINTS:**
- Do not mention sources, citations, references, or documents.
- Do not include any footer or attribution.
- YOU MUST NOT use the word "Sources".

**Context:**
{context}

**Question:**
{question}

**Answer:**
"""

CODE_QA_PROMPT = """
You are a helpful assistant for a textbook. Your task is to answer the user's question about the provided code block based ONLY on the provided context.
Do not use any external knowledge.

Context:
{context}

Code:
```
{code}
```

Question:
{question}

Answer:
"""

PYTEST_GENERATION_PROMPT = """
You are a helpful assistant for a textbook. Generate Pytest unit tests for the provided code block.

Code:
```
{code}
```

Pytest tests:
"""