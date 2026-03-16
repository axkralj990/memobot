# Extending the Agent - Examples 🛠️

This guide shows you how to add new capabilities to your agent by adding tools.

## Example 1: Add Weekly Summary Tool

```python
# In src/agent.py, add to self.tools:

{
    "type": "function",
    "function": {
        "name": "get_weekly_summary",
        "description": "Get a summary of the user's week including averages for sleep, coffee, anxiety, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "week_start_date": {
                    "type": "string",
                    "description": "Start date of the week in YYYY-MM-DD format"
                }
            },
            "required": ["week_start_date"]
        }
    }
}

# Then implement the function:

def get_weekly_summary(self, week_start_date: str) -> dict:
    """Tool: Get weekly summary statistics."""
    from datetime import datetime, timedelta
    import requests
    
    start = datetime.fromisoformat(week_start_date).date()
    end = start + timedelta(days=7)
    
    # Query Notion for the week
    url = f"https://api.notion.com/v1/databases/{self.notion_db_id}/query"
    headers = {
        "Authorization": f"Bearer {self.notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    
    payload = {
        "filter": {
            "and": [
                {"property": "Date", "date": {"on_or_after": start.isoformat()}},
                {"property": "Date", "date": {"before": end.isoformat()}}
            ]
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json()["results"]
    
    # Calculate averages
    sleep_total = 0
    coffee_total = 0
    entries_count = len(results)
    
    for result in results:
        props = result["properties"]
        sleep_total += props.get("Sleep (hrs)", {}).get("number", 0) or 0
        coffee_total += props.get("Coffee (#)", {}).get("number", 0) or 0
    
    return {
        "success": True,
        "week_start": start.isoformat(),
        "entries_count": entries_count,
        "avg_sleep": round(sleep_total / entries_count, 1) if entries_count > 0 else 0,
        "avg_coffee": round(coffee_total / entries_count, 1) if entries_count > 0 else 0,
    }

# Add to the execute tool section in process_message():

elif function_name == "get_weekly_summary":
    result = self.get_weekly_summary(**function_args)
```

**Now you can ask:**
```
"Summarize this week"
"How did I do last week?"
```

## Example 2: Add Comparison Tool

```python
{
    "type": "function",
    "function": {
        "name": "compare_two_days",
        "description": "Compare metrics between two specific dates",
        "parameters": {
            "type": "object",
            "properties": {
                "date1": {"type": "string", "description": "First date YYYY-MM-DD"},
                "date2": {"type": "string", "description": "Second date YYYY-MM-DD"}
            },
            "required": ["date1", "date2"]
        }
    }
}

def compare_two_days(self, date1: str, date2: str) -> dict:
    """Tool: Compare two days side by side."""
    entry1 = self.query_daily_entries(date1)
    entry2 = self.query_daily_entries(date2)
    
    if not entry1["success"] or not entry2["success"]:
        return {"success": False, "message": "One or both dates not found"}
    
    return {
        "success": True,
        "date1": date1,
        "date2": date2,
        "entry1": entry1["entry"],
        "entry2": entry2["entry"],
        "differences": {
            "sleep_diff": entry1["entry"]["sleep_hrs"] - entry2["entry"]["sleep_hrs"],
            "anxiety_diff": int(entry1["entry"]["anxiety_status"] or 0) - int(entry2["entry"]["anxiety_status"] or 0),
        }
    }

# Add to execute section:
elif function_name == "compare_two_days":
    result = self.compare_two_days(**function_args)
```

**Now you can ask:**
```
"Compare yesterday to last Monday"
"How does today compare to March 1st?"
```

## Example 3: Add Trend Analysis

