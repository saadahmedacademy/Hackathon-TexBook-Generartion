from typing import Any, Dict
import json
import logging

# Import the retrieve_context function from the retrieval layer
from src.retrieval.main import retrieve_context
from src.retrieval.models import RetrievedContext, ContentChunk, Query as RetrievalQuery # Alias Query to avoid conflict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RetrievalTool:
    """
    A tool for the OpenAI Agent SDK that wraps the retrieval layer
    to fetch relevant textbook context.
    """
    name = "retrieve_textbook_context"
    description = (
        "Retrieves relevant text chunks from the ROS 2 textbook based on a query. "
        "Input should be a JSON string with a 'query' field (string) "
        "and optional 'top_k' (int) and 'score_threshold' (float) fields."
        "Example: {'query': 'what is a ROS node?', 'top_k': 3, 'score_threshold': 0.7}"
    )

    def __call__(self, input_str: str) -> str:
        """
        Executes the retrieval tool.
        Args:
            input_str: A JSON string containing the query and optional retrieval parameters.
        Returns:
            A JSON string representing the RetrievedContext or an error message.
        """
        try:
            input_data = json.loads(input_str)
            query_text = input_data.get("query")
            top_k = input_data.get("top_k", 5) # Default from spec
            score_threshold = input_data.get("score_threshold", 0.75) # Default from spec

            if not query_text:
                raise ValueError("Query text is required for the retrieval tool.")

            logger.info(f"RetrievalTool: Calling retrieve_context for query: {query_text[:50]}...")
            retrieved_context: RetrievedContext = retrieve_context(
                query_text=query_text,
                top_k=top_k,
                score_threshold=score_threshold
            )

            if retrieved_context.chunks:
                # Format the chunks for the agent. Prioritize text and URL.
                formatted_chunks = []
                for chunk in retrieved_context.chunks:
                    formatted_chunks.append({
                        "text": chunk.text,
                        "source_url": chunk.source_url,
                        "doc_id": chunk.doc_id,
                        "section_heading": chunk.metadata.get("section_heading", "N/A")
                    })
                return json.dumps({"status": "success", "context": formatted_chunks})
            else:
                return json.dumps({"status": "no_context", "message": "No relevant context found in the textbook."})

        except json.JSONDecodeError:
            logger.error(f"RetrievalTool: Invalid JSON input: {input_str}")
            return json.dumps({"status": "error", "message": "Invalid JSON input for retrieval tool."})
        except ValueError as ve:
            logger.error(f"RetrievalTool: Invalid input data: {ve}")
            return json.dumps({"status": "error", "message": str(ve)})
        except Exception as e:
            logger.error(f"RetrievalTool: An unexpected error occurred: {e}", exc_info=True)
            return json.dumps({"status": "error", "message": f"An unexpected error occurred during retrieval: {e}"})

# Example of how to make this tool available to the OpenAI Agent SDK
# This would typically be done in the agent_core.py or main.py
tools_list = [RetrievalTool()]
