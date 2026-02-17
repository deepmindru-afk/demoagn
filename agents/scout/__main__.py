"""CLI entry point: python -m agents.scout"""

from agents.scout.agent import scout

if __name__ == "__main__":
    scout.cli_app(stream=True)
