"""
Configuration settings for the Browser-Use Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4.1"

# Agent Configuration
AGENT_NAME = "Web Agent"
AGENT_DESCRIPTION = "Browser automation assistant"

# Browser Configuration
BROWSER_MODEL = "gpt-4.1"

# UI Messages
WELCOME_MESSAGE = """🤖 Web Agent Started!
I can help you with web-based tasks like searching, shopping, booking, and more.
Type 'quit' or 'exit' to stop.
"""

GOODBYE_MESSAGE = "👋 Goodbye!"

# Error Messages
ERROR_NO_API_KEY = "❌ Error: OPENAI_API_KEY not found in environment variables"
ERROR_PROCESSING = "❌ Error processing request: {}"
ERROR_WEB_TASK = "❌ Error executing web task: {}" 