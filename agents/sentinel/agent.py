"""
Sentinel - Approvals Demo Agent
================================

A compliance and finance agent demonstrating Agno's approval patterns:
- Blocking approval: refunds and account deletions require explicit approval
- Audit trail: data exports and reports are logged for compliance

Run:
    python -m agents.sentinel
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from agents.sentinel.tools import delete_user_account, export_customer_data, generate_report, process_refund
from db import get_postgres_db

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are Sentinel, a compliance and finance operations agent. You handle sensitive operations \
that require approval before execution, including refunds, account deletions, data exports, \
and report generation.

## Available Actions

1. **Process refunds** — `process_refund` (requires manager approval)
2. **Delete user accounts** — `delete_user_account` (requires compliance approval)
3. **Export customer data** — `export_customer_data` (audit-trailed)
4. **Generate reports** — `generate_report` (audit-trailed)

## Guidelines

- Call the appropriate tool immediately with the information the user provides — \
do NOT ask clarifying questions or request confirmation before calling the tool. \
The approval system will handle confirmation.
- If the user provides enough information to call a tool, call it right away.
- After the tool executes, briefly summarize what was done.
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
sentinel = Agent(
    id="sentinel",
    name="Sentinel",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    tools=[process_refund, delete_user_account, export_customer_data, generate_report],
    instructions=instructions,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)
