"""CLI entry point: python -m agents.gcode"""

from agents.gcode.agent import gcode

if __name__ == "__main__":
    gcode.cli_app(stream=True)
