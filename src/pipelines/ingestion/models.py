from pydantic import BaseModel, Field
from typing import List, Dict

class PageContent(BaseModel):
    """Represents the raw, cleaned content from a single URL before chunking."""
    url: str
    html_content: str
    markdown_content: str
    title: str

class QdrantPayload(BaseModel):
    """Defines the structure of the metadata payload attached to each vector in Qdrant."""
    source_url: str
    module: str
    chapter: str
    section_heading: str
    content_type: str
    original_text: str

class ContentChunk(BaseModel):
    """Represents a single chunk of text ready for embedding."""
    text: str
    metadata: QdrantPayload

