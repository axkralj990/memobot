"""Weather API integration using Open-Meteo (free)."""

import requests
from datetime import date


# Location coordinates (can be extended)
LOCATIONS = {
    "ljubljana": {"lat": 46.0569, "lon": 14.5058},
    "london": {"lat": 51.5074, "lon": -0.1278},
    "new york": {"lat": 40.7128, "lon": -74.0060},
    "tokyo": {"lat": 35.6762, "lon": 139.6503},
}


def get_weather_for_date(target_date: date, location: str = "ljubljana") -> dict:
    """
    Get weather data for a specific date and location.
    
    Args:
        target_date: The date to get weather for
        location: City name (default: ljubljana)
    
    Returns:
        dict with weather data
    """
    location_lower = location.lower()
    
    if location_lower not in LOCATIONS:
        return {
            "success": False,
            "message": f"Location '{location}' not found. Available: {', '.join(LOCATIONS.keys())}"
        }
    
    coords = LOCATIONS[location_lower]
    
    # Open-Meteo API (free, no key needed)
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "start_date": target_date.isoformat(),
        "end_date": target_date.isoformat(),
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min", 
            "precipitation_sum",
            "weathercode",
            "windspeed_10m_max",
        ],
        "timezone": "Europe/Ljubljana" if location_lower == "ljubljana" else "auto"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        daily = data["daily"]
        
        # Weather code interpretation
        weather_code = daily["weathercode"][0]
        weather_desc = _interpret_weather_code(weather_code)
        
        return {
            "success": True,
            "location": location.title(),
            "date": target_date.isoformat(),
            "temperature_max": daily["temperature_2m_max"][0],
            "temperature_min": daily["temperature_2m_min"][0],
            "precipitation": daily["precipitation_sum"][0],
            "weather": weather_desc,
            "wind_speed": daily["windspeed_10m_max"][0],
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to fetch weather: {str(e)}"
        }


def _interpret_weather_code(code: int) -> str:
    """Interpret WMO weather code."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return codes.get(code, f"Unknown ({code})")


def format_weather_summary(weather_data: dict) -> str:
    """Format weather data into a nice summary string."""
    if not weather_data.get("success"):
        return ""
    
    temp_max = weather_data["temperature_max"]
    temp_min = weather_data["temperature_min"]
    weather = weather_data["weather"]
    precip = weather_data["precipitation"]
    wind = weather_data["wind_speed"]
    location = weather_data["location"]
    
    summary = f"📍 **{location}**\n"
    summary += f"🌡️ {temp_min:.1f}°C - {temp_max:.1f}°C\n"
    summary += f"☁️ {weather}\n"
    
    if precip > 0:
        summary += f"🌧️ {precip:.1f}mm precipitation\n"
    
    if wind > 20:
        summary += f"💨 {wind:.0f} km/h wind\n"
    
    return summary
