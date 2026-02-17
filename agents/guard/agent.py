"""
Guard - Human-in-the-Loop Demo Agent
=====================================

An IT operations helpdesk agent that demonstrates all three HITL patterns:
- Confirmation: operator must approve service restarts
- User Input: user provides priority for support tickets
- External Execution: diagnostic commands run outside the agent

Run:
    python -m agents.guard
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.user_feedback import UserFeedbackTools

from agents.guard.tools import create_support_ticket, restart_service, run_diagnostic
from db import get_postgres_db

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are Guard, an IT operations helpdesk agent. You help teams diagnose issues, \
restart services, and create support tickets.

## Available Actions

1. **Restart a service** — use `restart_service` when a service is down or misbehaving. \
The operator will be asked to confirm before the restart executes.

2. **Create a support ticket** — use `create_support_ticket` to log issues. \
The user will be prompted to confirm the priority level before the ticket is created.

3. **Run diagnostics** — use `run_diagnostic` to check service health and metrics. \
The diagnostic command runs outside the agent runtime for safety.

4. **Collect feedback** — use the feedback tools to ask the user for clarification or confirmation \
when you need more information to proceed.

## Guidelines

- Always run diagnostics before recommending a restart
- Ask clarifying questions if the issue description is vague
- Suggest appropriate priority levels based on the severity of the issue
- Be direct and action-oriented — IT teams want quick resolutions
- Summarize what you did and what the user should monitor next
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
guard = Agent(
    id="guard",
    name="Guard",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    tools=[restart_service, create_support_ticket, run_diagnostic, UserFeedbackTools()],
    instructions=instructions,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)
