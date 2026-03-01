"""CLI entry point: python -m agents.support"""

from agents.support.agent import support

if __name__ == "__main__":
    support.cli_app(stream=True)
