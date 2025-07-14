"""
Main WebAgent class for Browser-Use Agent

Handles conversation flow, OpenAI integration, and orchestrates tool execution.
"""

import json
from typing import List, Dict, Any, Optional
import openai
from tools import WebTools
from config import OPENAI_API_KEY, OPENAI_MODEL, ERROR_NO_API_KEY, ERROR_PROCESSING
from browser_use import BrowserSession


class WebAgent:
    """Main agent class that orchestrates web automation tasks"""
    
    def __init__(self, browser_session: Optional[BrowserSession] = None):
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_NO_API_KEY)
            
        self.conversation_history: List[Dict[str, Any]] = []
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.tools = WebTools(browser_session=browser_session)
        self.browser_session = browser_session
        
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
            
            IMPORTANT WORKFLOW:
            1. For complex tasks (booking, shopping, etc.), FIRST use analyze_task_requirements to understand what steps and information are needed
            2. After analysis, STOP and present the results to the user. Ask them to provide any missing information.
            3. ONLY use execute_web_task when the user has provided all necessary details in a follow-up message
            4. If execute_web_task fails or returns an error, analyze the error and ask the user for additional information needed to resolve the issue
            
            CRITICAL: After calling analyze_task_requirements, DO NOT call any other functions. Wait for the user's response with the required information.
            
            ERROR HANDLING:
            - If a task fails with authentication errors, ask for login credentials
            - If a task fails with payment errors, ask for payment information
            - If a task fails with access errors, ask for proper permissions
            - If a task fails with connection errors, suggest trying again or checking connectivity
            - If a task fails for other reasons, ask the user to provide additional details or clarify requirements
            
            When you receive error responses from execute_web_task (messages starting with ❌), carefully read the error details and ask the user for the specific information needed to resolve the issue. Be specific about what information is missing.
            
            For simple tasks like basic searches, you may go directly to execute_web_task.
            For general questions or status checks, respond normally or use get_current_status.
            
            Always ask for clarification if information is incomplete. Never proceed with missing details."""
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
                

                
                # For other functions, get final response from the model
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