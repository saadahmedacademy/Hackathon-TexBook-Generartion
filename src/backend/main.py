from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import Query, ChatResponse
from .agent_core import AgentCore
import logging

# Initialize FastAPI app
app = FastAPI(
    title="Agentic RAG Backend",
    description="API for the RAG-powered conversational agent for the ROS 2 Textbook.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat/query", response_model=ChatResponse)
async def chat_query(request: Query):
    logger.info(f"Received query: '{request.question[:50]}...'")
    try:
        if "generate pytest" in request.question.lower():
            response_data = agent_core.generate_pytest(request.code_block)
            return ChatResponse(answer=response_data, citations=[], status="success")
        else:
            response_data = agent_core.answer_question(request)
            return response_data
    except Exception as e:
        logger.error(f"Error processing chat query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

