import sys
import os
import logging

# Ensure src/ is importable
sys.path.append(os.path.abspath("src"))

from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr

from backend.agent_core import AgentCore
from backend.models import Query, ChatResponse

# --------------------
# Logging (important for HF Spaces)
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------
# Initialize Agent
# --------------------
agent = AgentCore()

# --------------------
# FastAPI App
# --------------------
app = FastAPI(title="ROS 2 Textbook RAG Backend")

class ChatRequest(BaseModel):
    question: str
    code_block: str | None = None


@app.post("/chat/query", response_model=ChatResponse)
async def chat_query(req: ChatRequest):
    """
    Programmatic API endpoint used by Vercel / Docusaurus frontend
    """
    logger.info(f"API query: {req.question[:80]}")

    query = Query(
        question=req.question,
        code_block=req.code_block,
    )

    response = agent.answer_question(query)

    return response


# --------------------
# Gradio UI
# --------------------
def rag_predict(user_input: str):
    """
    HF Spaces UI wrapper.
    Returns user-friendly text only.
    """
    if not user_input or not user_input.strip():
        return "Please ask a ROS 2 related question."

    logger.info(f"Gradio query: {user_input[:80]}")

    query = Query(
        question=user_input,
        code_block=None,
    )

    response = agent.answer_question(query)

    # ✅ System / greeting / identity responses
    if response.status == "system":
        return response.answer

    # ✅ Successful grounded answer
    if response.status == "success" and response.answer:
        return response.answer

    # ✅ Refusal (no context, invalid module, etc.)
    if response.refusal_reason:
        return response.refusal_reason

    # ✅ Final safety fallback
    return "I can only answer questions based on the ROS 2 textbook."


gradio_app = gr.Interface(
    fn=rag_predict,
    inputs=gr.Textbox(
        lines=4,
        placeholder="Ask a ROS 2 question from the textbook…"
    ),
    outputs=gr.Textbox(label="Answer"),
    title="ROS 2 Textbook Assistant",
    description="Answers questions strictly using the official ROS 2 textbook.",
)

# --------------------
# Mount Gradio on /
# --------------------
app = gr.mount_gradio_app(app, gradio_app, path="/")
