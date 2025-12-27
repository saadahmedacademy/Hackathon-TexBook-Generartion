import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from .models import ContentChunk, QdrantPayload

def chunk_text(markdown_content: str, url: str, module: str, chapter: str, chunk_size: int = 512, chunk_overlap: int = 50) -> List[ContentChunk]:
    """
    Chunks the markdown content and creates ContentChunk objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_text(markdown_content)
    
    content_chunks = []
    # This is a simplified way to get section headings. A more advanced
    # implementation would parse the markdown structure more deeply.
    current_heading = "Introduction" 
    
    for text_chunk in chunks:
        # Simplistic heading detection
        lines = text_chunk.split('\n')
        for line in lines:
            if line.startswith('#'):
                current_heading = line.lstrip('# ').strip()
                break # Take the first heading found in the chunk
                
        payload = QdrantPayload(
            source_url=url,
            module=module,
            chapter=chapter,
            section_heading=current_heading,
            content_type='text', # Simple assumption, could be enhanced to detect code blocks
            original_text=text_chunk
        )
        
        content_chunks.append(ContentChunk(text=text_chunk, metadata=payload))
        
    return content_chunks

def generate_deterministic_id(url: str, content: str) -> str:
    """
    Generates a deterministic SHA256 hash for a chunk to be used as its ID.
    """
    return hashlib.sha256(f"{url}{content}".encode("utf-8")).hexdigest()
