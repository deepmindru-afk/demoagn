"""CLI entry point: python -m agents.sentinel"""

from agents.sentinel.agent import sentinel

if __name__ == "__main__":
    sentinel.cli_app(stream=True)
