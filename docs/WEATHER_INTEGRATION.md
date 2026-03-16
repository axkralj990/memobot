# 🌤️ Weather Integration

## Overview

Every daily entry automatically includes weather data from [Open-Meteo](https://open-meteo.com/), a free weather API that requires no authentication.

## Features

- **Automatic**: Weather is fetched automatically for each entry
- **Location-aware**: Defaults to Ljubljana, but can detect other cities from your message
- **Historical data**: Works for past dates (up to 92 days back)
- **Rich formatting**: Displayed as a blue callout block in Notion with emoji indicators

## How It Works

When you create a daily entry, the system:

1. Extracts the date from your message (today, yesterday, or specific date)
2. Determines location (default: Ljubljana, or extracted from message)
3. Calls Open-Meteo API to fetch weather for that date
4. Formats the data with temperature, conditions, precipitation, and wind
5. Adds it as a callout block at the top of your Notion page

## Weather Data Included

- 📍 **Location** (city name)
- 🌡️ **Temperature** (min-max range in Celsius)
- ☁️ **Weather condition** (clear, cloudy, rain, snow, etc.)
- 🌧️ **Precipitation** (in mm, if > 0)
- 💨 **Wind speed** (in km/h, if > 20)

## Example Output

When you send: `"Yesterday I slept 7 hours and had 2 coffees"`

Your Notion page will include:

```
┌─────────────────────────────────────────┐
│ 🌤️                                      │
│ 📍 Ljubljana                            │
│ 🌡️ 4.1°C - 15.9°C                       │
│ ☁️ Moderate rain                        │
│ 🌧️ 7.5mm precipitation                  │
└─────────────────────────────────────────┘
```

## Supported Locations

Pre-configured cities:
- **Ljubljana** (default) - 46.0569°N, 14.5058°E
- **London** - 51.5074°N, 0.1278°W
- **New York** - 40.7128°N, 74.0060°W
- **Tokyo** - 35.6762°N, 139.6503°E

### Adding More Locations

Edit `src/tools/weather_tools.py` and add to the `LOCATIONS` dictionary:

```python
LOCATIONS = {
    "ljubljana": {"lat": 46.0569, "lon": 14.5058},
    "paris": {"lat": 48.8566, "lon": 2.3522},  # Add your city
}
```

## Agent Behavior

The AI agent automatically handles location:

```
"I slept 8 hours" → Uses Ljubljana (default)
"I'm in Berlin, slept 8 hours" → Would use Berlin if configured
"Today in London: slept well" → Uses London (pre-configured)
```

## API Details

- **Provider**: Open-Meteo (https://open-meteo.com)
- **Cost**: Free, no API key needed
- **Rate limits**: Generous free tier
- **Data range**: Up to 92 days of historical data
- **Update frequency**: Daily

## Technical Implementation

### Files
- `src/tools/weather_tools.py` - Weather API integration
- `src/tools/create_tools.py` - Integrates weather into Notion pages

### Key Functions
- `get_weather_for_date(date, location)` - Fetches weather data
- `format_weather_summary(weather_data)` - Formats for display
- `create_notion_entry()` - Includes weather in page creation

### Error Handling

If weather fetch fails (network error, invalid location):
- Entry is still created successfully
- Weather block is simply omitted
- No error shown to user

## Testing

Test the weather integration:

```bash
# Test weather fetching
uv run python test_weather.py

# Test multiple cities
uv run python -c "
from src.tools.weather_tools import get_weather_for_date, format_weather_summary
from datetime import date

for city in ['ljubljana', 'london', 'tokyo']:
    weather = get_weather_for_date(date.today(), city)
    print(format_weather_summary(weather))
"
```

## Future Enhancements

Potential improvements:
- Add weather to query responses ("How was weather yesterday?")
- Weather-based insights ("You sleep better on rainy days")
- Forecast for planning ("Tomorrow looks sunny!")
- More detailed metrics (humidity, UV index, etc.)