```python
{
    "type": "function",
    "function": {
        "name": "analyze_sleep_trend",
        "description": "Analyze sleep patterns over the last N days",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "Number of days to analyze",
                    "default": 7
                }
            }
        }
    }
}

def analyze_sleep_trend(self, days: int = 7) -> dict:
    """Tool: Analyze sleep trends."""
    from datetime import date, timedelta
    import requests
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Query entries
    url = f"https://api.notion.com/v1/databases/{self.notion_db_id}/query"
    headers = {
        "Authorization": f"Bearer {self.notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    
    payload = {
        "filter": {
            "and": [
                {"property": "Date", "date": {"on_or_after": start_date.isoformat()}},
                {"property": "Date", "date": {"on_or_before": end_date.isoformat()}}
            ]
        },
        "sorts": [{"property": "Date", "direction": "ascending"}]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json()["results"]
    
    # Analyze
    sleep_values = []
    for result in results:
        sleep = result["properties"].get("Sleep (hrs)", {}).get("number")
        if sleep:
            sleep_values.append(sleep)
    
    if not sleep_values:
        return {"success": False, "message": "No sleep data found"}
    
    avg_sleep = sum(sleep_values) / len(sleep_values)
    trend = "improving" if sleep_values[-1] > avg_sleep else "declining"
    
    return {
        "success": True,
        "days_analyzed": len(sleep_values),
        "average_sleep": round(avg_sleep, 1),
        "min_sleep": min(sleep_values),
        "max_sleep": max(sleep_values),
        "trend": trend,
        "sleep_data": sleep_values
    }

# Add to execute section:
elif function_name == "analyze_sleep_trend":
    result = self.analyze_sleep_trend(**function_args)
```

**Now you can ask:**
```
"How's my sleep been?"
"Analyze my sleep over the last 2 weeks"
"Am I sleeping better or worse?"
```

## Example 4: Add Goal Checking

```python
{
    "type": "function",
    "function": {
        "name": "check_goals",
        "description": "Check if user is meeting their health goals",
        "parameters": {
            "type": "object",
            "properties": {
                "goal_type": {
                    "type": "string",
                    "enum": ["sleep", "coffee", "exercise", "all"],
                    "description": "Which goal to check"
                }
            }
        }
    }
}

def check_goals(self, goal_type: str = "all") -> dict:
    """Tool: Check if goals are being met."""
    # Define goals
    goals = {
        "sleep": {"target": 8, "min": 7, "max": 9},
        "coffee": {"target": 2, "max": 3},
        "exercise": {"target": 30, "min": 20}
    }
    
    # Get recent data (last 7 days)
    summary = self.get_weekly_summary(
        (date.today() - timedelta(days=7)).isoformat()
    )
    
    results = {}
    
    if goal_type in ["sleep", "all"]:
        avg_sleep = summary["avg_sleep"]
        sleep_goal = goals["sleep"]
        results["sleep"] = {
            "goal": sleep_goal["target"],
            "actual": avg_sleep,
            "met": sleep_goal["min"] <= avg_sleep <= sleep_goal["max"]
        }
    
    if goal_type in ["coffee", "all"]:
        avg_coffee = summary["avg_coffee"]
        coffee_goal = goals["coffee"]
        results["coffee"] = {
            "goal": coffee_goal["target"],
            "actual": avg_coffee,
            "met": avg_coffee <= coffee_goal["max"]
        }
    
    return {
        "success": True,
        "results": results
    }

# Add to execute section:
elif function_name == "check_goals":
    result = self.check_goals(**function_args)
```

**Now you can ask:**
```
"Am I meeting my goals?"
"How am I doing on sleep?"
"Check my coffee goal"
```

## Tips for Adding Tools

1. **Clear descriptions** - The AI reads them to decide when to use the tool
2. **Structured returns** - Return dicts with consistent format
3. **Error handling** - Return `{"success": False, "message": "..."}` on errors
4. **Type hints** - Help with debugging and IDE support
5. **Keep focused** - One tool = one responsibility

## Testing New Tools

```bash
# Test locally first
uv run test_agent.py

# Try prompts that should trigger your new tool
> "Summarize this week"
> "Compare yesterday to last Monday"
> "Check my goals"
```

## Advanced: Multi-Tool Chains

The agent can use multiple tools in sequence!

**Example:**
```
You: "Compare my sleep this week to last week"

Agent:
  1. Uses get_weekly_summary for this week
  2. Uses get_weekly_summary for last week
  3. Synthesizes comparison
  4. Responds with insights
```

No extra code needed - the agent figures it out! 🤯

## Your Turn!

What tools will you add?
- Mood tracking analysis?
- Exercise correlation?
- Weather impact on mood?
- Supplement effectiveness?
- Social activity tracking?

The possibilities are endless! 🚀
