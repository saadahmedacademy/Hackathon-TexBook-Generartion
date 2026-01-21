import os
from google import genai
import logging
from src.retrieval.retry_decorator import retry

class GeminiClient:
    def __init__(self):
        # Initialization is now minimal. The client will be created on-demand.
        pass

    @retry(tries=3, delay=2)
    def query_llm(self, prompt: str) -> str:
        """
        Queries the Gemini LLM with the given prompt.
        The client is created lazily inside this method.
        """
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                # This check is important for graceful failure.
                logging.error("GEMINI_API_KEY environment variable not set.")
                return "Error: The API key is missing. Please configure the GEMINI_API_KEY environment variable."

            # Lazily instantiate the client here.
            client = genai.Client(api_key=api_key)
            
            # The model call is updated to the new SDK's format.
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # Correct model as per new guidelines
                contents=prompt
            )
            return response.text
        except Exception as e:
            logging.error(f"Error querying Gemini LLM: {e}", exc_info=True)
            return "The language model is currently unavailable. Please try again later."

    def check_health(self) -> bool:
        """
        Performs a lightweight health check of the Gemini API.
        """
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                logging.error("GEMINI_API_KEY environment variable not set. Health check cannot be performed.")
                return False

            # Lazily instantiate the client for the health check.
            client = genai.Client(api_key=api_key)
            
            # Attempt to list models as a lightweight check
            list(client.models.list())
            logging.info("Gemini API health check successful.")
            return True
        except Exception as e:
            logging.error(f"Gemini API health check failed: {e}", exc_info=True)
            return False