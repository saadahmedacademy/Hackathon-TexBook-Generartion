QA_PROMPT = """
You are a helpful assistant for a textbook. Your task is to answer the user's question based ONLY on the provided context.
Do not use any external knowledge.
You must cite every factual claim you make by referencing the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

CODE_QA_PROMPT = """
You are a helpful assistant for a textbook. Your task is to answer the user's question about the provided code block based ONLY on the provided context.
Do not use any external knowledge.
You must cite every factual claim you make by referencing the provided context.

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