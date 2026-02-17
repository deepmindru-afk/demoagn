"""
Scout Evaluation Suite.

Usage:
    python -m agents.scout.evals.run_evals                    # String matching (default)
    python -m agents.scout.evals.run_evals --llm-grader       # LLM-based grading
    python -m agents.scout.evals.run_evals --check-sources    # Source citation verification
"""

from agents.scout.evals.grader import GradeResult, check_source_citation, grade_response
from agents.scout.evals.test_cases import CATEGORIES, TEST_CASES, TestCase

__all__ = [
    "TEST_CASES",
    "CATEGORIES",
    "TestCase",
    "grade_response",
    "check_source_citation",
    "GradeResult",
]
