from datetime import date
from unittest.mock import Mock, patch

import pytest

from src.models import DailyEntryInput
from src.tools.create_tools import create_notion_entry


def notion_response(payload):
    response = Mock()
    response.json.return_value = payload
    response.ok = True
    return response


@patch("src.tools.create_tools.get_weather_for_date")
@patch("src.tools.create_tools.requests.patch")
@patch("src.tools.create_tools.requests.post")
def test_existing_date_updates_only_supplied_properties(
    mock_post,
    mock_patch,
    mock_weather,
):
    existing_page = {"id": "page-123", "url": "https://notion.so/page-123"}
    mock_post.return_value = notion_response({"results": [existing_page]})
    mock_patch.return_value = notion_response(existing_page)
    entry = DailyEntryInput.model_validate(
        {
            "entry_date": "2026-10-31",
            "sleep_hrs": 8,
            "mindful_min": None,
        }
    )

    result = create_notion_entry(entry, "database-id", "token")

    assert result["_memobot_action"] == "updated"
    mock_patch.assert_called_once_with(
        "https://api.notion.com/v1/pages/page-123",
        headers={
            "Authorization": "Bearer token",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        json={"properties": {"Sleep (hrs)": {"number": 8.0}}},
        timeout=30,
    )
    mock_weather.assert_not_called()


@patch("src.tools.create_tools.requests.patch")
@patch("src.tools.create_tools.requests.post")
def test_existing_general_notes_are_appended(mock_post, mock_patch):
    existing_page = {
        "id": "page-123",
        "url": "https://notion.so/page-123",
        "properties": {
            "General Notes": {
                "rich_text": [{"plain_text": "Original description."}]
            }
        },
    }
    mock_post.return_value = notion_response({"results": [existing_page]})
    mock_patch.return_value = notion_response(existing_page)
    entry = DailyEntryInput(
        entry_date=date(2026, 10, 31),
        general_notes="Additional thought.",
    )

    create_notion_entry(entry, "database-id", "token")

    update_payload = mock_patch.call_args.kwargs["json"]
    assert update_payload["properties"]["General Notes"] == {
        "rich_text": [
            {
                "text": {
                    "content": "Original description.\n\nAdditional thought."
                }
            }
        ]
    }


@patch("src.tools.create_tools.requests.patch")
@patch("src.tools.create_tools.requests.post")
def test_duplicate_dates_are_not_updated(mock_post, mock_patch):
    mock_post.return_value = notion_response(
        {
            "results": [
                {"id": "page-1", "url": "https://notion.so/page-1"},
                {"id": "page-2", "url": "https://notion.so/page-2"},
            ]
        }
    )
    entry = DailyEntryInput(entry_date=date(2026, 10, 31), sleep_hrs=8)

    with pytest.raises(RuntimeError, match="Multiple Notion entries found"):
        create_notion_entry(entry, "database-id", "token")

    mock_patch.assert_not_called()


@patch("src.tools.create_tools.format_weather_summary", return_value=None)
@patch("src.tools.create_tools.get_weather_for_date", return_value=None)
@patch("src.tools.create_tools.requests.post")
def test_missing_date_creates_new_page(mock_post, _mock_weather, _mock_summary):
    created_page = {"id": "page-new", "url": "https://notion.so/page-new"}
    mock_post.side_effect = [
        notion_response({"results": []}),
        notion_response(created_page),
    ]
    entry = DailyEntryInput(entry_date=date(2026, 10, 31), sleep_hrs=8)

    result = create_notion_entry(entry, "database-id", "token")

    assert result["_memobot_action"] == "created"
    create_payload = mock_post.call_args_list[1].kwargs["json"]
    assert create_payload["properties"]["Sleep (hrs)"] == {"number": 8.0}
    assert create_payload["properties"]["Mindful (min)"] == {"number": 0.0}
    assert "children" not in create_payload
