"""
Test cases for evaluating Relay (User Feedback demo agent).

Each test case includes:
- question: The natural language question to ask
- expected_strings: Strings that should appear in the response
- expected_tools: Tool names the agent should call
- category: Test category for filtering
"""

from evals import TestCase

TEST_CASES: list[TestCase] = [
    # Travel - trip planning questions that should trigger ask_user
    TestCase(
        question="Help me plan a vacation for next month.",
        expected_strings=["ask_user"],
        expected_tools=["ask_user"],
        category="travel",
    ),
    TestCase(
        question="I want to plan a weekend getaway. Where should I go?",
        expected_strings=["ask_user"],
        expected_tools=["ask_user"],
        category="travel",
    ),
    # Events - event planning that should trigger structured questions
    TestCase(
        question="Help me plan a team offsite for 20 people.",
        expected_strings=["ask_user"],
        expected_tools=["ask_user"],
        category="events",
    ),
    TestCase(
        question="I need to organize a birthday dinner for my partner.",
        expected_strings=["ask_user"],
        expected_tools=["ask_user"],
        category="events",
    ),
    # Direct - requests with enough detail to skip questions
    TestCase(
        question="Plan a 3-day trip to Tokyo with a $2000 budget, focused on food and culture.",
        expected_strings=["Tokyo"],
        expected_tools=[],
        category="direct",
    ),
    TestCase(
        question="Recommend a casual Italian restaurant in downtown for 4 people, budget around $50 per person.",
        expected_strings=["Italian"],
        expected_tools=[],
        category="direct",
    ),
    # Edge cases - ambiguous or unusual requests
    TestCase(
        question="I'm bored. Suggest something fun to do.",
        expected_strings=["ask_user"],
        expected_tools=["ask_user"],
        category="edge_case",
    ),
    TestCase(
        question="What's the best vacation destination?",
        expected_strings=["ask_user"],
        expected_tools=["ask_user"],
        category="edge_case",
    ),
]

# Categories for filtering
CATEGORIES = ["travel", "events", "direct", "edge_case"]
