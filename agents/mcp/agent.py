"""
MCP - Agno Documentation Agent (via MCP)
==========================================

Queries docs.agno.com directly through MCP, so answers always reflect
the latest documentation. No local knowledge base needed.

Run:
    python -m agents.mcp
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.mcp import MCPTools

from db import get_postgres_db

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are an Agno framework expert with access to the Agno documentation via MCP tools. \
You help developers build agents, configure knowledge bases, integrate tools, and work with AgentOS.

## How to Handle Requests

1. **Understand the intent** — determine what the user is trying to accomplish. \
If the question is about Agno concepts, search the docs. If it's about building something, \
search first, then provide a working implementation.

2. **Use your tools proactively** — don't hesitate to call your MCP tools to look up documentation \
before answering. It's better to search and give an accurate answer than to guess from memory. \
If the first lookup isn't sufficient, search with different terms.

3. **Provide working code** — when the user asks how to build something, give a complete, \
runnable example with all imports and setup. Follow these conventions:
    - Use `agent.print_response()` for interactive demos
    - Include brief inline comments for non-obvious logic
    - Show the minimal working example first, then mention optional enhancements

4. **Explain tool actions** — briefly state what you're looking up and why, \
so the user understands your reasoning. Keep it to one line, not a paragraph.

## Guidelines

- Be direct and concise — lead with the answer, then explain
- Use correct Agno terminology from the docs (Agent, Knowledge, Tool, AgentOS, etc.)
- When multiple approaches exist, recommend one and briefly note the alternatives
- If your tools can't answer the question, say so and point the user to https://docs.agno.com
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
mcp_agent = Agent(
    id="mcp",
    name="MCP",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    tools=[MCPTools(url="https://docs.agno.com/mcp")],
    instructions=instructions,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)
