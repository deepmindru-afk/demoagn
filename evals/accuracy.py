"""
Accuracy Evals
===============

Tests whether agents produce correct answers for known queries.
Uses an LLM judge to compare agent output against expected answers.

Run:
    python -m evals.accuracy
"""

from agno.eval.accuracy import AccuracyEval
from agno.models.openai import OpenAIResponses

from agents.dash import dash
from agents.scout import scout
from db import get_postgres_db

eval_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Dash: Known F1 query with a verifiable answer
# ---------------------------------------------------------------------------
dash_accuracy_eval = AccuracyEval(
    db=eval_db,
    name="Dash Accuracy - F1 Race Winners",
    model=OpenAIResponses(id="gpt-5.2"),
    agent=dash,
    input="Who won the most Formula 1 races in the 2019 season?",
    expected_output="Lewis Hamilton won the most races in the 2019 season with 11 victories.",
    additional_guidelines="The answer must identify Lewis Hamilton and mention 11 wins.",
    num_iterations=1,
)

# ---------------------------------------------------------------------------
# Scout: Known PTO policy from employee handbook
# ---------------------------------------------------------------------------
scout_accuracy_eval = AccuracyEval(
    db=eval_db,
    name="Scout Accuracy - PTO Policy",
    model=OpenAIResponses(id="gpt-5.2"),
    agent=scout,
    input="What is our PTO policy?",
    expected_output=(
        "Acme Corp offers unlimited PTO with manager approval. "
        "A minimum of two weeks (10 business days) per year is recommended. "
        "Requests exceeding three consecutive days should be submitted "
        "through Workday at least two weeks in advance."
    ),
    additional_guidelines=(
        "The answer must mention unlimited PTO, manager approval, "
        "and the recommended minimum. Must cite the employee handbook as source."
    ),
    num_iterations=1,
)

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Dash Accuracy Eval")
    print("=" * 60)
    dash_result = dash_accuracy_eval.run(print_results=True, print_summary=True)
    if dash_result:
        print(f"Average score: {dash_result.avg_score}/10\n")

    print("=" * 60)
    print("Scout Accuracy Eval")
    print("=" * 60)
    scout_result = scout_accuracy_eval.run(print_results=True, print_summary=True)
    if scout_result:
        print(f"Average score: {scout_result.avg_score}/10")
