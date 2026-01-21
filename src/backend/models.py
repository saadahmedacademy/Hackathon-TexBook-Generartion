from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    source_id: str
    content: str
    title: Optional[str] = None

class Query(BaseModel):
    question: str
    code_block: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: Optional[List[Document]] = None
    status: str
    refusal_reason: Optional[str] = None
    stream_id: Optional[str] = None