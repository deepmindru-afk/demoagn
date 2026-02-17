"""CLI entry point: python -m agents.relay"""

from agents.relay.agent import relay

if __name__ == "__main__":
    relay.cli_app(stream=True)
