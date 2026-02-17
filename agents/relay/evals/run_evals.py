"""
Run evaluations against Relay.

Uses Agno's AccuracyEval (LLM judge) and ReliabilityEval (tool-call verification).

Usage:
    python -m agents.relay.evals.run_evals
    python -m agents.relay.evals.run_evals --category travel
"""

import argparse

from agno.eval.accuracy import AccuracyEval
from agno.eval.reliability import ReliabilityEval
from agno.models.openai import OpenAIResponses

from agents.relay.evals.test_cases import CATEGORIES, TEST_CASES
from db import get_postgres_db

EVAL_GUIDELINES = (
    "Did the agent use ask_user when preferences need clarification? "
    "When the user provides enough detail, the agent should skip questions "
    "and plan directly. Extra clarifying questions are acceptable."
)

eval_db = get_postgres_db()


def run_evals(category: str | None = None) -> None:
    """Run evaluation suite for Relay."""
    from agents.relay.agent import relay

    tests = TEST_CASES
    if category:
        tests = [tc for tc in tests if tc.category == category]

    if not tests:
        print(f"No tests found for category: {category}")
        return

    print(f"Running {len(tests)} Relay evals...")

    for idx, tc in enumerate(tests, 1):
        print(f"\n{'=' * 60}")
        print(f"[{idx}/{len(tests)}] {tc.question}")
        print(f"Category: {tc.category}")
        print("=" * 60)

        response = relay.run(tc.question)

        # Accuracy: LLM judge compares output vs expected
        AccuracyEval(
            db=eval_db,
            name=f"Relay Accuracy - {tc.category}",
            model=OpenAIResponses(id="gpt-5.2"),
            agent=relay,
            input=tc.question,
            expected_output=", ".join(tc.expected_strings),
            additional_guidelines=EVAL_GUIDELINES,
            num_iterations=1,
        ).run_with_output(output=response.content or "", print_results=True, print_summary=True)

        # Reliability: verify expected tools were called
        if tc.expected_tools:
            ReliabilityEval(
                db=eval_db,
                name=f"Relay Reliability - {tc.category}",
                agent_response=response,
                expected_tool_calls=tc.expected_tools,
            ).run(print_results=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Relay evaluations")
    parser.add_argument("--category", "-c", choices=CATEGORIES, help="Filter by category")
    args = parser.parse_args()

    run_evals(category=args.category)
