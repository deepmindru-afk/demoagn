"""
Run all evals.

Usage:
    python -m evals
"""

from evals.accuracy import dash_accuracy_eval, scout_accuracy_eval
from evals.quality import scout, scout_quality_eval, seek, seek_quality_eval
from evals.reliability import run_dash_reliability_eval


def main() -> None:
    # --- Accuracy ---
    print("=" * 60)
    print("1. Dash Accuracy Eval")
    print("=" * 60)
    dash_result = dash_accuracy_eval.run(print_results=True, print_summary=True)
    if dash_result:
        print(f"Average score: {dash_result.avg_score}/10\n")

    print("=" * 60)
    print("2. Scout Accuracy Eval")
    print("=" * 60)
    scout_acc_result = scout_accuracy_eval.run(print_results=True, print_summary=True)
    if scout_acc_result:
        print(f"Average score: {scout_acc_result.avg_score}/10\n")

    # --- Reliability ---
    print("=" * 60)
    print("3. Dash Reliability Eval")
    print("=" * 60)
    run_dash_reliability_eval()
    print()

    # --- Quality ---
    print("=" * 60)
    print("4. Scout Quality Eval")
    print("=" * 60)
    scout_response = scout.run("What is our PTO policy?")
    scout_q_result = scout_quality_eval.run(
        input="What is our PTO policy?",
        output=str(scout_response.content),
        print_results=True,
        print_summary=True,
    )
    if scout_q_result:
        print(f"Pass rate: {scout_q_result.pass_rate:.0f}%\n")

    print("=" * 60)
    print("5. Seek Quality Eval")
    print("=" * 60)
    seek_response = seek.run("What is Agno?")
    seek_q_result = seek_quality_eval.run(
        input="What is Agno?",
        output=str(seek_response.content),
        print_results=True,
        print_summary=True,
    )
    if seek_q_result:
        print(f"Pass rate: {seek_q_result.pass_rate:.0f}%\n")

    print("=" * 60)
    print("All evals complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
