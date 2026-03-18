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
    },
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Create a new event on Google Calendar. Use when user wants to book, schedule, or add an appointment/event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Event title/name"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Event start time in ISO 8601 format (e.g., '2026-03-19T14:00:00')"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "Event end time in ISO 8601 format (e.g., '2026-03-19T15:00:00')"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional event description or notes"
                    },
                    "location": {
                        "type": "string",
                        "description": "Optional event location"
                    }
                },
                "required": ["summary", "start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_calendar_events",
            "description": "List events from Google Calendar within a date range. Use when user asks what's on their calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in ISO format (e.g., '2026-03-19')"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Optional end date in ISO format. If not provided, defaults to 7 days from start_date"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of events to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["start_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_free_slots",
            "description": "Find available time slots on a specific date. Use when user asks for free time or when to schedule something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date to check in ISO format (e.g., '2026-03-19')"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Required slot duration in minutes (default: 30)",
                        "default": 30
                    },
                    "working_hours_start": {
                        "type": "integer",
                        "description": "Start of working hours (0-23, default: 9)",
                        "default": 9
                    },
                    "working_hours_end": {
                        "type": "integer",
                        "description": "End of working hours (0-23, default: 18)",
                        "default": 18
                    }
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_calendar_event",
            "description": "Delete an event from Google Calendar. Use when user wants to cancel or remove an event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to delete (obtained from list_calendar_events)"
                    }
                },
                "required": ["event_id"]
            }
        }
    }
]

