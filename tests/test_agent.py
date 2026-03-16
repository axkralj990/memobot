#!/usr/bin/env python3
"""
Test the agentic system locally without Discord.

This demonstrates how the agent can:
1. Determine user intent (read vs write)
2. Use tools to accomplish tasks
3. Provide intelligent responses
"""

import os
from dotenv import load_dotenv
from src.agent import DailyLogAgent

load_dotenv()


def main():
    """Interactive CLI to test the agent."""
    print("🤖 Daily Log Agent - Interactive Test")
    print("=" * 50)
    print("\nExamples to try:")
    print("  - 'Yesterday I slept 8 hours and had 2 coffees'")
    print("  - 'What did I log yesterday?'")
    print("  - 'Show me my entry from March 15'")
    print("  - 'How was I feeling last Tuesday?'")
    print("\nType 'quit' to exit\n")
    
    # Initialize agent
    agent = DailyLogAgent(
        notion_db_id=os.getenv("NOTION_DATABASE_ID"),
        notion_token=os.getenv("NOTION_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤔 Agent thinking...")
            response = agent.process_message(user_input)
            
            print(f"\n🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
