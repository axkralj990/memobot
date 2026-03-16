# Understanding Agentic Programming 🤖

This project demonstrates **agentic programming** - an AI pattern where the model autonomously decides what actions to take based on user input.

## What is Agentic Programming?

Traditional approach:
```
User Input → Fixed Logic → Single Action → Response
```

Agentic approach:
```
User Input → AI Reasoning → Choose Tool(s) → Execute → AI Synthesis → Response
```

The AI **agent** has:
1. **Reasoning** - Understands user intent
2. **Tools** - Functions it can call to accomplish tasks
3. **Autonomy** - Decides which tools to use and when
4. **Iteration** - Can use multiple tools in sequence

## How Our Agent Works

### 1. Tool Definition

The agent has access to tools (functions):

```python
tools = [
    {
        "name": "create_daily_entry",
        "description": "Create a new daily log entry...",
        "parameters": {...}
    },
    {
        "name": "query_daily_entries", 
        "description": "Query and retrieve entries...",
        "parameters": {...}
    }
]
```

### 2. Agent Loop

```python
while not_done:
    # 1. AI decides what to do
    response = openai.chat.completions.create(
        messages=[...],
        tools=tools,
        tool_choice="auto"  # Let AI decide
    )
    
    # 2. If AI wants to use a tool
    if response.tool_calls:
        for tool_call in response.tool_calls:
            # 3. Execute the tool
            result = execute_tool(tool_call)
            
            # 4. Give result back to AI
            messages.append(tool_result)
    else:
        # 5. AI is done, return response
        return response.content
```

### 3. Intent Recognition

The agent automatically determines intent:

**Create Intent:**
```
User: "Yesterday I slept 8 hours and had 2 coffees"
Agent: → Uses create_daily_entry tool
```

**Query Intent:**
```
User: "What did I log yesterday?"
Agent: → Uses query_daily_entries tool
```

**Conversational:**
```
User: "How does the anxiety scale work?"
Agent: → Responds directly without tools
```

## Key Agentic Patterns

### 1. Tool Use (Function Calling)

The AI can call functions to interact with external systems:

```python
def create_daily_entry(entry_data: dict):
    """Tool that creates Notion entries."""
    entry = DailyEntryInput.model_validate(entry_data)
    return create_notion_entry(entry, db_id, token)
```

### 2. Multi-Step Reasoning

The agent can chain multiple tools:

```
User: "Compare yesterday to last Monday"

Agent:
  1. Uses query_daily_entries for yesterday
  2. Uses query_daily_entries for last Monday  
  3. Synthesizes comparison
  4. Returns analysis
```

### 3. Context Awareness

The agent maintains conversation history:

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What did I log yesterday?"},
    {"role": "assistant", "tool_calls": [...]},
    {"role": "tool", "content": "{...}"},
    {"role": "assistant", "content": "Here's what you logged..."}
]
```

### 4. Error Recovery

The agent can handle failures gracefully:

```python
if result["success"] == False:
    # Agent sees the error and can try alternative approach
    # or ask user for clarification
```

## Example Flow

**User Message:** "What did I eat yesterday?"

**Step 1: Intent Recognition**
```
AI analyzes: User is asking ABOUT yesterday (query intent)
```

**Step 2: Tool Selection**
```
AI decides: Use query_daily_entries tool
Parameters: target_date = "2026-03-15"
```

**Step 3: Tool Execution**
```python
result = query_daily_entries(target_date="2026-03-15")
# Returns: {fish: True, meat: False, supplements: ["omega3"]}
```

**Step 4: Synthesis**
```
AI reads result and generates natural response:
"Yesterday you ate fish and took omega3 supplements. 
You didn't have any meat."
```

## Benefits of Agentic Approach

1. **Flexible** - Handles diverse inputs without explicit rules
2. **Intelligent** - Understands context and intent
3. **Extensible** - Easy to add new tools/capabilities
4. **Natural** - Conversational interface
5. **Powerful** - Can chain complex operations

## Advanced Patterns

### Memory

Add long-term memory:
```python
# Store conversation history in database
# Load relevant past conversations as context
```

### Verification

Add verification step:
```python
{
    "name": "verify_before_create",
    "description": "Show user preview before creating"
}
```

### Multi-Agent Systems

Multiple specialized agents:
```python
health_agent = Agent(tools=[sleep_analysis, nutrition])
mood_agent = Agent(tools=[sentiment_analysis, trends])
coordinator = Agent(sub_agents=[health_agent, mood_agent])
```

## Testing the Agent

Run the interactive test:

```bash
uv run test_agent.py
```

Try these prompts:
- "Yesterday I slept 7 hours" → Creates entry
- "What did I log yesterday?" → Queries entry
- "Show me last week" → Could extend to multi-day query
- "How has my sleep been?" → Could add analytics tool

## Learn More

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- [ReAct Pattern](https://arxiv.org/abs/2210.03629)
