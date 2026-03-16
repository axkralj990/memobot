"""
Agentic Daily Log Assistant

This module implements an AI agent that can:
1. Determine user intent (create entry, read entry, query data)
2. Use tools to interact with Notion
3. Provide intelligent, contextual responses
"""

import os
import json
from openai import OpenAI

from src.models import DailyEntryInput
from src.tools import create_notion_entry, query_daily_entries
from src.agent_tools import AGENT_TOOLS
from src.agent_prompt import get_system_prompt


class DailyLogAgent:
    """An AI agent for managing daily log entries."""
    
    def __init__(self, notion_db_id: str, notion_token: str, openai_api_key: str | None = None):
        self.client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))
        self.notion_db_id = notion_db_id
        self.notion_token = notion_token
        self.tools = AGENT_TOOLS
    
    def _create_daily_entry(self, entry_data: dict) -> dict:
        """Tool: Create a daily entry in Notion."""
        # Convert 'date' to 'entry_date' if needed (OpenAI sends 'date')
        if "date" in entry_data and "entry_date" not in entry_data:
            entry_data["entry_date"] = entry_data.pop("date")
        
        entry = DailyEntryInput.model_validate(entry_data)
        
        # Default location to Ljubljana unless specified
        location = entry_data.get("location", "ljubljana")
        
        result = create_notion_entry(
            entry, 
            self.notion_db_id, 
            self.notion_token,
            location=location
        )
        return {
            "success": True,
            "url": result["url"],
            "date": entry.entry_date.isoformat(),
            "message": f"Entry created for {entry.entry_date} with weather data"
        }
    
    def _query_daily_entries(self, target_date: str, num_entries: int = 1) -> dict:
        """Tool: Query daily entries from Notion."""
        return query_daily_entries(
            self.notion_db_id,
            self.notion_token,
            target_date,
            num_entries
        )
    
    def process_message(self, user_message: str) -> str:
        """
        Process a user message using agentic reasoning.
        The agent will determine intent and use appropriate tools.
        """
        system_prompt = get_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Agent loop: keep going until the agent responds without tool calls
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            # If no tool calls, we're done
            if not assistant_message.tool_calls:
                return assistant_message.content
            
            # Execute tool calls
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Agent using tool: {function_name}")
                print(f"   Args: {function_args}")
                
                # Execute the tool
                if function_name == "create_daily_entry":
                    result = self._create_daily_entry(function_args["entry_data"])
                elif function_name == "query_daily_entries":
                    result = self._query_daily_entries(**function_args)
                else:
                    result = {"error": "Unknown function"}
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        
        return "I apologize, but I'm having trouble processing your request. Please try again."
