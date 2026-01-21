from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .models import Query, ChatResponse
from .agent_core import AgentCore
from .gemini_client import GeminiClient # Added import
import logging
from dotenv import load_dotenv
import signal
import sys
import os # Added os import

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    logging.error(f"Received signal: {sig}. Exiting gracefully.")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
# Note: SIGSEGV and SIGABRT are harder to catch gracefully, but we register them for logging.
try:
    signal.signal(signal.SIGSEGV, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
except (ValueError, AttributeError):
    logging.warning("Could not register SIGSEGV or SIGABRT handlers (likely on Windows).")

# Load environment variables
load_dotenv()

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agentic RAG Backend",
    description="API for the RAG-powered conversational agent for the ROS 2 Textbook.",
    version="1.0.0",
)

# --- Startup event handler ---
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    # Check for GEMINI_API_KEY
    if not os.getenv("GEMINI_API_KEY"):
        logger.critical("GEMINI_API_KEY environment variable not set. Exiting.")
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")
    logger.info("GEMINI_API_KEY check passed.")

    # Perform Gemini API health check
    try:
        gemini_client_for_health_check = GeminiClient()
        if not gemini_client_for_health_check.check_health():
            logger.critical("Gemini API health check failed on startup. Exiting.")
            raise RuntimeError("Gemini API health check failed on startup.")
        logger.info("Gemini API health check passed.")
    except Exception as e:
        logger.critical(f"Failed to initialize GeminiClient for health check: {e}. Exiting.")
        raise RuntimeError(f"Failed to initialize GeminiClient for health check: {e}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/chat/query", response_model=ChatResponse, response_model_exclude_none=True)
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

