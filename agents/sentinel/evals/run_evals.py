"""
Run evaluations against Sentinel.

Uses Agno's AccuracyEval (LLM judge) and ReliabilityEval (tool-call verification).

Usage:
    python -m agents.sentinel.evals.run_evals
    python -m agents.sentinel.evals.run_evals --category refund
"""

import argparse

from agno.eval.accuracy import AccuracyEval
from agno.eval.reliability import ReliabilityEval
from agno.models.openai import OpenAIResponses

from agents.sentinel.evals.test_cases import CATEGORIES, TEST_CASES
from db import get_postgres_db

EVAL_GUIDELINES = (
    "Did the agent acknowledge that approval is needed for sensitive operations? "
    "Did it use the correct tool (refund, delete, export, report)? "
    "Extra confirmation steps before acting are acceptable."
)

eval_db = get_postgres_db()


def run_evals(category: str | None = None) -> None:
    """Run evaluation suite for Sentinel."""
    from agents.sentinel.agent import sentinel

    tests = TEST_CASES
    if category:
        tests = [tc for tc in tests if tc.category == category]

    if not tests:
        print(f"No tests found for category: {category}")
        return

    print(f"Running {len(tests)} Sentinel evals...")

    for idx, tc in enumerate(tests, 1):
        print(f"\n{'=' * 60}")
        print(f"[{idx}/{len(tests)}] {tc.question}")
        print(f"Category: {tc.category}")
        print("=" * 60)

        response = sentinel.run(tc.question)

        # Accuracy: LLM judge compares output vs expected
        AccuracyEval(
            db=eval_db,
            name=f"Sentinel Accuracy - {tc.category}",
            model=OpenAIResponses(id="gpt-5.2"),
            agent=sentinel,
            input=tc.question,
            expected_output=", ".join(tc.expected_strings),
            additional_guidelines=EVAL_GUIDELINES,
            num_iterations=1,
        ).run_with_output(output=response.content or "", print_results=True, print_summary=True)

        # Reliability: verify expected tools were called
        if tc.expected_tools:
            ReliabilityEval(
                db=eval_db,
                name=f"Sentinel Reliability - {tc.category}",
                agent_response=response,
                expected_tool_calls=tc.expected_tools,
            ).run(print_results=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sentinel evaluations")
    parser.add_argument("--category", "-c", choices=CATEGORIES, help="Filter by category")
    args = parser.parse_args()

    run_evals(category=args.category)
