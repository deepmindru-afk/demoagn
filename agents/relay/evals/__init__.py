"""
Relay Evaluation Suite.

Uses Agno's AccuracyEval and ReliabilityEval to test user feedback patterns.

Usage:
    python -m agents.relay.evals.run_evals
"""

from agents.relay.evals.test_cases import CATEGORIES, TEST_CASES

__all__ = [
    "TEST_CASES",
    "CATEGORIES",
]
