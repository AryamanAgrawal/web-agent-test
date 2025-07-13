"""
Main WebAgent class for Browser-Use Agent

Handles conversation flow, OpenAI integration, and orchestrates tool execution.
"""

import json
from typing import List, Dict, Any
import openai
from tools import WebTools
from config import OPENAI_API_KEY, OPENAI_MODEL, ERROR_NO_API_KEY, ERROR_PROCESSING


class WebAgent:
    """Main agent class that orchestrates web automation tasks"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_NO_API_KEY)
            
        self.conversation_history: List[Dict[str, Any]] = []
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.tools = WebTools()
        
    def get_system_message(self) -> Dict[str, str]:
        """Get the system message for the agent"""
        return {
            "role": "system",
            "content": """You are a helpful web automation agent. You can help users accomplish web-based tasks like:
            - Searching for information online
            - Online shopping (buying products)
            - Booking flights, hotels, restaurants
            - Filling out forms
            - Extracting data from websites
            - Navigating complex websites
            
            When a user asks for a web-based task, use the execute_web_task function with:
            1. A clear, detailed description of the task
            2. A list of specific steps to accomplish the task
            
            Break down complex tasks into manageable steps. For example:
            - "Buy a basketball on Amazon" → ["Navigate to Amazon", "Search for basketball", "Select a product", "Add to cart", "Proceed to checkout"]
            - "Book a flight" → ["Go to airline website", "Enter departure/arrival cities", "Select dates", "Choose flight", "Enter passenger details", "Complete booking"]
            
            For general questions or status checks, respond normally or use get_current_status.
            
            Be helpful, clear, and ask for clarification if the task is ambiguous."""
        }
    
    async def process_user_input(self, user_input: str) -> str:
        """Process user input using OpenAI function calling"""
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Prepare messages for OpenAI
        messages = [self.get_system_message()] + self.conversation_history
        
        try:
            # Make OpenAI API call with tool calling
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,  # type: ignore
                tools=self.tools.get_available_tools(),  # type: ignore
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # Check if the model wants to call a tool
            if message.tool_calls:
                tool_call = message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the tool
                result = await self.tools.execute_tool(function_name, function_args)
                
                # Add tool call to conversation
                self.conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": json.dumps(function_args)
                            }
                        }
                    ]
                })
                
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
                
                # Get final response from the model
                final_response = self.openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[self.get_system_message()] + self.conversation_history  # type: ignore
                )
                
                final_message = final_response.choices[0].message.content or "Task completed."
                self.conversation_history.append({"role": "assistant", "content": final_message})
                
                return final_message
            
            else:
                # No tool call needed, just return the response
                response_content = message.content or "I'm ready to help with web tasks."
                self.conversation_history.append({"role": "assistant", "content": response_content})
                return response_content
                
        except Exception as e:
            error_msg = ERROR_PROCESSING.format(str(e))
            self.conversation_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        return self.conversation_history.copy() 