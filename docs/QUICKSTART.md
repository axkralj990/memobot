# Quick Start Guide 🚀

## What You've Built

An **agentic AI assistant** that:
- Listens to your Discord messages
- Understands if you're logging data or asking questions
- Automatically creates or queries Notion entries
- Responds naturally in conversation

## The Agent Pattern

```
Traditional Bot:          Agentic Bot:
User → Rules → Action     User → AI → Tools → Response
     (rigid)                   (intelligent)
```

## Core Components

### 1. Agent (`src/agent.py`)
The brain - reasons about intent and chooses tools

### 2. Tools (Functions the agent can call)
- `create_daily_entry()` - Saves to Notion
- `query_daily_entries()` - Retrieves from Notion

### 3. Discord Bot (`src/discord_bot.py`)
The interface - connects Discord to the agent

## Example Interactions

### Creating an Entry
```
You: "Yesterday I slept 8 hours, had 2 coffees, feeling anxious"

Agent thinks:
  - Intent: CREATE (user describing their day)
  - Tool: create_daily_entry
  - Date: yesterday
  - Extract: sleep=8, coffee=2, anxiety=4

Response: "✅ Entry created for March 15, 2026..."
```

### Querying an Entry
```
You: "What did I log yesterday?"

Agent thinks:
  - Intent: QUERY (user asking about past)
  - Tool: query_daily_entries
  - Date: yesterday

Response: "Yesterday you slept 8 hours, had 2 coffees..."
```

## How It Works (Technical)

1. **User sends message** to Discord
2. **Agent receives** message with context (today's date, etc.)
3. **GPT-4 analyzes** intent and parameters
4. **Agent executes** the chosen tool (create/query)
5. **Tool interacts** with Notion API
6. **Agent synthesizes** result into natural language
7. **Bot replies** to user on Discord

## Key Code Snippet

```python
# The agent loop
response = openai.chat.completions.create(
    messages=[...],
    tools=[create_daily_entry, query_daily_entries],
    tool_choice="auto"  # Let AI decide!
)

if response.tool_calls:
    # AI chose a tool - execute it
    result = execute_tool(tool_call)
    # Give result back to AI for synthesis
else:
    # AI responded directly
    return response.content
```

## Running It

```bash
# Test locally (no Discord)
uv run test_agent.py

# Run full Discord bot
uv run main.py
```

## Extending the Agent

Want to add more capabilities? Just add tools!

```python
{
    "name": "analyze_trends",
    "description": "Analyze sleep patterns over time",
    "parameters": {...}
}
```

The agent will automatically know when to use it!

## Learning Path

1. ✅ **Understand the basics** - Read this guide
2. 📚 **Deep dive** - Read [AGENTIC_PROGRAMMING.md](./AGENTIC_PROGRAMMING.md)
3. 🧪 **Experiment** - Run `test_agent.py` and try different prompts
4. 🔧 **Extend** - Add new tools to `src/agent.py`
5. 🚀 **Build** - Create your own agentic systems!

## Next Steps

### Add Analytics Tool
```python
def analyze_sleep_trends(days: int):
    """Analyze sleep patterns over N days"""
    # Query multiple entries
    # Calculate averages, trends
    # Return insights
```

### Add Multi-Day Queries
```python
def query_date_range(start_date: str, end_date: str):
    """Query entries across a date range"""
    # Useful for "show me this week"
```

### Add Comparisons
```python
def compare_dates(date1: str, date2: str):
    """Compare two days side by side"""
    # Useful for "compare yesterday to last Monday"
```

## Pro Tips

1. **Be descriptive in tool descriptions** - The AI reads them!
2. **Use clear parameter types** - Helps AI understand what to provide
3. **Return structured data** - Easier for AI to synthesize
4. **Keep tools focused** - One responsibility per tool
5. **Add error handling** - Agent can recover from failures

## Architecture Benefits

✅ **No hard-coded rules** - AI figures out intent
✅ **Easy to extend** - Just add new tools
✅ **Natural UX** - Conversational interface
✅ **Flexible** - Handles diverse inputs
✅ **Intelligent** - Understands context

## Common Questions

**Q: Why not just use if/else statements?**
A: Agents scale better and handle ambiguity gracefully.

**Q: Does it always work perfectly?**
A: No, but it handles edge cases better than rigid rules.

**Q: Can I add multiple agents?**
A: Yes! Advanced pattern: coordinator agent managing specialized sub-agents.

**Q: What about costs?**
A: Each interaction uses GPT-4 API calls. Monitor usage.

**Q: How do I debug?**
A: Agent prints tool calls. Use `test_agent.py` to iterate quickly.

## Resources

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use)

---

**You now understand agentic programming!** 🎉

The key insight: Instead of programming specific behaviors, you give the AI tools and let it reason about when to use them.
