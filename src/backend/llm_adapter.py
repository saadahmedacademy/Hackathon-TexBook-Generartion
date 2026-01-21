from typing import Any, List, Optional, Dict
from google import genai
from pydantic import BaseModel, Field
import logging
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# This class will act as a stand-in for an LLM that the OpenAI Agent SDK might expect.
# It mimics the behavior of an LLM that can handle messages and potentially tool calls.
class GeminiAdapter:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        logger.info(f"GeminiAdapter initialized for model: {self.model_name}")

    def generate(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None, # Expects tools in a dict format similar to OpenAI
        **kwargs: Any,
    ) -> str:
        """
        Generates a response from Gemini based on a list of messages, potentially using tools.
        Returns a simplified string response for now, to be expanded for tool_code.
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not set.")
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        client = genai.Client(api_key=api_key)

        gemini_messages = []
        for msg in messages:
            role = 'user' if msg['role'] == 'user' else 'model'
            gemini_messages.append({'role': role, 'parts': [msg['content']]})

        gemini_tools = []
        if tools:
            for tool in tools:
                if tool.get("type") == "function" and "function" in tool:
                    gemini_tools.append(tool["function"])


        try:
            safety_settings = kwargs.get("safety_settings", [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ])
            
            generation_config = kwargs.get("generation_config", {})

            response = client.models.generate_content(
                model=self.model_name,
                contents=gemini_messages,
                safety_settings=safety_settings,
                generation_config=generation_config,
                tools=gemini_tools if gemini_tools else None
            )
            
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    part = candidate.content.parts[0]
                    if part.function_call:
                        tool_call = part.function_call
                        return json.dumps({
                            "tool_code": {
                                "name": tool_call.name,
                                "arguments": dict(tool_call.args)
                            }
                        })
                    elif part.text:
                        return part.text
                # Fallback for empty parts
                return ""
            else:
                logger.warning("Gemini API returned no candidates.")
                return ""
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise