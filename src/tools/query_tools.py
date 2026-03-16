"""Notion API tools for querying and reading entries."""

import requests
from src.models import DailyEntry


def get_notion_entry(database_id: str, notion_token: str) -> dict | None:
    """Get one entry from Notion database using latest API structure."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    payload = {"page_size": 1}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 401:
        raise Exception(
            f"Unauthorized: Check that your integration token is valid and "
            f"the integration is connected to database {database_id}"
        )
    
    response.raise_for_status()
    return response.json()["results"][0] if response.json()["results"] else None


def query_daily_entries(
    database_id: str,
    notion_token: str,
    target_date: str,
    num_entries: int = 1
) -> dict:
    """Query daily entries from Notion by date."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    
    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "equals": target_date
            }
        },
        "page_size": num_entries
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    results = response.json()["results"]
    
    if not results:
        return {
            "success": False,
            "message": f"No entries found for {target_date}"
        }
    
    # Parse the first result
    entry = DailyEntry.from_notion(results[0])
    
    return {
        "success": True,
        "date": target_date,
        "entry": {
            "name": entry.name,
            "productivity": entry.productivity.value if entry.productivity else None,
            "anxiety_status": entry.anxiety_status.value if entry.anxiety_status else None,
            "physical_status": entry.physical_status.value if entry.physical_status else None,
            "sleep_hrs": entry.sleep_hrs,
            "coffee": entry.coffee,
            "weight_kg": entry.weight_kg,
            "mindful_min": entry.mindful_min,
            "alcohol_unt": entry.alcohol_unt,
            "supplements": [s.value for s in entry.supplements],
            "fish": entry.fish,
            "meat": entry.meat,
            "learned": entry.learned,
            "general_notes": entry.general_notes,
            "substances": entry.substances,
        },
        "url": entry.url
    }
