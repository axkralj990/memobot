#!/usr/bin/env python3
"""Simple test script to verify weather integration in Notion entries."""

import os
from datetime import date
from dotenv import load_dotenv
from src.models import DailyEntryInput, PhysicalStatus
from src.tools.create_tools import create_notion_entry

# Load environment variables
load_dotenv()

# Get credentials
database_id = os.getenv("NOTION_DATABASE_ID")
notion_token = os.getenv("NOTION_API_KEY")

if not database_id or not notion_token:
    print("❌ Missing NOTION_DATABASE_ID or NOTION_API_KEY in .env")
    exit(1)

# Create a simple entry
entry = DailyEntryInput(
    entry_date=date.today(),
    sleep_hrs=7.0,
    coffee=3,
    physical_status=PhysicalStatus.GOOD,
    general_notes="Testing weather integration"
)

print(f"📝 Creating entry for {entry.entry_date} with weather data...")
print(f"🌍 Location: Ljubljana (default)")

try:
    result = create_notion_entry(entry, database_id, notion_token, location="ljubljana")
    print(f"\n✅ Entry created successfully!")
    print(f"🔗 URL: {result['url']}")
    print(f"\n💡 Check the Notion page to see the weather callout block!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
