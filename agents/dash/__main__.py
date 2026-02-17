"""CLI entry point: python -m agents.dash"""

from agents.dash.agent import dash

if __name__ == "__main__":
    dash.cli_app(stream=True)
