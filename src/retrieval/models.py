from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ContentChunk(BaseModel):
    """
    Represents a single piece of content retrieved from the vector database,
    including its metadata and similarity score.
    """
    doc_id: str
    source_url: str
    text: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict) # To hold section_heading, etc.

class RetrievedContext(BaseModel):
    """
    The main object returned by the retrieval module.
    It contains the original query and the list of retrieved chunks.
    """
    query: str
    chunks: List[ContentChunk] = Field(default_factory=list)

class Query(BaseModel):
    """Simple input model for the retrieval function."""
    query: str
