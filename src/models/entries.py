"""Daily entry models for input and database representation."""

from datetime import date, datetime
from pydantic import BaseModel

from .enums import (
    Productivity,
    AnxietyStatus,
    PhysicalStatus,
)


class DailyEntryInput(BaseModel):
    """Model for creating new daily entries via OpenAI parsing."""
    entry_date: date
    productivity: Productivity | None = None
    anxiety_status: AnxietyStatus | None = None
    physical_status: PhysicalStatus | None = None
    supplements: str | None = None
    
    sleep_hrs: float | None = None
    weight_kg: float | None = None
    mindful_min: float = 0  # Default 0 if not mentioned
    alcohol_unt: float = 0  # Default 0 if not mentioned
    coffee: float | None = None
    fasting: float = 0  # Default 0 if not mentioned
    cold_min: float = 0  # Default 0 if not mentioned
    points: float | None = None
    
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
    supplements: str | None = None
    
    sleep_hrs: float | None = None
    weight_kg: float | None = None
    mindful_min: float | None = None
    alcohol_unt: float | None = None
    coffee: float | None = None
    fasting: float | None = None
    cold_min: float | None = None
    points: float | None = None
    
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
            entry_date=props["Date"]["date"]["start"] if props.get("Date", {}).get("date") else None,
            productivity=props.get("Productivity", {}).get("select", {}).get("name") if props.get("Productivity", {}).get("select") else None,
            anxiety_status=props.get("Anxiety Status", {}).get("select", {}).get("name") if props.get("Anxiety Status", {}).get("select") else None,
            physical_status=props.get("Physical Status", {}).get("select", {}).get("name") if props.get("Physical Status", {}).get("select") else None,
            supplements=get_rich_text(props.get("Supplements", {})),
            
            sleep_hrs=props.get("Sleep (hrs)", {}).get("number"),
            weight_kg=props.get("Weight (kg)", {}).get("number"),
            mindful_min=props.get("Mindful (min)", {}).get("number"),
            alcohol_unt=props.get("Alcohol (unt)", {}).get("number"),
            coffee=props.get("Coffee (#)", {}).get("number"),
            fasting=props.get("Fasting", {}).get("number"),
            cold_min=props.get("Cold (min)", {}).get("number"),
            points=props.get("Points", {}).get("number"),
            
            learned=get_rich_text(props.get("Learned", {})),
            general_notes=get_rich_text(props.get("General Notes", {})),
            substances=get_rich_text(props.get("Substances", {})),
        )
