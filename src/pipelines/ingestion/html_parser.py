from bs4 import BeautifulSoup
from markdownify import markdownify as md
import logging

def extract_content_from_html(html_content: str, base_url: str) -> tuple[str, str] | None:
    """
    Extracts the main content from a Docusaurus page's HTML.
    
    Returns a tuple of (markdown_content, title) or None if no article tag is found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    main_content = soup.find("main")
    if not main_content:
        logging.warning(f"No <main> tag found on page with base URL: {base_url}")
        return None
        
    # Extract title, usually the first h1
    title_tag = main_content.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    # Convert main_content content to Markdown
    # This helps in cleaning up the HTML and structuring the text
    markdown_content = md(str(main_content), heading_style="ATX")
    
    return markdown_content, title

def get_metadata_from_url(url: str) -> dict:
    """Derives module and chapter from the URL path."""
    path_parts = [part for part in url.split('/') if part]
    metadata = {"module": "general", "chapter": "index"}

    # Example logic, might need adjustment for the exact URL structure
    if 'docs' in path_parts:
        docs_index = path_parts.index('docs')
        if len(path_parts) > docs_index + 1:
            metadata['module'] = path_parts[docs_index + 1]
        if len(path_parts) > docs_index + 2:
            metadata['chapter'] = path_parts[docs_index + 2]
            
    return metadata
