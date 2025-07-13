"""
Tools module for Browser-Use Agent

Contains tool definitions and execution functions for OpenAI function calling.
"""

from typing import Dict, List, Any
from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI
from config import BROWSER_MODEL


class WebTools:
    """Tools for web automation and agent functionality"""
    
    def __init__(self):
        self.browser_llm = ChatOpenAI(model=BROWSER_MODEL)
    
    async def execute_web_task(self, task_description: str, task_steps: List[str]) -> str:
        """
        Execute a web-based task using browser-use
        
        Args:
            task_description: Description of the web task to perform
            task_steps: List of steps to perform the task
            
        Returns:
            Result of the web task execution
        """
        try:
            print(f"🌐 Executing web task: {task_description}")
            print(f"📋 Steps: {', '.join(task_steps)}")
            
            # Combine task description with steps for better context
            detailed_task = f"{task_description}\n\nSteps to follow:\n" + "\n".join(f"- {step}" for step in task_steps)
            
            # Create and run the browser-use agent
            agent = Agent(task=detailed_task, llm=self.browser_llm)
            result = await agent.run()
            
            return f"Web task completed successfully. Result: {result}"
            
        except Exception as e:
            return f"Error executing web task: {str(e)}"
    
    def get_current_status(self) -> str:
        """Get current agent status"""
        return "Agent is ready to help with web-based tasks."
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Define available tools for OpenAI function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "execute_web_task",
                    "description": "Execute a web-based task using browser automation. Use this for tasks like searching, navigating websites, filling forms, extracting data, online shopping, booking reservations, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Clear and paraphrased description of the web task to perform (e.g., 'Search Google for Python tutorials', 'Buy a basketball on Amazon', 'Book a flight from NYC to LA')"
                            },
                            "task_steps": {
                                "type": "array",
                                "description": "List of steps to perform the task. Each step should be a clear and paraphrased description of the step to perform. For each task you should break it down into a list of steps.",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "required": ["task_description", "task_steps"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_status",
                    "description": "Get the current status of the agent",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
    
    async def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        """
        Execute a specific tool by name
        
        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool
            
        Returns:
            Result of the tool execution
        """
        print(f"🔧 Calling function: {tool_name}")
        
        if tool_name == "execute_web_task":
            return await self.execute_web_task(
                tool_args["task_description"],
                tool_args["task_steps"]
            )
        elif tool_name == "get_current_status":
            return self.get_current_status()
        else:
            return f"Unknown function: {tool_name}" 