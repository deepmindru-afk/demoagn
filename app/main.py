"""
Agno Demo
-------

The main entry point for Agno Demo.

Run:
    python -m app.main
"""

from os import getenv
from pathlib import Path

from agno.os import AgentOS

from agents.dash import dash
from agents.gcode import gcode
from agents.guard import guard
from agents.knowledge import knowledge_agent
from agents.mcp import mcp_agent
from agents.pal import pal
from agents.relay import relay
from agents.scout import scout
from agents.seek import seek
from agents.sentinel import sentinel
from app.registry import registry
from db import get_postgres_db
from teams.research import research_team
from workflows.daily_brief import daily_brief_workflow

# ---------------------------------------------------------------------------
# Create AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    name="AgentOS",
    tracing=True,
    scheduler=True,
    db=get_postgres_db(),
    agents=[knowledge_agent, mcp_agent, dash, gcode, guard, pal, relay, scout, seek, sentinel],
    teams=[research_team],
    workflows=[daily_brief_workflow],
    registry=registry,
    config=str(Path(__file__).parent / "config.yaml"),
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(
        app="app.main:app",
        reload=getenv("RUNTIME_ENV", "prd") == "dev",
    )
