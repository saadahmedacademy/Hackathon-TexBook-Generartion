from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging

from .config import GEMINI_API_KEY # Ensure all configs are loaded
from .models import ChatRequest, ChatResponse, Citation
from .agent_core import AgentCore

# Initialize FastAPI app
app = FastAPI(
    title="Agentic RAG Backend",
    description="API for the RAG-powered conversational agent for the ROS 2 Textbook.",
    version="1.0.0",
)

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize AgentCore
agent_core = AgentCore()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Agentic RAG Backend!"}

# Health check endpoint (T019)
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    logger.info(f"Received query: '{request.question[:50]}...'")
    try:
        response_data = agent_core.get_agent_response(request.question, request.code_block)
        return ChatResponse(**response_data)
    except Exception as e:
        logger.error(f"Error processing chat query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

