#!/usr/bin/env python3
"""Test Google Calendar integration."""

from datetime import datetime, timedelta
from src.tools.calendar_tools import (
    create_calendar_event,
    list_calendar_events,
    find_free_slots,
    delete_calendar_event
)


def test_calendar_integration():
    """Test all calendar functions."""
    print("🧪 Testing Google Calendar Integration\n")
    print("=" * 60)
    
    # Test 1: Create a test event
    print("\n1️⃣  Creating test event...")
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    start_time = f"{tomorrow}T14:00:00"
    end_time = f"{tomorrow}T15:00:00"
    
    result = create_calendar_event(
        summary="Test Event - memobot",
        start_time=start_time,
        end_time=end_time,
        description="This is a test event created by memobot. Safe to delete.",
        location="Test Location"
    )
    
    if result["success"]:
        print(f"✅ {result['message']}")
        print(f"   Event ID: {result['event_id']}")
        print(f"   Link: {result['link']}")
        event_id = result["event_id"]
    else:
        print(f"❌ {result['message']}")
        return
    
    # Test 2: List events
    print("\n2️⃣  Listing events for tomorrow...")
    result = list_calendar_events(
        start_date=str(tomorrow),
        end_date=str(tomorrow + timedelta(days=1))
    )
    
    if result["success"]:
        print(f"✅ {result['message']}")
        for event in result["events"]:
            print(f"   - {event['summary']} at {event['start']}")
    else:
        print(f"❌ {result['message']}")
    
    # Test 3: Find free slots
    print("\n3️⃣  Finding free slots tomorrow...")
    result = find_free_slots(
        date=str(tomorrow),
        duration_minutes=30
    )
    
    if result["success"]:
        print(f"✅ {result['message']}")
        for slot in result["slots"][:5]:  # Show first 5 slots
            start = datetime.fromisoformat(slot["start"])
            end = datetime.fromisoformat(slot["end"])
            print(f"   - {start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({slot['duration_minutes']} min)")
    else:
        print(f"❌ {result['message']}")
    
    # Test 4: Delete the test event
    print("\n4️⃣  Cleaning up - deleting test event...")
    result = delete_calendar_event(event_id)
    
    if result["success"]:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
    
    print("\n" + "=" * 60)
    print("🎉 Calendar integration test complete!\n")


if __name__ == "__main__":
    try:
        test_calendar_integration()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📖 Please follow the setup instructions in docs/CALENDAR_INTEGRATION.md")
        print("   Key steps:")
        print("   1. Enable Google Calendar API in Google Cloud Console")
        print("   2. Download credentials.json")
        print("   3. Place it in the project root directory")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
