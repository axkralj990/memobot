#!/usr/bin/env python3
"""
Daily Log Assistant - Main Entry Point

This script runs the Discord bot that:
1. Listens to Discord messages in a specific channel
2. Parses natural language descriptions using OpenAI
3. Creates structured entries in Notion database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_env_vars():
    """Check that all required environment variables are set."""
    required = {
        "DISCORD_BOT_TOKEN": "Discord bot authentication token",
        "DISCORD_CHANNEL_ID": "Discord channel ID to monitor",
        "NOTION_API_KEY": "Notion integration API key",
        "NOTION_DATABASE_ID": "Notion database ID",
        "OPENAI_API_KEY": "OpenAI API key for GPT parsing",
    }
    
    missing = []
    for var, description in required.items():
        if not os.getenv(var):
            missing.append(f"  - {var}: {description}")
    
    if missing:
        print("❌ Missing required environment variables in .env:\n")
        print("\n".join(missing))
        print("\nPlease add these to your .env file.")
        sys.exit(1)


def main():
    """Run the Discord bot."""
    print("🚀 Starting Daily Log Assistant...")
    
    # Check environment
    check_env_vars()
    
    # Import and run bot
    from src.discord_bot import run_bot
    
    print("\n📝 Bot will:")
    print("  1. Listen to Discord messages")
    print("  2. Parse them with OpenAI GPT")
    print("  3. Create Notion database entries")
    print("\n⏳ Starting bot...\n")
    
    run_bot()


if __name__ == "__main__":
    main()
