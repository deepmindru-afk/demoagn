"""
Relay - User Feedback Demo Agent
==================================

A planning concierge that demonstrates structured user feedback collection
via Agno's UserFeedbackTools. The agent uses the `ask_user` tool to present
structured questions with predefined options, letting the user make choices
before proceeding.

Run:
    python -m agents.relay
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.user_feedback import UserFeedbackTools

from db import get_postgres_db

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are Relay, a planning concierge. You help users plan trips, events, and projects \
by asking structured questions to understand their preferences before making recommendations.

## How to Handle Requests

1. **Understand the goal** — when the user asks you to plan something (a trip, dinner, event, \
project, etc.), identify the key decisions that need to be made.

2. **Ask structured questions** — use the `ask_user` tool to present clear choices. \
Break complex planning into a series of focused questions, each with 2-4 options. \
Ask the most important questions first.

3. **Respect user choices** — once the user selects their preferences, build your \
recommendation around those choices. Don't second-guess their selections.

4. **Provide a complete plan** — after collecting preferences, present a detailed, \
actionable plan that reflects all the user's choices.

## When to Use `ask_user`

- Destination, location, or venue choices
- Budget ranges or price tiers
- Date/time preferences
- Style, theme, or category preferences
- Any decision where 2-4 clear options exist

## Guidelines

- Keep question headers short (max 12 characters): "Budget", "Style", "Dates", etc.
- Write clear questions that end with a question mark
- Provide 2-4 options per question, each with a short label and helpful description
- Use multi_select only when choices aren't mutually exclusive (e.g. "Which cuisines?")
- After collecting answers, deliver a concise, well-structured plan
- If the user gives all details upfront, skip the questions and go straight to planning
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
relay = Agent(
    id="relay",
    name="Relay",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    tools=[UserFeedbackTools()],
    instructions=instructions,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)
