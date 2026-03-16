import os
from datetime import date, timedelta

from openai import OpenAI

from src.models import DailyEntryInput


def parse_daily_entry(message: str, api_key: str | None = None) -> DailyEntryInput:
    """
    Parse a natural language message into a structured DailyEntry using OpenAI.

    Args:
        message: User's natural language description of their day
        api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)

    Returns:
        DailyEntryInput: Parsed and structured daily log entry
    """
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    today = date.today()
    yesterday = today - timedelta(days=1)

    system_prompt = f"""You are a personal health and wellness tracker assistant. 
Your job is to parse natural language descriptions of daily activities into structured data.

IMPORTANT - Date handling:
- Today's date is: {today.isoformat()}
- Yesterday's date was: {yesterday.isoformat()}
- If the user says "yesterday", use {yesterday.isoformat()}
- If the user provides a specific date, use that exact date
- If no date is mentioned, use today's date: {today.isoformat()}

Extract the following information from the user's message:
- Productivity level (high/medium/low)
- Anxiety status (1-5 scale, where 1=calm, 5=very anxious)
- Physical status (good/ok/not so good/bad)
- Temperature feeling (scorching/hot/warm/perfect/normal/cold/freezing)
- Weather conditions (sunny/cloudy/rainy/etc.)
- Supplements taken
- Sleep hours
- Weight in kg
- Mindfulness/meditation minutes
- Alcohol units consumed
- Coffee cups/shots
- Fasting hours
- Cold exposure minutes (cold shower, ice bath)
- Whether they ate fish or meat
- Any substances used
- What they learned
- General notes about the day

Be intelligent about inferring information. For examples:
- "slept well" = ~8 hours sleep
- "anxious day" = anxiety_status: 4 or 5
- "great day" = productivity: high, physical_status: good
- "had my morning coffee" = coffee: 1
- "omega3 and vitamins" = supplements: [omega3, vit+min]

Leave fields as None/empty if not mentioned in the message."""

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        response_format=DailyEntryInput,
    )

    return completion.choices[0].message.parsed
