"""CLI entry point: python -m agents.guard"""

from agents.guard.agent import guard

if __name__ == "__main__":
    guard.cli_app(stream=True)
