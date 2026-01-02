from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    source_id: str
    content: str

class Query(BaseModel):
    question: str
    code_block: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[Document]
    status: str
    refusal_reason: Optional[str] = None