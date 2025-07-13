"""
Main entry point for Browser-Use Agent

Provides the interactive loop for user interaction.
"""

import asyncio
from web_agent import WebAgent
from config import WELCOME_MESSAGE, GOODBYE_MESSAGE


async def run_agent_loop():
    """Main agent loop for interacting with users"""
    print(WELCOME_MESSAGE)
    
    try:
        agent = WebAgent()
    except ValueError as e:
        print(str(e))
        return
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(GOODBYE_MESSAGE)
                break
            
            if not user_input:
                continue
            
            # Process the input
            print("🤖 Agent: Processing your request...")
            response = await agent.process_user_input(user_input)
            print(f"🤖 Agent: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n{GOODBYE_MESSAGE}")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def main():
    """Main entry point"""
    asyncio.run(run_agent_loop())


if __name__ == '__main__':
    main() 