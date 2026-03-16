"""Daily entry models for input and database representation."""

from datetime import date, datetime
from pydantic import BaseModel

from .enums import (
    Productivity,
    AnxietyStatus,
    PhysicalStatus,
    Supplement,
)


class DailyEntryInput(BaseModel):
    """Model for creating new daily entries via OpenAI parsing."""
    entry_date: date
    productivity: Productivity | None = None
    anxiety_status: AnxietyStatus | None = None
    physical_status: PhysicalStatus | None = None
    supplements: list[Supplement] = []
    
    sleep_hrs: float | None = None
    weight_kg: float | None = None
    mindful_min: float = 0  # Default 0 if not mentioned
    alcohol_unt: float = 0  # Default 0 if not mentioned
    coffee: float | None = None
    fasting: float = 0  # Default 0 if not mentioned
    cold_min: float = 0  # Default 0 if not mentioned
    points: float | None = None
    
    fish: bool = False
    meat: bool = False
    
    learned: str | None = None
    general_notes: str | None = None
    substances: str | None = None


class DailyEntry(BaseModel):
    """Model for daily entries from Notion API."""
    id: str
    created_time: datetime
    last_edited_time: datetime
    emoji: str | None = None
    url: str
    
    # Properties
    name: str | None = None
    entry_date: date | None = None
    productivity: Productivity | None = None
    anxiety_status: AnxietyStatus | None = None
    physical_status: PhysicalStatus | None = None
    supplements: list[Supplement] = []
    
    sleep_hrs: float | None = None
    weight_kg: float | None = None
    mindful_min: float | None = None
    alcohol_unt: float | None = None
    coffee: float | None = None
    fasting: float | None = None
    cold_min: float | None = None
    points: float | None = None
    
    fish: bool = False
    meat: bool = False
    
    learned: str | None = None
    general_notes: str | None = None
    substances: str | None = None
    
    @classmethod
    def from_notion(cls, data: dict) -> "DailyEntry":
        """Parse Notion API response into DailyEntry model."""
        props = data["properties"]
        
        # Helper to get rich text content
        def get_rich_text(prop):
            if not prop.get("rich_text"):
                return None
            return "".join(t["plain_text"] for t in prop["rich_text"])
        
        # Helper to get title content
        def get_title(prop):
            if not prop.get("title"):
                return None
            return "".join(t["plain_text"] for t in prop["title"])
        
        return cls(
            id=data["id"],
            created_time=data["created_time"],
            last_edited_time=data["last_edited_time"],
            emoji=data.get("icon", {}).get("emoji") if data.get("icon") else None,
            url=data["url"],
            
            name=get_title(props["Name"]),
            entry_date=props["Date"]["date"]["start"] if props["Date"]["date"] else None,
            productivity=props["Productivity"]["select"]["name"] if props["Productivity"]["select"] else None,
            anxiety_status=props["Anxiety Status"]["select"]["name"] if props["Anxiety Status"]["select"] else None,
            physical_status=props["Physical Status"]["select"]["name"] if props["Physical Status"]["select"] else None,
            supplements=[s["name"] for s in props["Supplements"]["multi_select"]],
            
            sleep_hrs=props["Sleep (hrs)"]["number"],
            weight_kg=props["Weight (kg)"]["number"],
            mindful_min=props["Mindful (min)"]["number"],
            alcohol_unt=props["Alcohol (unt)"]["number"],
            coffee=props["Coffee (#)"]["number"],
            fasting=props["Fasting"]["number"],
            cold_min=props["Cold (min)"]["number"],
            points=props["Points"]["number"],
            
            fish=props["Fish"]["checkbox"],
            meat=props["Meat"]["checkbox"],
            
            learned=get_rich_text(props["Learned"]),
            general_notes=get_rich_text(props["General Notes"]),
            substances=get_rich_text(props["Substances"]),
        )
