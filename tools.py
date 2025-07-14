"""
Tools module for Browser-Use Agent

Contains tool definitions and execution functions for OpenAI function calling.
"""

from typing import Dict, List, Any, Optional
from browser_use import Agent, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI
from config import BROWSER_MODEL


class WebTools:
    """Tools for web automation and agent functionality"""
    
    def __init__(self, browser_session: Optional[BrowserSession] = None):
        self.browser_llm = ChatOpenAI(model=BROWSER_MODEL)
        self.browser_session = browser_session
    
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
            agent = Agent(task=detailed_task, llm=self.browser_llm, use_vision=True, browser_session=self.browser_session)
            result = await agent.run()
            
            # Convert result to string for processing
            result_str = str(result) if result else ""
            
            # Check if the result indicates failure or incomplete task
            if result_str and self._is_task_unsuccessful(result_str):
                return f"❌ TASK_INCOMPLETE: {result_str}\n\nThe task could not be completed successfully. This might be due to:\n• Missing or incorrect information\n• Authentication issues\n• Website unavailable or changed\n• Payment or account setup required\n• Insufficient permissions\n\nPlease provide additional information or clarify the requirements to help complete this task."
            
            return f"✅ Web task completed successfully. Result: {result_str}"
            
        except Exception as e:
            error_msg = str(e)
            # Provide more specific error guidance based on error type
            if "login" in error_msg.lower() or "authentication" in error_msg.lower():
                return f"❌ AUTHENTICATION_ERROR: {error_msg}\n\nIt appears this task requires login credentials or authentication. Please provide:\n• Account username/email\n• Password or authentication method\n• Two-factor authentication codes if needed"
            elif "payment" in error_msg.lower() or "billing" in error_msg.lower():
                return f"❌ PAYMENT_ERROR: {error_msg}\n\nThis task requires payment information. Please provide:\n• Payment method (credit card, PayPal, etc.)\n• Billing address\n• Payment authorization"
            elif "permission" in error_msg.lower() or "access" in error_msg.lower():
                return f"❌ ACCESS_ERROR: {error_msg}\n\nAccess permissions are required. Please provide:\n• Proper account permissions\n• Admin access credentials\n• Required authorization"
            elif "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                return f"❌ CONNECTION_ERROR: {error_msg}\n\nThere was a connection issue. Please:\n• Check your internet connection\n• Try again in a few moments\n• Verify the website is accessible"
            else:
                return f"❌ EXECUTION_ERROR: {error_msg}\n\nThe task encountered an error. Please:\n• Verify all provided information is correct\n• Check if additional details are needed\n• Try rephrasing the task requirements"
    
    def _is_task_unsuccessful(self, result: str) -> bool:
        """
        Check if the task result indicates failure or incomplete execution
        
        Args:
            result: The result string from browser-use execution
            
        Returns:
            True if the task appears to be unsuccessful
        """
        failure_indicators = [
            "failed", "error", "unable", "cannot", "could not", "unsuccessful",
            "not found", "access denied", "permission denied", "login required",
            "authentication required", "timeout", "connection failed",
            "page not found", "server error", "unavailable"
        ]
        
        result_lower = result.lower()
        return any(indicator in result_lower for indicator in failure_indicators)
    
    async def retry_web_task(self, original_task_description: str, additional_information: str, task_steps: List[str]) -> str:
        """
        Retry a previously failed web task with additional information
        
        Args:
            original_task_description: The original task that failed
            additional_information: Additional info provided by user to resolve the failure
            task_steps: Updated steps incorporating the additional information
            
        Returns:
            Result of the retry attempt
        """
        try:
            print(f"🔄 Retrying web task: {original_task_description}")
            print(f"➕ Additional information: {additional_information}")
            print(f"📋 Updated steps: {', '.join(task_steps)}")
            
            # Combine original task, additional info, and steps
            enhanced_task = f"""
ORIGINAL TASK: {original_task_description}

ADDITIONAL INFORMATION PROVIDED:
{additional_information}

UPDATED STEPS TO FOLLOW:
{chr(10).join(f"- {step}" for step in task_steps)}

Please use the additional information to successfully complete the original task.
"""
            
            # Create and run the browser-use agent with enhanced context
            agent = Agent(task=enhanced_task, llm=self.browser_llm, use_vision=True, browser_session=self.browser_session)
            result = await agent.run()
            
            # Convert result to string for processing
            result_str = str(result) if result else ""
            
            # Check if the retry was successful
            if result_str and self._is_task_unsuccessful(result_str):
                return f"❌ RETRY_FAILED: {result_str}\n\nThe task retry was unsuccessful. The additional information provided may not have resolved the issue, or there may be other problems:\n• The website may have changed or be unavailable\n• Additional authentication or permissions may be required\n• The provided information may be incorrect or incomplete\n• Technical issues with the website\n\nPlease try providing different information or approach the task differently."
            
            return f"✅ Task retry successful! Result: {result_str}"
            
        except Exception as e:
            error_msg = str(e)
            return f"❌ RETRY_ERROR: {error_msg}\n\nThe retry attempt encountered an error. This could be due to:\n• The same issues that caused the original failure\n• New technical problems\n• Insufficient additional information\n\nPlease provide more details or try a different approach."
    
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
                    "description": "Execute a web-based task using browser automation. Use this ONLY AFTER analyzing task requirements and gathering necessary information from the user. If this function returns an error, ask the user for additional information to resolve the issue.",
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
                    "name": "retry_web_task",
                    "description": "Retry a previously failed web task with additional information provided by the user. Use this when execute_web_task has failed and the user has provided additional details to resolve the issue.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "original_task_description": {
                                "type": "string",
                                "description": "The original task description that failed"
                            },
                            "additional_information": {
                                "type": "string",
                                "description": "Additional information provided by the user to resolve the failure (e.g., login credentials, payment info, corrected details)"
                            },
                            "task_steps": {
                                "type": "array",
                                "description": "Updated list of steps that incorporate the additional information",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "required": ["original_task_description", "additional_information", "task_steps"]
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
        elif tool_name == "retry_web_task":
            return await self.retry_web_task(
                tool_args["original_task_description"],
                tool_args["additional_information"],
                tool_args["task_steps"]
            )
        elif tool_name == "get_current_status":
            return self.get_current_status()
        else:
            return f"Unknown function: {tool_name}" 