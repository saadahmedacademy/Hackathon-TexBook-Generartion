import sys
import os

sys.path.append(os.path.abspath("src"))

from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr

from backend.agent_core import AgentCore
from backend.models import Query

agent = AgentCore()

# --------------------
# FastAPI
# --------------------
app = FastAPI()

class ChatRequest(BaseModel):
    question: str
    code_block: str | None = None

@app.post("/chat/query")
async def chat_query(req: ChatRequest):
    query = Query(
        question=req.question,
        code_block=req.code_block
    )
    response = agent.answer_question(query)

    return {
        "answer": response.answer,
        "citations": getattr(response, "citations", []),
        "refusal_reason": response.refusal_reason,
    }

# --------------------
# Gradio UI
# --------------------
def rag_predict(user_input: str):
    if not user_input or not user_input.strip():
        return "Please ask a ROS 2 related question."

    query = Query(
        question=user_input,
        code_block=None
    )

    response = agent.answer_question(query)

    # ✅ Prefer explicit answer
    if response.answer:
        return response.answer

    # ✅ If refused, show reason (user-friendly)
    if response.refusal_reason:
        return response.refusal_reason

    # ✅ Final fallback (should be rare)
    return "I can only answer questions based on the ROS 2 textbook."

# Gradio Interface

gradio_app = gr.Interface(
    fn=rag_predict,
    inputs=gr.Textbox(lines=4, placeholder="Ask a ROS 2 question"),
    outputs=gr.Textbox(label="Answer"),
    title="ROS 2 Agentic RAG Backend",
)

# Mount Gradio on /
app = gr.mount_gradio_app(app, gradio_app, path="/")
