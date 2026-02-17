"""
Guard Evaluation Suite.

Uses Agno's AccuracyEval and ReliabilityEval to test HITL patterns.

Usage:
    python -m agents.guard.evals.run_evals
"""

from agents.guard.evals.test_cases import CATEGORIES, TEST_CASES

__all__ = [
    "TEST_CASES",
    "CATEGORIES",
]
