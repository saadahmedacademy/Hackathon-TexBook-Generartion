from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    """Represents the incoming request body for the POST /chat/query endpoint."""
    question: str
    code_block: Optional[str] = None

class Citation(BaseModel):
    """Represents a single source citation, linking to the textbook."""
    source_url: str
    section_heading: str

class ChatResponse(BaseModel):
    """Represents the outgoing response body from the POST /chat/query endpoint."""
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    refusal_reason: Optional[str] = None

class AgentToolInput(BaseModel):
    """
    Represents the input structure for tools the agent might use internally
    (e.g., the retrieval tool).
    """
    query: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
