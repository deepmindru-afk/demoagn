"""
Test cases for evaluating Support (governance patterns demo agent).

Each test case includes:
- question: The natural language question to ask
- expected_strings: Strings that should appear in the response
- expected_tools: Tool names the agent should call
- category: Test category for filtering
"""

from evals import TestCase

TEST_CASES: list[TestCase] = [
    # Order lookup - auto-execute pattern
    TestCase(
        question="Can you check the status of order ORD-1098?",
        expected_strings=["USB-C Hub", "shipped"],
        expected_tools=["lookup_order"],
        category="order_lookup",
    ),
    TestCase(
        question="Where is my order ORD-1107?",
        expected_strings=["Monitor Stand", "processing"],
        expected_tools=["lookup_order"],
        category="order_lookup",
    ),
    # Policy - auto-execute pattern
    TestCase(
        question="What's your return policy?",
        expected_strings=["30 days", "refund"],
        expected_tools=["search_help_docs"],
        category="policy",
    ),
    TestCase(
        question="How long does shipping take?",
        expected_strings=["5-7 business days"],
        expected_tools=["search_help_docs"],
        category="policy",
    ),
    # Refund - confirmation pattern
    TestCase(
        question="I'd like a refund on order ORD-1042",
        expected_strings=["refund", "ORD-1042"],
        expected_tools=["issue_refund"],
        category="refund",
    ),
    TestCase(
        question="Please refund my Wireless Keyboard order, it arrived damaged.",
        expected_strings=["refund", "Wireless Keyboard"],
        expected_tools=["issue_refund"],
        category="refund",
    ),
    # Edge cases - ambiguous or multi-step
    TestCase(
        question="I have a problem with order ORD-9999",
        expected_strings=["not found"],
        expected_tools=["lookup_order"],
        category="edge_case",
    ),
    TestCase(
        question="Check order ORD-1042 and tell me about your warranty policy.",
        expected_strings=["Wireless Keyboard", "warranty"],
        expected_tools=["lookup_order", "search_help_docs"],
        category="edge_case",
    ),
]

# Categories for filtering
CATEGORIES = ["order_lookup", "policy", "refund", "edge_case"]
