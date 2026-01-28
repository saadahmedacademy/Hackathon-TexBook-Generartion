from pydantic import BaseModel, Field
from typing import List, Optional

class Document(BaseModel):
    source_id: str
    content: str
    title: Optional[str] = None

class Query(BaseModel):
    question: str
    code_block: Optional[str] = None

class Citation(BaseModel):
    source_url: str
    section_heading: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    refusal_reason: Optional[str] = None
    status: str = "success"
