"""
Sentinel Evaluation Suite.

Uses Agno's AccuracyEval and ReliabilityEval to test approval patterns.

Usage:
    python -m agents.sentinel.evals.run_evals
"""

from agents.sentinel.evals.test_cases import CATEGORIES, TEST_CASES

__all__ = [
    "TEST_CASES",
    "CATEGORIES",
]
