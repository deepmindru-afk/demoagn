"""Exa MCP integration helpers."""

from os import getenv

from agno.tools.mcp import MCPTools


def get_exa_mcp_tools(tools: str = "web_search_exa") -> list:
    """Return MCPTools for Exa if API key is available, else empty list."""
    key = getenv("EXA_API_KEY", "")
    if not key:
        return []
    return [MCPTools(url=f"https://mcp.exa.ai/mcp?exaApiKey={key}&tools={tools}")]
