"""Notion API tools for creating entries."""

import requests
from datetime import date
from src.models import DailyEntryInput
from .weather_tools import get_weather_for_date, format_weather_summary


def _notion_headers(notion_token: str) -> dict:
    return {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


def _find_entries_by_date(
    database_id: str,
    notion_token: str,
    entry_date: date,
) -> list[dict]:
    """Return up to two pages matching a date so duplicates can be detected."""
    response = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=_notion_headers(notion_token),
        json={
            "filter": {
                "property": "Date",
                "date": {"equals": entry_date.isoformat()},
            },
            "page_size": 2,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["results"]


def _update_notion_entry(
    page: dict,
    entry: DailyEntryInput,
    notion_token: str,
) -> dict:
    """Patch only explicitly supplied database properties on an existing page."""
    supplied = entry.model_fields_set
    properties = {}

    select_fields = {
        "productivity": "Productivity",
        "anxiety_status": "Anxiety Status",
        "physical_status": "Physical Status",
    }
    for field, notion_name in select_fields.items():
        value = getattr(entry, field)
        if field in supplied and value is not None:
            properties[notion_name] = {"select": {"name": value.value}}

    number_fields = {
        "sleep_hrs": "Sleep (hrs)",
        "weight_kg": "Weight (kg)",
        "mindful_min": "Mindful (min)",
        "alcohol_unt": "Alcohol (unt)",
        "coffee": "Coffee (#)",
        "fasting": "Fasting",
        "cold_min": "Cold (min)",
        "points": "Points",
    }
    for field, notion_name in number_fields.items():
        value = getattr(entry, field)
        if field in supplied and value is not None:
            properties[notion_name] = {"number": value}

    text_fields = {
        "supplements": "Supplements",
        "learned": "Learned",
        "substances": "Substances",
    }
    for field, notion_name in text_fields.items():
        value = getattr(entry, field)
        if field in supplied and value:
            properties[notion_name] = {
                "rich_text": [{"text": {"content": value}}]
            }

    if "general_notes" in supplied and entry.general_notes:
        existing_items = (
            page.get("properties", {})
            .get("General Notes", {})
            .get("rich_text", [])
        )
        existing_notes = "".join(
            item.get("plain_text")
            or item.get("text", {}).get("content", "")
            for item in existing_items
        ).strip()
        combined_notes = (
            f"{existing_notes}\n\n{entry.general_notes}"
            if existing_notes
            else entry.general_notes
        )
        properties["General Notes"] = {
            "rich_text": [{"text": {"content": combined_notes}}]
        }

    if not properties:
        return {**page, "_memobot_action": "updated"}

    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page['id']}",
        headers=_notion_headers(notion_token),
        json={"properties": properties},
        timeout=30,
    )
    response.raise_for_status()
    return {**response.json(), "_memobot_action": "updated"}


def determine_emoji(entry_date: date, general_notes: str | None, location: str) -> str:
    """Determine the appropriate emoji based on date, content, and location."""
    notes_lower = (general_notes or "").lower()
    
    # Priority order - check specific keywords first
    if any(word in notes_lower for word in ["flying", "flight", "airplane", "airport"]):
        return "🛩️"
    
    if any(word in notes_lower for word in ["hiking", "hike", "mountain", "climb"]):
        return "🏔️"
    
    if any(word in notes_lower for word in ["party", "birthday", "celebration", "celebrating"]):
        return "🎉"
    
    if any(word in notes_lower for word in ["forest", "woods", "trail", "nature walk"]):
        return "🌲"
    
    # Coastal/sea check
    coastal_cities = [
        "split", "zadar", "dubrovnik", "rijeka", "krk", "pula", "rovinj", "poreč", "makarska",
        "barcelona", "lisbon", "porto", "valencia", "nice", "cannes", "marseille",
        "naples", "venice", "miami", "san diego", "los angeles", "sydney", "melbourne"
    ]
    location_lower = location.lower()
    if (any(word in notes_lower for word in ["sea", "beach", "surfing", "swimming", "ocean", "krk", "coast"]) or
        any(city in location_lower for city in coastal_cities)):
        return "🌊"
    
    # Christmas period (December 20 - January 7)
    if (entry_date.month == 12 and entry_date.day >= 20) or (entry_date.month == 1 and entry_date.day <= 7):
        return "🎅"
    
    # Weekend vs weekday
    weekday = entry_date.weekday()
    if weekday >= 5:  # Saturday (5) or Sunday (6)
        return "🏡"
    else:
        return "👨‍💻"


