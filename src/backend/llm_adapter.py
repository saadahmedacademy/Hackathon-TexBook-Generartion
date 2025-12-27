from typing import Any, List, Optional, Dict
import google.generativeai as genai
from pydantic import BaseModel, Field
import logging

from .config import GEMINI_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# This class will act as a stand-in for an LLM that the OpenAI Agent SDK might expect.
# It mimics the behavior of an LLM that can handle messages and potentially tool calls.
class GeminiAdapter:
    def __init__(self, model_name: str = "gemini-pro"):
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"GeminiAdapter initialized with model: {model_name}")

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
        gemini_messages = []
        for msg in messages:
            role = 'user' if msg['role'] == 'user' else 'model'
            gemini_messages.append({'role': role, 'parts': [msg['content']]})

        # Adapt tools to Gemini's FunctionDeclaration format
        gemini_tools = []
        if tools:
            for tool in tools:
                # Assuming 'tool' is like {"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}
                if tool.get("type") == "function" and "function" in tool:
                    func_spec = tool["function"]
                    gemini_tools.append(
                        genai.types.FunctionDeclaration(
                            name=func_spec["name"],
                            description=func_spec.get("description", ""),
                            parameters=func_spec.get("parameters", {})
                        )
                    )

        try:
            safety_settings = kwargs.get("safety_settings", [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ])
            
            # The generate_content call needs to include tools if they are provided
            generation_config = kwargs.get("generation_config", {})
            if gemini_tools:
                generation_config["tools"] = gemini_tools # Add tools to config if present

            response = self.model.generate_content(
                gemini_messages,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            if response.candidates:
                candidate_content = response.candidates[0].content
                # If Gemini decides to call a tool, its response will be a FunctionCall
                if candidate_content.function_calls:
                    tool_call = candidate_content.function_calls[0] # Assuming one tool call for simplicity
                    return json.dumps({
                        "tool_code": {
                            "name": tool_call.name,
                            "arguments": {k: v for k, v in tool_call.args.items()}
                        }
                    })
                else:
                    return candidate_content.parts[0].text
            else:
                logger.warning("Gemini API returned no candidates.")
                return ""
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise

