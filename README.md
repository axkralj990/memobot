# memobot 🤖

> *Agentic memory bot that logs to Notion*

An **agentic AI system** that captures your health and wellness data through natural language Discord messages and stores them in Notion.

> 🎓 **New to agentic programming?** Start with [docs/QUICKSTART.md](./docs/QUICKSTART.md)!

## What Makes This "Agentic"?

Unlike traditional bots that follow fixed rules, this assistant uses **AI reasoning** to:
- 🧠 **Understand intent** - Knows if you're logging data or asking questions
- 🔧 **Choose tools** - Autonomously selects the right function to accomplish your goal
- 💬 **Respond naturally** - Provides conversational, contextual responses

**Example:**
```
You: "Yesterday I slept 8 hours and had 2 coffees"
→ Agent creates a Notion entry

You: "What did I log yesterday?"
→ Agent queries Notion and summarizes your day

You: "How does the anxiety scale work?"
→ Agent responds conversationally without using tools
```

See [docs/AGENTIC_PROGRAMMING.md](./docs/AGENTIC_PROGRAMMING.md) to learn how it works!

## Features

- 🤖 **Discord Bot Integration**: Send messages in natural language to your private Discord channel
- 🧠 **AI-Powered Parsing**: OpenAI GPT extracts structured data from your messages
- 📊 **Notion Database**: Automatically creates and organizes entries in your Notion database
- 📅 **Smart Date Handling**: Understands "yesterday", "today", or specific dates
- 🌤️ **Automatic Weather**: Fetches weather data for your location and adds it to each entry
- 💪 **Health Tracking**: Sleep, anxiety, productivity, supplements, exercise, and more

## What You Can Track

- Productivity levels
- Anxiety status (1-5 scale)
- Physical status
- Sleep hours
- Weight
- Mindfulness/meditation minutes
- Supplements taken
- Coffee consumption
- Alcohol units
- Fasting hours
- Cold exposure minutes (defaults to 1 if not specified)
- Fish/meat consumption
- Substances
- **What you learned** - The agent extracts learning-related content (e.g., "I learned about X")
- **General notes** - Summary of your entire day including workouts, activities, and anything that doesn't fit into specific fields

### 🌤️ Automatic Weather Integration

Each daily entry includes weather data automatically fetched from Open-Meteo:
- Temperature (min/max)
- Precipitation
- Weather conditions
- Default location: **Ljubljana** (customizable via message, e.g., "I'm in Berlin today")

📖 **See [docs/WEATHER_INTEGRATION.md](./docs/WEATHER_INTEGRATION.md) for detailed weather documentation**

## Setup

### 1. Install Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file with:

```env
# Notion
NOTION_API_KEY=ntn_your_notion_integration_token
NOTION_DATABASE_ID=04f42963-328a-4d91-ad6c-cc20a7efb105

# OpenAI
OPENAI_API_KEY=sk-your_openai_api_key

# Discord
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

### 3. Set Up Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration and copy the token
3. Share your database with the integration:
   - Open your Notion database
   - Click "..." → "Add connections"
   - Select your integration

### 4. Set Up Discord Bot

Follow the instructions in [docs/DISCORD_SETUP.md](./docs/DISCORD_SETUP.md)

## Usage

### Run the Bot

```bash
uv run main.py
```

### Test the Agent Locally

Test the agentic system without Discord:

```bash
PYTHONPATH=. uv run python tests/test_agent.py
```

This opens an interactive CLI where you can experiment with different prompts and see how the agent reasons and chooses tools.

### Send Messages to Discord

Once running, send natural language messages in your configured Discord channel:

**Example 1:**
```
Yesterday I slept 7 hours, had 2 coffees, feeling anxious (maybe a 4), 
took my omega3 and vitamins, went for a cold shower for 5 minutes
```

The Notion entry will include a weather callout like:
```
📍 Ljubljana
🌡️ 4.1°C - 15.9°C
☁️ Moderate rain
🌧️ 7.5mm precipitation
```

**Example 2:**
```
Great productive day! Slept well (8h), did 20 min meditation, 
ate salmon for lunch, feeling good physically and mentally calm (anxiety: 1)
```

**Example 3 (With learning and activities):**
```
Yesterday was productive! Slept 7 hours, 3 coffees. Did a 45-minute HIIT workout 
at the gym, then had salmon for lunch. Feeling really good physically, anxiety 
around 1-2. Took my omega3 and vitamins.

I learned about agentic programming patterns and how function calling works in OpenAI.

Evening: went for a cold shower (5 min), then 15 minutes meditation.
```

This creates an entry with:
- **General Notes**: "Did a 45-minute HIIT workout at the gym. Went for a cold shower and then did 15 minutes of meditation. Had salmon for lunch."
- **Learned**: "agentic programming patterns, how function calling works in OpenAI..."

**Example 4 (Querying):**
```
What did I log yesterday?
```

**Example 5 (Querying):**
```
Show me my entry from March 15th
```

The bot will:
1. **Understand your intent** (creating vs querying)
2. **Fetch weather data** automatically (default: Ljubljana)
3. **Use the appropriate tool** (create or query Notion)
4. **Provide a natural response** with relevant data
5. **Include a link** to the Notion page (when creating)

Weather is added automatically as a callout block in the Notion page with temperature, conditions, and precipitation data.

### 🌍 Supported Locations

Weather data is available for any location. Some pre-configured cities include:
- Ljubljana (default)
- London
- New York
- Tokyo

You can mention a location in your message (e.g., "I'm in Berlin today") and the agent will fetch weather for that location. To add more cities, update `LOCATIONS` in `src/tools/weather_tools.py`.

## Learning Agentic Programming

This project is an excellent introduction to agentic AI systems! 

**Getting Started:**
- 📖 [docs/QUICKSTART.md](./docs/QUICKSTART.md) - Quick intro to agentic concepts
- 🔬 [docs/AGENTIC_PROGRAMMING.md](./docs/AGENTIC_PROGRAMMING.md) - Deep dive into agent patterns
- 🛠️ [docs/EXTENDING_AGENT.md](./docs/EXTENDING_AGENT.md) - How to add new tools/capabilities

**Topics covered:**
- How agents work
- The agent loop pattern
- Tool use and function calling
- Intent recognition
- Multi-step reasoning
- Advanced patterns

## Project Structure

```
assistant/
├── src/                     # Core application code
│   ├── models/             # Pydantic models and enums
│   ├── tools/              # Notion API and weather tools
│   ├── agent.py            # 🤖 Agentic orchestration
│   ├── agent_tools.py      # Tool definitions for OpenAI
│   ├── agent_prompt.py     # System prompt generation
│   ├── discord_bot.py      # Discord bot implementation
│   └── openai_parser.py    # OpenAI parsing (legacy)
├── tests/                   # Test scripts
│   ├── test_agent.py       # Test agent locally
│   ├── test_parser.py      # Test OpenAI parser
│   ├── test_weather.py     # Test weather integration
│   └── fetch_latest.py     # Fetch latest Notion entry
├── docs/                    # Documentation
│   ├── AGENTIC_PROGRAMMING.md  # 📚 Agentic systems guide
│   ├── QUICKSTART.md           # Quick intro to agents
│   ├── EXTENDING_AGENT.md      # How to add capabilities
│   ├── DISCORD_SETUP.md        # Discord bot setup
│   ├── WEATHER_INTEGRATION.md  # Weather feature docs
│   ├── SECURITY_AUDIT.md       # Security analysis
│   └── DEPLOYMENT.md           # Deployment guide (Pi, VPS)
├── main.py                  # Main entry point
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Utilities

### Test the Parser

Test the OpenAI parser without Discord:

```bash
PYTHONPATH=. uv run python tests/test_parser.py
```

### Fetch Latest Entry

Retrieve the most recent entry from your Notion database:

```bash
PYTHONPATH=. uv run python tests/fetch_latest.py
```

## Models

The system uses strongly-typed Pydantic models with enums for all categorical data:

- `Productivity`: high, medium, low
- `AnxietyStatus`: 1-5 scale
- `PhysicalStatus`: good, ok, not so good, bad
- `Temperature`: scorching, hot, warm, perfect, normal, cold, freezing
- `Weather`: sunny, cloudy, rainy, storms, etc.
- `Supplement`: omega3, proteins, creatine, vitamins, etc.

## Requirements

- Python 3.11+
- OpenAI API key (GPT-4)
- Notion integration token
- Discord bot token

## License

MIT
