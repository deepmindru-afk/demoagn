"""CLI entry point: python -m agents.seek"""

from agents.seek.agent import seek

if __name__ == "__main__":
    seek.cli_app(stream=True)
