import typer
from typing_extensions import Annotated
import logging

from . import config
from . import crawler
from . import html_parser
from . import chunker
from . import embedder
from . import storage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = typer.Typer()

@app.command()
def run(
    url: Annotated[str, typer.Option(help="The base URL of the Docusaurus site to crawl.")] = config.VERCEL_URL,
    collection_name: Annotated[str, typer.Option(help="The name of the Qdrant collection to create or update.")] = config.QDRANT_COLLECTION_NAME,
    chunk_size: Annotated[int, typer.Option(help="The target size for content chunks in tokens.")] = 512,
    chunk_overlap: Annotated[int, typer.Option(help="The token overlap between adjacent chunks.")] = 50,
    force_recreate: Annotated[bool, typer.Option(help="If set, delete the Qdrant collection if it exists.")] = False,
):
    """
    Runs the full content ingestion pipeline.
    Crawl -> Parse -> Chunk -> Embed -> Store
    """
    logging.info("--- Starting Content Ingestion Pipeline ---")
    
    # 0. Initialize clients
    qdrant_client = storage.get_qdrant_client()
    cohere_client = embedder.get_cohere_client()

    # 1. Handle collection creation/recreation
    if force_recreate:
        logging.warning(f"Force recreate enabled. Deleting collection '{collection_name}' if it exists.")
        qdrant_client.delete_collection(collection_name=collection_name)
    
    # Using Cohere's default vector size for this model
    storage.create_collection(qdrant_client, collection_name, vector_size=1024)

    # 2. Crawl
    logging.info(f"Crawling site starting from {url}...")
    all_urls = crawler.get_all_page_urls(url)
    logging.info(f"Found {len(all_urls)} pages to process.")

    all_chunks = []
    for page_url in all_urls:
        logging.info(f"Processing: {page_url}")
        html_content = crawler.fetch_page_content(page_url)
        if not html_content:
            continue

        # 3. Parse
        parsed_result = html_parser.extract_content_from_html(html_content, page_url)
        if not parsed_result:
            logging.warning(f"  -> Skipping, no <article> tag found.")
            continue
        
        markdown_content, title = parsed_result
        url_meta = html_parser.get_metadata_from_url(page_url)

        # 4. Chunk
        chunks = chunker.chunk_text(
            markdown_content=markdown_content,
            url=page_url,
            module=url_meta.get("module"),
            chapter=url_meta.get("chapter"),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        all_chunks.extend(chunks)
        logging.info(f"  -> Created {len(chunks)} chunks.")

    # 5. Embed
    logging.info(f"\nEmbedding {len(all_chunks)} chunks in total...")
    chunk_texts = [chunk.text for chunk in all_chunks]
    # Process in batches for embedding to avoid hitting API limits
    batch_size = 96 # Cohere's API has a limit of 96 strings per call for embeddings
    all_embeddings = []
    for i in range(0, len(chunk_texts), batch_size):
        batch_texts = chunk_texts[i:i+batch_size]
        embeddings_batch = embedder.embed_chunks(cohere_client, batch_texts)
        all_embeddings.extend(embeddings_batch)
        logging.info(f"  -> Embedded batch {i//batch_size + 1}/{(len(chunk_texts)-1)//batch_size + 1}")


    # 6. Store
    logging.info(f"Storing {len(all_embeddings)} vectors in Qdrant...")
    storage.upsert_vectors(qdrant_client, collection_name, all_chunks, all_embeddings)
    
    logging.info("\n--- Pipeline Finished Successfully ---")


if __name__ == "__main__":
    app()

