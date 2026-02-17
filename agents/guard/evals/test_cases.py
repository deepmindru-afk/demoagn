"""
Test cases for evaluating Guard (HITL demo agent).

Each test case includes:
- question: The natural language question to ask
- expected_strings: Strings that should appear in the response
- expected_tools: Tool names the agent should call
- category: Test category for filtering
"""

from evals import TestCase

TEST_CASES: list[TestCase] = [
    # Confirmation - tests requiring operator approval (restart_service)
    TestCase(
        question="The auth service is returning 503 errors. Can you restart it?",
        expected_strings=["restart", "auth"],
        expected_tools=["restart_service"],
        category="confirmation",
    ),
    TestCase(
        question="Payments-api is unresponsive, please restart it immediately.",
        expected_strings=["restart", "payments"],
        expected_tools=["restart_service"],
        category="confirmation",
    ),
    # User input - tests requiring user-provided priority (create_support_ticket)
    TestCase(
        question="Create a ticket for the broken CI pipeline.",
        expected_strings=["ticket", "CI"],
        expected_tools=["create_support_ticket"],
        category="user_input",
    ),
    TestCase(
        question="Log a support ticket: the staging database is running out of disk space.",
        expected_strings=["ticket", "disk"],
        expected_tools=["create_support_ticket"],
        category="user_input",
    ),
    # External execution - tests running diagnostics outside agent runtime
    TestCase(
        question="Check the health of the payments-api.",
        expected_strings=["health", "payments"],
        expected_tools=["run_diagnostic"],
        category="external_execution",
    ),
    TestCase(
        question="Run diagnostics on the auth service to see why it's slow.",
        expected_strings=["diagnostic", "auth"],
        expected_tools=["run_diagnostic"],
        category="external_execution",
    ),
    # Edge cases - ambiguous or multi-step requests
    TestCase(
        question="Something is wrong with the search service but I'm not sure what.",
        expected_strings=["diagnostic", "search"],
        expected_tools=["run_diagnostic"],
        category="edge_case",
    ),
    TestCase(
        question="The API is down. Fix it and create a ticket to track the incident.",
        expected_strings=["restart", "ticket"],
        expected_tools=["restart_service", "create_support_ticket"],
        category="edge_case",
    ),
]

# Categories for filtering
CATEGORIES = ["confirmation", "user_input", "external_execution", "edge_case"]
