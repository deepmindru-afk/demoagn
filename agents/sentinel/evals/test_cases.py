"""
Test cases for evaluating Sentinel (Approvals demo agent).

Each test case includes:
- question: The natural language question to ask
- expected_strings: Strings that should appear in the response
- expected_tools: Tool names the agent should call
- category: Test category for filtering
"""

from evals import TestCase

TEST_CASES: list[TestCase] = [
    # Refund - tests for process_refund (blocking approval)
    TestCase(
        question="Process a $250 refund for customer C-1042 due to a billing error.",
        expected_strings=["refund", "C-1042", "250"],
        expected_tools=["process_refund"],
        category="refund",
    ),
    TestCase(
        question="Customer C-5567 was double-charged $89.99. Please issue a refund.",
        expected_strings=["refund", "C-5567"],
        expected_tools=["process_refund"],
        category="refund",
    ),
    # Data access - tests for export_customer_data (audit trail)
    TestCase(
        question="Export all data for customer C-3021 for a GDPR request.",
        expected_strings=["export", "C-3021"],
        expected_tools=["export_customer_data"],
        category="data_access",
    ),
    TestCase(
        question="Generate a revenue report for Q4 2025.",
        expected_strings=["report", "revenue", "Q4"],
        expected_tools=["generate_report"],
        category="data_access",
    ),
    # Account management - tests for delete_user_account (blocking approval)
    TestCase(
        question="Delete user account U-7788 per their closure request.",
        expected_strings=["delete", "U-7788"],
        expected_tools=["delete_user_account"],
        category="account_management",
    ),
    TestCase(
        question="User U-3344 has requested permanent account deletion under CCPA.",
        expected_strings=["delete", "U-3344"],
        expected_tools=["delete_user_account"],
        category="account_management",
    ),
    # Edge cases - ambiguous or multi-step requests
    TestCase(
        question="A customer is asking for their data to be deleted. Their ID is C-9901.",
        expected_strings=["C-9901"],
        expected_tools=["delete_user_account"],
        category="edge_case",
    ),
    TestCase(
        question="Process a refund and generate a compliance report for the same customer C-4455.",
        expected_strings=["refund", "report", "C-4455"],
        expected_tools=["process_refund", "generate_report"],
        category="edge_case",
    ),
]

# Categories for filtering
CATEGORIES = ["refund", "data_access", "account_management", "edge_case"]
