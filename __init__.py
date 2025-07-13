"""
Browser-Use Agent Package

A web automation agent that uses OpenAI function calling and browser-use
for accomplishing complex web-based tasks.
"""

from .web_agent import WebAgent
from .tools import WebTools
from .config import *

__version__ = "1.0.0"
__author__ = "Browser-Use Agent"
__description__ = "Web automation agent with OpenAI function calling"

__all__ = [
    "WebAgent",
    "WebTools",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "BROWSER_MODEL",
    "WELCOME_MESSAGE",
    "GOODBYE_MESSAGE"
] 