# Google Calendar Integration 📅

memobot now supports natural language calendar management! Book appointments, check your schedule, and find free time slots—all through Discord.

## Features

- ✅ **Create Events** - "Book dentist tomorrow at 2pm for 1 hour"
- 📋 **List Events** - "What's on my calendar this week?"
- 🔍 **Find Free Slots** - "When am I free tomorrow afternoon?"
- ❌ **Delete Events** - "Cancel my gym session on Friday"
- 🤖 **AI-Powered** - Natural language understanding, intelligent date parsing

## Setup

### 1. Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google Calendar API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

### 2. Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **External** (for personal use)
   - App name: "memobot" (or your choice)
   - User support email: your email
   - Developer contact: your email
   - Scopes: None needed for now
   - Test users: Add your Gmail address
   - Click "Save and Continue"
4. Back to Create Credentials:
   - Application type: **Desktop app**
   - Name: "memobot-desktop"
   - Click "Create"
5. **Download JSON** - Click download icon
6. Save as `credentials.json` in your project root

### 3. First-Time Authorization

When you first use a calendar feature, memobot will:
1. Open a browser window
2. Ask you to log in with Google
3. Request permission to manage your calendar
4. Save credentials to `token.pickle` (auto-refreshes)

**Important**: This only happens once! The token is saved locally.

### 4. Update Environment (Optional)

In `.env`, add your timezone:
```bash
TIMEZONE=Europe/Ljubljana
```

Default is `Europe/Ljubljana` if not set.

## Usage Examples

### Creating Events

```
You: Book a dentist appointment tomorrow at 2pm for 1 hour
Bot: ✅ Created event 'Dentist appointment' on March 19, 2026 at 14:00

You: Schedule team meeting next Monday 10am to 11am
Bot: ✅ Created event 'Team meeting' on March 24, 2026 at 10:00

You: Add gym session Friday 6pm, location: FitGym, 90 minutes
Bot: ✅ Created event 'Gym session' on March 21, 2026 at 18:00
     Location: FitGym
```

**Natural language features:**
- Relative dates: "tomorrow", "next Monday", "Friday"
- Time formats: "2pm", "14:00", "2:30pm"
- Duration inference: If not specified, uses defaults
  - Appointments: 30 minutes
  - Meetings: 1 hour
  - Custom: Specify explicitly

### Listing Events

```
You: What's on my calendar this week?
Bot: 📅 You have 3 events:
     
     1. Monday, March 24 at 10:00
        Team meeting (1 hour)
        
     2. Wednesday, March 26 at 14:00
        Dentist appointment (1 hour)
        Location: Dr. Smith's Office
        
     3. Friday, March 28 at 18:00
        Gym session (1.5 hours)
        Location: FitGym

You: Show me tomorrow's schedule
Bot: 📅 You have 2 events tomorrow:
     - 09:00: Morning standup (30 min)
     - 14:00: Client call (1 hour)
```

### Finding Free Time

```
You: When am I free tomorrow?
Bot: 🔍 Available slots tomorrow:
     - 09:00 - 12:00 (3 hours)
     - 13:00 - 14:00 (1 hour)
     - 15:00 - 18:00 (3 hours)

You: Find me 30 minutes tomorrow afternoon
Bot: 🔍 Free 30-minute slots tomorrow afternoon:
     - 13:00 - 13:30
     - 15:00 - 15:30
     - 16:30 - 17:00

You: Am I free Monday morning?
Bot: 🔍 Monday morning (9am-12pm) availability:
     - 09:00 - 10:00 (1 hour) ✅
     - 11:00 - 12:00 (1 hour) ✅
     
     Note: You have "Team meeting" at 10:00-11:00
```

**Working hours defaults:**
- Start: 9:00 AM
- End: 6:00 PM
- Customizable per request

### Deleting Events

```
You: Cancel my gym session on Friday
Bot: Let me check your Friday schedule...
     Found: "Gym session" at 18:00
     ✅ Cancelled event

You: Remove the dentist appointment
Bot: I found these events with "dentist":
     1. March 26 at 14:00 - Dentist appointment
     Should I cancel this one?
     
You: Yes
Bot: ✅ Cancelled "Dentist appointment" on March 26
```

## Advanced Features

### Conflict Detection

The agent intelligently checks for conflicts:

```
You: Book lunch with Sarah tomorrow at 1pm
Bot: ⚠️  You already have "Client call" at 13:00-14:00
     Would you like me to:
     1. Find an alternative time?
     2. Book anyway (overlap)?
```

### Multi-Event Booking

```
You: Tomorrow I need to schedule:
     - Morning workout at 7am (1 hour)
     - Team standup at 10am (30 min)
     - Lunch break at 12pm (1 hour)
     
Bot: ✅ Created 3 events for tomorrow:
     - 07:00: Morning workout
     - 10:00: Team standup
     - 12:00: Lunch break
```

