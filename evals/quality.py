"""
Quality Evals (Agent-as-Judge)
===============================

LLM-based quality evaluation using batch test cases. Scores agent responses
on criteria like helpfulness, structure, and source attribution.

Run:
    python -m evals.quality
"""

from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIResponses

from agents.scout import scout
from agents.seek import seek
from db import get_postgres_db

eval_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Scout: Enterprise knowledge agent quality
# ---------------------------------------------------------------------------
scout_quality_eval = AgentAsJudgeEval(
    db=eval_db,
    name="Scout - Answer Quality",
    model=OpenAIResponses(id="gpt-5.2"),
    criteria=(
        "Response should answer the question directly with specific details "
        "(numbers, dates, policy specifics) and reference the source document."
    ),
    scoring_strategy="numeric",
    threshold=7,
    additional_guidelines=[
        "A good answer summarizes the policy in the agent's own words -- verbatim quotes are NOT required",
        "Must reference a source file path (e.g. company-docs/policies/employee-handbook.md)",
        "Must include concrete details from the document, not vague generalities",
        "Should NOT say 'I couldn't find' if the information exists in the documents",
    ],
)

# ---------------------------------------------------------------------------
# Seek: Deep research agent quality
# ---------------------------------------------------------------------------
seek_quality_eval = AgentAsJudgeEval(
    db=eval_db,
    name="Seek - Research Quality",
    model=OpenAIResponses(id="gpt-5.2"),
    criteria=(
        "Research response should be well-organized, informative, and include source attribution for key claims."
    ),
    scoring_strategy="numeric",
    threshold=7,
    additional_guidelines=[
        "Response should have clear structure (headings, sections, or bullet points)",
        "Key claims should reference where the information came from",
        "Response should distinguish what is well-established from what is uncertain",
        "A thorough overview is good; an exhaustive report is not always necessary",
    ],
)

# ---------------------------------------------------------------------------
# Run: Batch evaluation with multiple test cases per agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Scout batch eval ---
    print("=" * 60)
    print("Scout Quality Eval (batch)")
    print("=" * 60)

    scout_cases = [
        {"question": "What is our PTO policy?"},
        {"question": "How do I request a new laptop?"},
        {"question": "What is the deployment rollback procedure?"},
    ]

    for case in scout_cases:
        q = case["question"]
        print(f"\n  > {q}")
        response = scout.run(q)
        scout_quality_eval.run(
            input=q,
            output=str(response.content),
            print_results=True,
        )

    # --- Seek batch eval ---
    print("\n" + "=" * 60)
    print("Seek Quality Eval (batch)")
    print("=" * 60)

    seek_cases = [
        {"question": "What is Agno?"},
        {"question": "Compare the top AI agent frameworks in 2025"},
    ]

    for case in seek_cases:
        q = case["question"]
        print(f"\n  > {q}")
        response = seek.run(q)
        seek_quality_eval.run(
            input=q,
            output=str(response.content),
            print_results=True,
        )
