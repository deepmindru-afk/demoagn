"""
Support - Governance Patterns Demo Agent
==========================================

A customer support agent that demonstrates three governance patterns in one agent:
- Auto-execute: order lookups and help doc searches run without approval
- Confirmation: refunds require operator approval before execution
- User feedback: structured questions collect missing info from the user

Run:
    python -m agents.support
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools import tool
from agno.tools.user_feedback import UserFeedbackTools

from db import get_postgres_db

# ---------------------------------------------------------------------------
# Simulated Data
# ---------------------------------------------------------------------------
ORDERS: dict[str, dict] = {
    "ORD-1042": {"item": "Wireless Keyboard", "status": "delivered", "total": 89.99},
    "ORD-1098": {"item": "USB-C Hub", "status": "shipped", "total": 45.00},
    "ORD-1107": {"item": "Monitor Stand", "status": "processing", "total": 129.99},
}

HELP_DOCS: dict[str, str] = {
    "returns": "Items may be returned within 30 days of delivery for a full refund. "
    "Items must be in original packaging. Refunds are processed within 5 business days.",
    "shipping": "Standard shipping takes 5-7 business days. "
    "Express shipping (2-day) is available for an additional $12.99.",
    "warranty": "All electronics carry a 1-year manufacturer warranty. "
    "Extended warranty (3 years) can be purchased within 30 days of delivery.",
}

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


def lookup_order(order_id: str) -> str:
    """Look up the current status of a customer order.

    Args:
        order_id: The order identifier (e.g. 'ORD-1042').

    Returns:
        Order details or an error if not found.
    """
    order = ORDERS.get(order_id)
    if not order:
        return f"Order '{order_id}' not found. Please check the order ID and try again."
    return f"Order {order_id}:\n  Item: {order['item']}\n  Status: {order['status']}\n  Total: ${order['total']:.2f}"


def search_help_docs(query: str) -> str:
    """Search help documentation for answers to common questions.

    Args:
        query: The topic to search for (e.g. 'returns', 'shipping', 'warranty').

    Returns:
        Matching help article or a list of available topics.
    """
    query_lower = query.lower()
    for topic, content in HELP_DOCS.items():
        if topic in query_lower:
            return f"**{topic.title()} Policy**\n\n{content}"
    available = ", ".join(HELP_DOCS.keys())
    return f"No exact match for '{query}'. Available topics: {available}"


@tool(requires_confirmation=True)
def issue_refund(order_id: str, reason: str) -> str:
    """Issue a refund for a customer order. Requires operator confirmation before executing.

    Args:
        order_id: The order identifier to refund (e.g. 'ORD-1042').
        reason: The reason for the refund.

    Returns:
        Refund confirmation or an error if the order is not found.
    """
    order = ORDERS.get(order_id)
    if not order:
        return f"Cannot refund: order '{order_id}' not found."
    if order["status"] != "delivered":
        return f"Cannot refund: order '{order_id}' has status '{order['status']}' (must be 'delivered')."
    return (
        f"Refund processed:\n"
        f"  Order: {order_id}\n"
        f"  Item: {order['item']}\n"
        f"  Amount: ${order['total']:.2f}\n"
        f"  Reason: {reason}\n"
        f"  Estimated return: 5 business days"
    )


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are Support, a customer support agent. You help customers check orders, \
answer policy questions, and process refunds.

## Available Actions

1. **Look up an order** — use `lookup_order` to check order status. This runs automatically.

2. **Search help docs** — use `search_help_docs` to answer policy questions about returns, \
shipping, or warranty. This runs automatically.

3. **Issue a refund** — use `issue_refund` when a customer requests a refund. \
The operator will be asked to confirm before the refund is processed.

4. **Collect information** — use the feedback tools to ask the user structured questions \
when you need more information to proceed (e.g. which order, what the issue is).

## Guidelines

- For order lookups, call `lookup_order` immediately with the order ID provided.
- For policy questions, call `search_help_docs` with the relevant topic.
- For refunds, look up the order first to verify it exists and is eligible, then call `issue_refund`.
- If the user's request is missing key information (order ID, reason for refund), \
use the feedback tools to ask structured questions before proceeding.
- Be friendly, concise, and action-oriented.
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
support = Agent(
    id="support",
    name="Support",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    tools=[lookup_order, search_help_docs, issue_refund, UserFeedbackTools()],
    instructions=instructions,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)
