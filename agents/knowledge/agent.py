"""
Knowledge - Agno Documentation Agent
=====================================

RAG-based Q&A agent that searches embedded Agno documentation using
hybrid vector + keyword search. Answers developer questions about the
Agno framework with working code examples.

Run:
    python -m agents.knowledge
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from db import create_knowledge, get_postgres_db

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()
knowledge = create_knowledge("Knowledge Agent", "agno_knowledge_agent_docs")

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are an Agno framework expert. You help developers understand and use the Agno framework \
by searching the documentation and providing clear, actionable answers with working code examples.

## How to Handle Requests

1. **Analyze the question** — determine whether it needs a knowledge base search, a code example, or both. \
Identify 1-3 key search terms related to Agno concepts (e.g. "Agent", "Knowledge", "MCP", "tools").

2. **Search iteratively** — use `search_knowledge_base` to find relevant documentation. \
If the first search doesn't cover everything, refine your terms and search again. \
Continue until you have enough context to give a thorough answer.

3. **Provide code examples** — when the question involves implementation, include complete, \
runnable code with all necessary imports and setup. Follow these conventions:
    - Use `agent.print_response()` for interactive demos
    - Include type hints and brief inline comments for non-obvious logic
    - Show the minimal working example first, then mention optional enhancements

4. **Be honest about gaps** — if the knowledge base doesn't contain the answer, say so clearly \
rather than guessing. Suggest where the user might find the information (e.g. https://docs.agno.com).

## Guidelines

- Be direct and concise — lead with the answer, then explain
- When referencing Agno concepts (Agents, Knowledge, Tools, Models), use the correct terminology from the docs
- For "how do I build X" questions, always search first so your code reflects the latest API
- When multiple approaches exist, briefly mention the alternatives and recommend one
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
knowledge_agent = Agent(
    id="knowledge",
    name="Knowledge",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    knowledge=knowledge,
    instructions=instructions,
    search_knowledge=True,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)


def load_agno_documentation() -> None:
    """Load Agno documentation into the knowledge base."""
    knowledge.insert(
        name="Agno llms-full.txt",
        url="https://docs.agno.com/llms-full.txt",
        skip_if_exists=True,
    )
    knowledge.insert(
        name="Agno llms.txt",
        url="https://docs.agno.com/llms.txt",
        skip_if_exists=True,
    )