def create_notion_entry(
    entry: DailyEntryInput,
    database_id: str,
    notion_token: str,
    location: str = "ljubljana"
) -> dict:
    """Create an entry, or patch supplied properties when its date exists."""
    matches = _find_entries_by_date(database_id, notion_token, entry.entry_date)
    if len(matches) > 1:
        raise RuntimeError(
            f"Multiple Notion entries found for {entry.entry_date}; "
            "refusing to update an arbitrary page"
        )
    if matches:
        return _update_notion_entry(matches[0], entry, notion_token)

    url = "https://api.notion.com/v1/pages"
    headers = _notion_headers(notion_token)
    
    # Get weather data for the entry date
    weather_data = get_weather_for_date(entry.entry_date, location)
    weather_summary = format_weather_summary(weather_data)
    
    # Determine emoji for the card
    emoji = determine_emoji(entry.entry_date, entry.general_notes, location)
    
    # Build properties payload
    properties = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": entry.entry_date.strftime("%A, %B %d, %Y")
                    }
                }
            ]
        },
        "Date": {
            "date": {
                "start": entry.entry_date.isoformat()
            }
        },
    }
    
    # Add optional select fields
    if entry.productivity:
        properties["Productivity"] = {"select": {"name": entry.productivity.value}}
    
    if entry.anxiety_status:
        properties["Anxiety Status"] = {"select": {"name": entry.anxiety_status.value}}
    
    if entry.physical_status:
        properties["Physical Status"] = {"select": {"name": entry.physical_status.value}}
    
    # Add number fields
    if entry.sleep_hrs is not None:
        properties["Sleep (hrs)"] = {"number": entry.sleep_hrs}
    
    if entry.weight_kg is not None:
        properties["Weight (kg)"] = {"number": entry.weight_kg}
    
    # Always send these fields (default 0)
    properties["Mindful (min)"] = {"number": entry.mindful_min}
    properties["Alcohol (unt)"] = {"number": entry.alcohol_unt}
    properties["Fasting"] = {"number": entry.fasting}
    properties["Cold (min)"] = {"number": entry.cold_min}
    
    if entry.coffee is not None:
        properties["Coffee (#)"] = {"number": entry.coffee}
    
    if entry.points is not None:
        properties["Points"] = {"number": entry.points}
    
    # Add rich text fields
    if entry.supplements:
        properties["Supplements"] = {
            "rich_text": [{"text": {"content": entry.supplements}}]
        }
    
    if entry.learned:
        properties["Learned"] = {
            "rich_text": [{"text": {"content": entry.learned}}]
        }
    
    if entry.general_notes:
        properties["General Notes"] = {
            "rich_text": [{"text": {"content": entry.general_notes}}]
        }
    
    if entry.substances:
        properties["Substances"] = {
            "rich_text": [{"text": {"content": entry.substances}}]
        }
    
    # Add weather as JSON string to Weather field
    if weather_data and weather_data.get("success"):
        import json
        weather_json = json.dumps({
            "location": weather_data.get("location"),
            "date": weather_data.get("date"),
            "temp_max": weather_data.get("temperature_max"),
            "temp_min": weather_data.get("temperature_min"),
            "precipitation": weather_data.get("precipitation"),
            "weather": weather_data.get("weather"),
            "wind_speed": weather_data.get("wind_speed")
        })
        properties["Weather"] = {
            "rich_text": [{"text": {"content": weather_json}}]
        }
    
    # Build the page content with weather
    children = []
    
    if weather_summary:
        # Add weather as a callout block
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": weather_summary}
                    }
                ],
                "icon": {"type": "emoji", "emoji": "🌤️"},
                "color": "blue_background"
            }
        })
    
    # Add notes if present
    if entry.general_notes:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": entry.general_notes}
                    }
                ]
            }
        })
    
    if entry.learned:
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "💡 Learned"}
                    }
                ]
            }
        })
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": entry.learned}
                    }
                ]
            }
        })
    
    payload = {
        "parent": {"database_id": database_id},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": properties,
    }
    
    # Add children blocks if any
    if children:
        payload["children"] = children
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if not response.ok:
        print(f"❌ Notion API Error: {response.status_code}")
        print(f"Response: {response.text}")
    response.raise_for_status()
    return {**response.json(), "_memobot_action": "created"}
