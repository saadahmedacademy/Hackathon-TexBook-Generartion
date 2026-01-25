import sys
import os

# Ensure src is on PYTHONPATH
sys.path.append(os.path.abspath("src"))

import gradio as gr
from backend.agent_core import AgentCore
from backend.models import Query


# Initialize agent once
agent = AgentCore()

def rag_predict(user_input: str):
    if not user_input or not user_input.strip():
        return "Please ask a valid ROS 2 question."

    query = Query(
        question=user_input,
        code_block=None
    )

    response = agent.answer_question(query)

    # Convert ChatResponse to string
    if response.status in {"success", "system"}:
        return response.answer or "No answer available."

    if response.status == "refused":
        return response.refusal_reason or "Query was refused."

    if response.status == "error":
        return response.refusal_reason or "An internal error occurred."

    return "Unexpected response state."



demo = gr.Interface(
    fn=rag_predict,
    inputs=gr.Textbox(
        lines=4,
        placeholder="Ask a question about the ROS 2 textbook..."
    ),
    outputs=gr.Textbox(label="Answer"),
    title="ROS 2 Agentic RAG Backend",
    description="Public API wrapper for the ROS 2 textbook chatbot",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
