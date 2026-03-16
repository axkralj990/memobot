"""Tool definitions for the AI agent."""

AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_daily_entry",
            "description": "Create a new daily log entry in Notion with weather data. Weather defaults to Ljubljana unless user mentions another location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "entry_data": {
                        "type": "object",
                        "description": "The structured daily entry data",
                        "properties": {
                            "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                            "location": {"type": "string", "description": "City for weather (default: ljubljana)"},
                            "productivity": {"type": "string", "enum": ["high", "medium", "low"]},
                            "anxiety_status": {"type": "string", "enum": ["1", "2", "3", "4", "5"]},
                            "physical_status": {"type": "string", "enum": ["good", "ok", "not so good", "bad"]},
                            "sleep_hrs": {"type": "number"},
                            "coffee": {"type": "number"},
                            "weight_kg": {"type": "number"},
                            "mindful_min": {"type": "number", "description": "Mindfulness/meditation minutes. Default 0 if not mentioned."},
                            "alcohol_unt": {"type": "number", "description": "Alcohol units. Default 0 if not mentioned."},
                            "fasting": {"type": "number", "description": "Fasting hours. Default 0 if not mentioned."},
                            "cold_min": {"type": "number", "description": "Cold exposure in minutes. Default 0 if not mentioned. Set to 1 if mentioned without specific time."},
                            "fish": {"type": "boolean"},
                            "meat": {"type": "boolean"},
                            "supplements": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": ["proteins", "creatine", "collagen", "omega3", "vit+min", "bcaa", "zinc", "Mg+Theanine", "ashwagandha"]
                                },
                                "description": "List of supplements taken. Use 'vit+min' for vitamins"
                            },
                            "learned": {
                                "type": "string",
                                "description": "ONLY fill if user EXPLICITLY says 'I learned', 'discovered', 'TIL', etc. Leave empty if not explicitly mentioned."
                            },
                            "general_notes": {
                                "type": "string",
                                "description": "Summary of the entire day including workout details, activities, and anything that doesn't fit into specific fields"
                            },
                            "substances": {"type": "string"},
                        },
                        "required": ["date"]
                    }
                },
                "required": ["entry_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_daily_entries",
            "description": "Query and retrieve daily log entries from Notion. Use this when the user asks about a specific date or wants to see their past data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_date": {
                        "type": "string",
                        "description": "The date to query in YYYY-MM-DD format"
                    },
                    "num_entries": {
                        "type": "integer",
                        "description": "Number of entries to retrieve",
                        "default": 1
                    }
                },
                "required": ["target_date"]
            }
        }
    }
]
