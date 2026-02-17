"""
Reliability Eval
=================

Verifies that agents call the expected tools. For example, Dash should
use SQL tools when answering data questions, not hallucinate results.

Run:
    python -m evals.reliability
"""

from agno.eval.reliability import ReliabilityEval

from agents.dash import dash
from db import get_postgres_db

eval_db = get_postgres_db()


def run_dash_reliability_eval() -> None:
    """Run Dash and verify it uses SQL tools."""
    response = dash.run("Who won the most races in 2019?")
    evaluation = ReliabilityEval(
        db=eval_db,
        name="Dash Reliability - SQL Tool Usage",
        agent_response=response,
        expected_tool_calls=["run_sql_query"],
    )
    result = evaluation.run(print_results=True)

    if result:
        print(f"\nStatus: {result.eval_status}")
        if result.passed_tool_calls:
            print(f"Passed: {result.passed_tool_calls}")
        if result.failed_tool_calls:
            print(f"Failed: {result.failed_tool_calls}")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Dash Reliability Eval")
    print("=" * 60)
    run_dash_reliability_eval()
