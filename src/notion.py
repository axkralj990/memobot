"""
Notion API integration module.

This module re-exports tools from the tools package for backwards compatibility.
"""

from src.tools import create_notion_entry, get_notion_entry, query_daily_entries

__all__ = ["create_notion_entry", "get_notion_entry", "query_daily_entries"]
