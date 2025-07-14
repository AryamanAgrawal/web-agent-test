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
    
    async def analyze_task_requirements(self, task_description: str) -> str:
        """
        Analyze a web task to identify required steps and information needed from the user
        
        Args:
            task_description: Description of the web task to analyze
            
        Returns:
            Analysis of the task including steps and required information
        """
        try:
            print(f"🔍 Analyzing task requirements: {task_description}")
            
            # Define common task patterns and their requirements
            task_patterns = {
                "flight": {
                    "keywords": ["flight", "fly", "airline", "airport", "travel"],
                    "required_info": [
                        "Departure city/airport",
                        "Destination city/airport", 
                        "Departure date",
                        "Return date (if round trip)",
                        "Number of passengers",
                        "Preferred departure time",
                        "Budget range",
                        "Airline preferences",
                        "Account login credentials (if booking)"
                    ],
                    "steps": [
                        "Navigate to airline website or booking platform",
                        "Enter departure and destination locations",
                        "Select travel dates",
                        "Choose number of passengers",
                        "Search for available flights",
                        "Filter by preferences (time, price, airline)",
                        "Select preferred flight",
                        "Enter passenger details",
                        "Complete payment process"
                    ]
                },
                "hotel": {
                    "keywords": ["hotel", "accommodation", "stay", "booking", "room"],
                    "required_info": [
                        "Destination city",
                        "Check-in date",
                        "Check-out date",
                        "Number of guests",
                        "Number of rooms",
                        "Budget range",
                        "Hotel preferences (star rating, amenities)",
                        "Account login credentials (if booking)"
                    ],
                    "steps": [
                        "Navigate to hotel booking website",
                        "Enter destination and dates",
                        "Specify number of guests and rooms",
                        "Search for available hotels",
                        "Filter by preferences and budget",
                        "Select preferred hotel",
                        "Choose room type",
                        "Enter guest details",
                        "Complete booking and payment"
                    ]
                },
                "restaurant": {
                    "keywords": ["restaurant", "reservation", "table", "dinner", "lunch"],
                    "required_info": [
                        "Restaurant name or cuisine type",
                        "Location/city",
                        "Date and time",
                        "Number of people",
                        "Dietary restrictions",
                        "Special requests",
                        "Contact information"
                    ],
                    "steps": [
                        "Find restaurant website or booking platform",
                        "Select location and date",
                        "Choose time slot",
                        "Specify party size",
                        "Enter contact details",
                        "Add special requests",
                        "Confirm reservation"
                    ]
                },
                "shopping": {
                    "keywords": ["buy", "purchase", "shop", "order", "amazon", "store"],
                    "required_info": [
                        "Specific product name or description",
                        "Budget range",
                        "Size/specifications (if applicable)",
                        "Quantity needed",
                        "Preferred brand",
                        "Delivery preferences",
                        "Account login credentials",
                        "Payment method",
                        "Shipping address"
                    ],
                    "steps": [
                        "Navigate to shopping website",
                        "Search for the product",
                        "Filter by specifications and price",
                        "Select preferred item",
                        "Add to cart",
                        "Review cart and quantities",
                        "Proceed to checkout",
                        "Enter shipping information",
                        "Complete payment"
                    ]
                },
                "search": {
                    "keywords": ["search", "find", "look up", "google", "information"],
                    "required_info": [
                        "Search query or topic",
                        "Specific type of information needed",
                        "Preferred sources (if any)"
                    ],
                    "steps": [
                        "Navigate to search engine",
                        "Enter search query",
                        "Review search results",
                        "Click on relevant links",
                        "Extract required information",
                        "Summarize findings"
                    ]
                }
            }
            
            # Analyze the task to determine type and requirements
            task_lower = task_description.lower()
            matched_pattern = None
            
            for pattern_name, pattern_data in task_patterns.items():
                if any(keyword in task_lower for keyword in pattern_data["keywords"]):
                    matched_pattern = pattern_data
                    break
            
            if matched_pattern:
                analysis = f"""
Task Analysis Complete:

📋 REQUIRED STEPS:
{chr(10).join(f"   {i+1}. {step}" for i, step in enumerate(matched_pattern["steps"]))}

❓ INFORMATION NEEDED FROM USER:
{chr(10).join(f"   • {info}" for info in matched_pattern["required_info"])}

⚠️  RECOMMENDATION: Please provide the above information before proceeding with the web task to ensure successful completion.
"""
            else:
                # Generic analysis for unknown task types
                analysis = f"""
Task Analysis Complete:

📋 GENERAL STEPS LIKELY NEEDED:
   1. Navigate to relevant website
   2. Locate required functionality
   3. Enter necessary information
   4. Complete the intended action
   5. Verify successful completion

❓ INFORMATION THAT MAY BE NEEDED:
   • Account login credentials
   • Personal information (name, email, phone)
   • Payment information (if purchasing)
   • Specific preferences or requirements
   • Contact details

⚠️  RECOMMENDATION: Please provide any relevant details about this task to ensure successful completion.
"""
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing task requirements: {str(e)}"

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
                    "name": "analyze_task_requirements",
                    "description": "Analyze a web task to identify required steps and information needed from the user before execution. Use this FIRST before executing any complex web task to ensure you have all necessary information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the web task to analyze for requirements"
                            }
                        },
                        "required": ["task_description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_web_task",
                    "description": "Execute a web-based task using browser automation. Use this ONLY AFTER analyzing task requirements and gathering necessary information from the user.",
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
        
        if tool_name == "analyze_task_requirements":
            return await self.analyze_task_requirements(tool_args["task_description"])
        elif tool_name == "execute_web_task":
            return await self.execute_web_task(
                tool_args["task_description"],
                tool_args["task_steps"]
            )
        elif tool_name == "get_current_status":
            return self.get_current_status()
        else:
            return f"Unknown function: {tool_name}" 