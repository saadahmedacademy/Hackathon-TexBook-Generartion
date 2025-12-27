import re
from openai_agent_sdk import Agent, Tool
from typing import List, Optional, Dict, Any
import logging
import json

from .llm_adapter import GeminiAdapter
from .tools import RetrievalTool
from .prompts import SYSTEM_PROMPT_GROUNDED_QNA # Import the prompt
from .models import Citation, ChatResponse # Import Citation Pydantic model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentCore:
    def __init__(self):
        # Initialize the custom Gemini LLM adapter
        self.llm = GeminiAdapter(model_name="gemini-pro") # Using gemini-pro as per common use

        # Define the tools available to the agent
        # The OpenAI Agent SDK expects tools to be instances of Tool class
        # with function definitions compatible with OpenAI's format.
        self.tools: List[Tool] = [
            Tool(
                name=RetrievalTool.name,
                description=RetrieralTool.description,
                func=RetrievalTool() # Instantiate the tool
            ),
            # Add other tools here (e.g., CodeInterpreterTool for Pytest generation/validation)
        ]

        # Initialize the Agent from OpenAI Agent SDK. This assumes the SDK's Agent can take
        # a custom LLM and tools directly, and will use the LLM's tool_calling capabilities.
        # Our GeminiAdapter now has rudimentary tool_calling support.
        # The Agent class may not be directly usable if our GeminiAdapter does not fully
        # conform to its expected LLM interface (e.g., for handling tool_code in responses).
        # For now, we will use a manual orchestration loop.
        self.agent = Agent(
            llm=self.llm,
            tools=self.tools,
        )
        logger.info("AgentCore initialized with GeminiAdapter and RetrievalTool.")

    def get_agent_response(self, user_query: str, code_block: str | None = None) -> Dict[str, Any]:
        """
        Orchestrates the agent's response based on user query and optional code block.
        Returns a dictionary containing the answer, citations, and refusal reason.
        """
        logger.info(f"AgentCore received query: '{user_query[:50]}...'\n")

        # --- Manual Retrieval Tool Call (Temporary, until full AgentSDK tool orchestration) ---
        # In a fully integrated OpenAI Agent SDK, the agent itself would decide WHEN to call tools.
        # For our current GeminiAdapter, we manually perform retrieval and inject context.
        
        logger.info(f"Manually triggering retrieval tool for query: '{user_query[:50]}...'\n")
        retrieval_input = json.dumps({"query": user_query})
        retrieval_tool_output_str = self.tools[0].func(retrieval_input) # Call the RetrievalTool func
        
        try:
            retrieval_tool_output = json.loads(retrieval_tool_output_str)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from retrieval tool: {retrieval_tool_output_str}")
            return {
                "answer": "An internal error occurred while processing retrieval results.",
                "citations": [],
                "refusal_reason": "Internal retrieval processing error."
            }

        if retrieval_tool_output["status"] == "no_context":
            logger.warning("Retrieval tool returned no relevant context.")
            return {
                "answer": "I cannot answer your question based on the available information.",
                "citations": [],
                "refusal_reason": "No relevant context found for the query."
            }
        
        context = retrieval_tool_output["context"]
        context_str = "\n".join([f"Source: {c['source_url']}, Section: {c['section_heading']}\nContent: {c['text']}" for c in context])

        # Prepare the messages for the LLM
        messages_for_llm: List[Dict[str, Any]] = []
        
        # Prepend the system prompt with the retrieved context
        system_message_content = SYSTEM_PROMPT_GROUNDED_QNA.format(
            context=context_str,
            code_block=code_block if code_block else "None provided."
        )
        messages_for_llm.append({"role": "system", "content": system_message_content})
        messages_for_llm.append({"role": "user", "content": user_query})
        
        try:
            # Call the LLM adapter with messages and tools (for Gemini to understand available tools)
            llm_raw_response = self.llm.generate(messages_for_llm, tools=[t.openai_function for t in self.tools])
            
            # Check if Gemini wants to make a tool call (unlikely for final response with this flow)
            if isinstance(llm_raw_response, dict) and "tool_code" in llm_raw_response:
                logger.warning(f"Gemini attempted a tool call: {llm_raw_response['tool_code']}. Agent should respond with text here.")
                # For this iteration, we treat a tool call as an unexpected final response
                return {
                    "answer": "The agent attempted a tool call when a direct answer was expected. This scenario is not yet fully handled.",
                    "citations": [],
                    "refusal_reason": "Agent tool call instead of direct answer."
                }


            # Post-process the LLM's response to extract answer and citations
            answer_lines = llm_raw_response.split('\n')
            answer_parts = []
            citations: List[Citation] = []
            
            citation_pattern = r"\(Citation: (.+?), Section: (.+?)\)"

            for line in answer_lines:
                # Find all citations in the line
                found_citations = re.findall(citation_pattern, line)
                for source_url, section_heading in found_citations:
                    citations.append(Citation(source_url=source_url, section_heading=section_heading))
                
                # Remove citations from the answer text
                clean_line = re.sub(citation_pattern, "", line).strip()
                if clean_line:
                    answer_parts.append(clean_line)

            final_answer = " ".join(answer_parts).strip()

            # Check for explicit refusal phrases in the LLM's answer
            if any(phrase in final_answer.lower() for phrase in ["cannot answer your question", "not enough information", "not found in the context"]):
                logger.info("Agent decided to refuse due to insufficient context based on its response.")
                return ChatResponse(
                    answer=final_answer,
                    citations=[],
                    refusal_reason="Agent determined insufficient context from retrieval or its internal logic."
                ).model_dump() # Return as dict

            # Ensure citations are present if an answer is given
            if not citations and final_answer:
                 logger.warning(f"Answer provided but no citations extracted. LLM raw response: {llm_raw_response}")
                 return ChatResponse(
                    answer="I found some information, but could not extract proper citations. Please rephrase your question or check the textbook manually.",
                    citations=[],
                    refusal_reason="Could not extract citations from answer."
                ).model_dump() # Return as dict


            return ChatResponse(
                answer=final_answer,
                citations=citations,
                refusal_reason=None
            ).model_dump() # Return as dict

        except Exception as e:
            logger.error(f"Error during agent response generation: {e}", exc_info=True)
            return {
                "answer": "An internal error occurred during response generation.",
                "citations": [],
                "refusal_reason": "Internal generation error."
            }