"""
Support Evaluation Suite.

Uses Agno's AccuracyEval and ReliabilityEval to test governance patterns.

Usage:
    python -m agents.support.evals.run_evals
"""

from agents.support.evals.test_cases import CATEGORIES, TEST_CASES

__all__ = [
    "TEST_CASES",
    "CATEGORIES",
]
