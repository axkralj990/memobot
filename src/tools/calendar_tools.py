"""Google Calendar integration for booking and managing events."""

import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required for calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar']

# File paths for credentials
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"


def get_credentials():
    """Get or refresh Google Calendar API credentials."""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"{CREDENTIALS_FILE} not found. Please download it from Google Cloud Console.\n"
                    "See docs/CALENDAR_INTEGRATION.md for setup instructions."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next time
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_calendar_service():
    """Get authenticated Google Calendar service."""
    creds = get_credentials()
    return build('calendar', 'v3', credentials=creds)


def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str | None = None,
    location: str | None = None,
    calendar_id: str = "primary"
):
    """
    Create a new calendar event.
    
    Args:
        summary: Event title
        start_time: Start time in ISO format (e.g., "2026-03-19T14:00:00")
        end_time: End time in ISO format
        description: Optional event description
        location: Optional event location
        calendar_id: Calendar ID (default: "primary")
    
    Returns:
        dict with event details
    """
    try:
        service = get_calendar_service()
        
        # Get timezone from environment or default to Ljubljana
        timezone = os.getenv("TIMEZONE", "Europe/Ljubljana")
        
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            },
        }
        
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        
        result = service.events().insert(calendarId=calendar_id, body=event).execute()
        
        return {
            "success": True,
            "event_id": result['id'],
            "summary": summary,
            "start": start_time,
            "end": end_time,
            "link": result.get('htmlLink'),
            "message": f"✅ Created event '{summary}' from {start_time} to {end_time}"
        }
    
    except HttpError as error:
        return {
            "success": False,
            "error": str(error),
            "message": f"❌ Failed to create event: {error}"
        }


def list_calendar_events(
    start_date: str,
    end_date: str | None = None,
    max_results: int = 10,
    calendar_id: str = "primary"
):
    """
    List calendar events in a date range.
    
    Args:
        start_date: Start date in ISO format (e.g., "2026-03-19")
        end_date: Optional end date in ISO format (defaults to start_date + 7 days)
        max_results: Maximum number of events to return
        calendar_id: Calendar ID (default: "primary")
    
    Returns:
        dict with list of events
    """
    try:
        service = get_calendar_service()
        
        # Parse start date and calculate end date if not provided
        start_dt = datetime.fromisoformat(start_date)
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
        else:
            end_dt = start_dt + timedelta(days=7)
        
        # Convert to RFC3339 format
        time_min = start_dt.isoformat() + 'Z'
        time_max = end_dt.isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return {
                "success": True,
                "events": [],
                "count": 0,
                "message": f"📅 No events found between {start_date} and {end_dt.date()}"
            }
        
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_list.append({
                "id": event['id'],
                "summary": event.get('summary', 'No title'),
                "start": start,
                "end": event['end'].get('dateTime', event['end'].get('date')),
                "location": event.get('location'),
                "description": event.get('description'),
                "link": event.get('htmlLink')
            })
        
        return {
            "success": True,
            "events": event_list,
            "count": len(event_list),
            "message": f"📅 Found {len(event_list)} event(s)"
        }
    
    except HttpError as error:
        return {
            "success": False,
            "error": str(error),
            "message": f"❌ Failed to list events: {error}"
        }


def delete_calendar_event(event_id: str, calendar_id: str = "primary"):
    """
    Delete a calendar event.
    
    Args:
        event_id: Event ID to delete
        calendar_id: Calendar ID (default: "primary")
    
    Returns:
        dict with deletion status
    """
    try:
        service = get_calendar_service()
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        
        return {
            "success": True,
            "event_id": event_id,
            "message": f"✅ Deleted event {event_id}"
        }
    
    except HttpError as error:
        return {
            "success": False,
            "error": str(error),
            "message": f"❌ Failed to delete event: {error}"
        }


def find_free_slots(
    date: str,
    duration_minutes: int = 30,
    working_hours_start: int = 9,
    working_hours_end: int = 18,
    calendar_id: str = "primary"
):
    """
    Find free time slots on a given date.
    
    Args:
        date: Date in ISO format (e.g., "2026-03-19")
        duration_minutes: Desired slot duration in minutes
        working_hours_start: Start of working hours (default: 9)
        working_hours_end: End of working hours (default: 18)
        calendar_id: Calendar ID (default: "primary")
    
    Returns:
        dict with list of free slots
    """
    try:
        service = get_calendar_service()
        
        # Parse date and set time boundaries
        target_date = datetime.fromisoformat(date)
        day_start = target_date.replace(hour=working_hours_start, minute=0, second=0)
        day_end = target_date.replace(hour=working_hours_end, minute=0, second=0)
        
        # Get busy times
        body = {
            "timeMin": day_start.isoformat() + 'Z',
            "timeMax": day_end.isoformat() + 'Z',
            "items": [{"id": calendar_id}]
        }
        
        freebusy_result = service.freebusy().query(body=body).execute()
        busy_times = freebusy_result['calendars'][calendar_id]['busy']
        
        # Calculate free slots
        free_slots = []
        current_time = day_start
        
        for busy in busy_times:
            busy_start = datetime.fromisoformat(busy['start'].replace('Z', ''))
            busy_end = datetime.fromisoformat(busy['end'].replace('Z', ''))
            
            # Check if there's a free slot before this busy period
            if (busy_start - current_time).total_seconds() >= duration_minutes * 60:
                free_slots.append({
                    "start": current_time.isoformat(),
                    "end": busy_start.isoformat(),
                    "duration_minutes": int((busy_start - current_time).total_seconds() / 60)
                })
            
            current_time = max(current_time, busy_end)
        
        # Check if there's time left at the end of the day
        if (day_end - current_time).total_seconds() >= duration_minutes * 60:
            free_slots.append({
                "start": current_time.isoformat(),
                "end": day_end.isoformat(),
                "duration_minutes": int((day_end - current_time).total_seconds() / 60)
            })
        
        if not free_slots:
            return {
                "success": True,
                "slots": [],
                "count": 0,
                "message": f"🔍 No free slots of {duration_minutes} minutes found on {date}"
            }
        
        return {
            "success": True,
            "slots": free_slots,
            "count": len(free_slots),
            "message": f"🔍 Found {len(free_slots)} free slot(s) on {date}"
        }
    
    except HttpError as error:
        return {
            "success": False,
            "error": str(error),
            "message": f"❌ Failed to find free slots: {error}"
        }