### Combined Logging + Booking

```
You: Today I slept 8 hours, worked out, and felt great. 
     Also book my next workout for Friday 7am.
     
Bot: ✅ Created daily log entry for today
     ✅ Scheduled "Workout" for Friday, March 21 at 07:00
```

## Configuration

### Working Hours

Default working hours: 9am - 6pm

Customize in prompt:
```
You: Find me 1 hour tomorrow between 8am and 10pm
Bot: [Searches 8am-10pm range]
```

Or modify `src/agent_prompt.py` for permanent changes.

### Timezone

Set in `.env`:
```bash
TIMEZONE=America/New_York
TIMEZONE=Europe/London
TIMEZONE=Asia/Tokyo
```

Valid timezones: [IANA timezone database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### Calendar Selection

Default: Primary calendar

To use a different calendar, modify `calendar_id` in `src/tools/calendar_tools.py`

## Troubleshooting

### "credentials.json not found"

**Solution**: Download OAuth credentials from Google Cloud Console (see Setup section)

### "Token expired" or "Invalid credentials"

**Solution**: Delete `token.pickle` and re-authorize:
```bash
rm token.pickle
uv run main.py
# Browser will open for re-authorization
```

### "Access denied" or "Insufficient permissions"

**Solutions**:
1. Check OAuth consent screen settings in Google Cloud Console
2. Make sure your email is added as a test user
3. Revoke access in [Google Account Settings](https://myaccount.google.com/permissions)
4. Re-authorize

### Rate Limits

Google Calendar API limits:
- 1,000,000 requests/day (way more than you'll ever need)
- 10,000 requests per 100 seconds

For personal use, you'll never hit these limits.

### Events Not Showing Up

**Check**:
1. Timezone mismatch - verify `TIMEZONE` in `.env`
2. Calendar selection - make sure using correct calendar
3. Date format - ensure dates are parsed correctly

## Security

### Credentials Storage

- `credentials.json` - OAuth client secrets (gitignored)
- `token.pickle` - Access/refresh tokens (gitignored)

**Never commit these files to version control!**

### Token Refresh

The library automatically refreshes expired tokens. You don't need to re-authorize unless:
- You revoke access manually
- Token file is deleted/corrupted
- Credentials change in Google Cloud Console

### Scope Permissions

memobot requests these scopes:
- `https://www.googleapis.com/auth/calendar` - Full calendar access

This allows creating, reading, updating, and deleting events.

## API Costs

**Google Calendar API: FREE** ✅
- No charges for any volume
- Generous rate limits
- Perfect for personal use

**OpenAI API**: ~$0.01 per calendar operation with GPT-4o
- Booking event: ~1,500 tokens (~$0.01)
- Listing events: ~1,000 tokens (~$0.007)
- Finding slots: ~1,200 tokens (~$0.008)

## Technical Details

### Files Structure

```
src/tools/calendar_tools.py    # Calendar API functions
src/agent_tools.py              # Tool definitions for OpenAI
src/agent.py                    # Agent logic (tool routing)
src/agent_prompt.py             # System prompt (capabilities)
credentials.json                # OAuth credentials (gitignored)
token.pickle                    # Access tokens (gitignored)
```

### Function Signatures

See `src/tools/calendar_tools.py` for full details:

```python
create_calendar_event(summary, start_time, end_time, description?, location?)
list_calendar_events(start_date, end_date?, max_results?)
find_free_slots(date, duration_minutes?, working_hours_start?, working_hours_end?)
delete_calendar_event(event_id)
```

### ISO 8601 Format

All datetimes use ISO 8601:
- Date: `2026-03-19`
- DateTime: `2026-03-19T14:00:00`
- With timezone: `2026-03-19T14:00:00+01:00`

The agent handles conversions automatically.

## Further Reading

- [Google Calendar API Documentation](https://developers.google.com/calendar/api)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [IANA Timezone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Limitations

Current version supports:
- ✅ Single-event creation
- ✅ Event listing
- ✅ Free slot finding
- ✅ Event deletion

Not yet implemented:
- ❌ Event updating/editing
- ❌ Recurring events
- ❌ Multiple calendar support
- ❌ Event reminders/notifications
- ❌ Attendee management

Want these features? Open an issue or contribute!

## Support

Having issues? Check:
1. This documentation
2. [Google Calendar API Troubleshooting](https://developers.google.com/calendar/api/guides/troubleshooting)
3. GitHub issues
4. Discord community

---

**Next Steps**: Try booking your first event! 🚀

```
You: Book a test event tomorrow at 3pm
```
