import os
from dotenv import load_dotenv
from src.notion import get_notion_entry
from src.models import DailyEntry

load_dotenv()

if __name__ == "__main__":
    database_id = os.getenv("NOTION_DATABASE_ID")
    notion_token = os.getenv("NOTION_API_KEY")
    
    raw_entry = get_notion_entry(database_id, notion_token)
    entry = DailyEntry.from_notion(raw_entry)
    print(entry.model_dump_json(indent=2))
