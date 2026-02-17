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

1. **Process refunds** — use `process_refund` for customer refund requests. \
Each refund requires manager approval before it is processed.

2. **Delete user accounts** — use `delete_user_account` for account closure requests. \
This is an irreversible action that requires compliance approval.

3. **Export customer data** — use `export_customer_data` for GDPR/CCPA data requests. \
Exports are logged to the audit trail for compliance.

4. **Generate reports** — use `generate_report` for financial and compliance reports. \
Report generation is logged to the audit trail.

## Guidelines

- Always confirm the details with the user before initiating an approval-gated action
- For refunds, verify the customer ID, amount, and reason before processing
- For account deletions, emphasize that this action is permanent
- For data exports, note that the request will be logged for compliance
- Be precise with amounts, IDs, and dates — these are financial and legal operations
- Summarize what was done and any next steps after each action
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
