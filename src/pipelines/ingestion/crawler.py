import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from .retry_decorator import retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@retry()
def _fetch_url_content(url: str) -> requests.Response:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response

def get_all_page_urls(base_url: str) -> list[str]:
    """
    Crawls a website from a base URL to find all unique page URLs.
    It starts from the base, finds all internal links, and recursively visits them.
    """
    visited = set()
    to_visit = {base_url}
    base_netloc = urlparse(base_url).netloc

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue

        try:
            logging.info(f"Crawling: {current_url}")
            response = _fetch_url_content(current_url)
            visited.add(current_url)
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(current_url, href)
                parsed_full_url = urlparse(full_url)

                # Ensure the link is internal to the same domain and is a new, valid URL
                if (parsed_full_url.netloc == base_netloc and 
                        full_url not in visited and
                        parsed_full_url.scheme in ["http", "https"]):
                    to_visit.add(full_url)
                    
        except requests.RequestException as e:
            logging.warning(f"Could not fetch {current_url} after multiple retries: {e}")

    # Filter out non-html content if necessary, though Docusaurus links are clean
    return sorted(list(visited))

def fetch_page_content(url: str) -> str | None:
    """Fetches the raw HTML content of a single page."""
    try:
        response = _fetch_url_content(url)
        return response.text
    except requests.RequestException as e:
        logging.warning(f"Failed to retrieve content for {url} after multiple retries: {e}")
        return None
