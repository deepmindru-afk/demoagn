# Agno Demo

A multi-agent system built with [Agno](https://docs.agno.com), deployable to Railway.

## Get Started

```sh
# Clone the repo
git clone https://github.com/agno-agi/demo.git agno-demo
cd agno-demo

# Add OPENAI_API_KEY
cp example.env .env
# Edit .env and add your key

# Start the application
docker compose up -d --build

# Load documents for the knowledge agent
docker exec -it agno-demo-api python -m agents.knowledge.scripts.load_knowledge
```

Confirm AgentOS is running at [http://localhost:8000/docs](http://localhost:8000/docs).

### Connect to the Web UI

1. Open [os.agno.com](https://os.agno.com) and login
2. Add OS → Local → `http://localhost:8000`
3. Click "Connect"

## Deploy to Railway

Requires:
- [Railway CLI](https://docs.railway.com/guides/cli)
- `OPENAI_API_KEY` set in your environment

```sh
railway login

./scripts/railway_up.sh
```

The script provisions PostgreSQL, configures environment variables, and deploys your application.

### Connect to the Web UI

1. Open [os.agno.com](https://os.agno.com)
2. Click "Add OS" → "Live"
3. Enter your Railway domain

### Manage deployment

```sh
railway logs --service agno-demo      # View logs
railway open                         # Open dashboard
railway up --service agno-demo -d    # Update after changes
```

To stop services:
```sh
railway down --service agno-demo
railway down --service pgvector
```

### Production Operations

**Load data and knowledge:**
```sh
# Knowledge agent — Agno documentation
railway run python -m agents.knowledge.scripts.load_knowledge

# Dash — table schemas, validated queries, and business rules
railway run python -m agents.dash.scripts.load_knowledge

# Dash — F1 data (1950-2020)
railway run python -m agents.dash.scripts.load_data

# Scout — source metadata, routing rules, and patterns
railway run python -m agents.scout.scripts.load_knowledge
```

**View logs:**
```sh
railway logs --service agno-demo
```

**Run commands in production:**
```sh
railway run python -m app.main  # CLI mode
```

**Redeploy after changes:**
```sh
railway up --service agno-demo -d
```

**Open dashboard:**
```sh
railway open
```

## What's Included

### Agents

| Agent | Description |
|-------|-------------|
| **Knowledge** | Answers questions about Agno using Agentic RAG |
| **MCP** | Queries the Agno docs using the Agno MCP Server |
| **Dash** | Self-learning data analyst — queries structured data with SQL and learns from validated results |
| **Gcode** | Lightweight coding agent — writes, reviews, and iterates on code in an isolated workspace |
| **Pal** | Personal knowledge agent — remembers preferences, saves notes, and manages user context |
| **Scout** | Enterprise knowledge agent — searches and synthesizes internal documents |
| **Seek** | Deep research agent — conducts multi-source research and produces structured reports |
| **Guard** | HITL demo — confirms restarts, collects user input, runs external diagnostics |
| **Relay** | User feedback demo — collects structured preferences via ask_user before planning |
| **Sentinel** | Approvals demo — gates refunds, deletions, and exports behind approval workflows |

#### Agent Details

<details>
<summary><strong>Knowledge</strong> — framework Q&A using RAG</summary>

Searches embedded Agno documentation using hybrid vector + keyword search. Answers developer questions about the Agno framework with working code examples.

**Knowledge:** `agno_knowledge_agent_docs`

**Operations:**

```sh
docker exec -it agno-demo-api python -m agents.knowledge.scripts.load_knowledge
```

**Try it:**
- "What is Agno?"
- "Tell me about Learning Machines"
- "Summarize the key features of Agno"

</details>

<details>
<summary><strong>MCP</strong> — framework expert via live docs</summary>

Queries docs.agno.com directly through MCP, so answers always reflect the latest documentation. No local knowledge base needed.

**Tools:** MCP connection to `docs.agno.com/mcp`

**Try it:**
- "What is Agno?"
- "Tell me about Learning Machines"
- "Summarize the key features of Agno"

</details>

<details>
<summary><strong>Dash</strong> — self-learning data analyst</summary>

SQL-based data agent that provides insights, not just query results. Ships with Formula 1 race data (1950–2020). Learns from errors, type gotchas, and user corrections.

**Tools:** SQL queries, schema introspection, Exa web search
**Knowledge:** `dash_knowledge`, `dash_learnings`

**Operations:**

```sh
# Load table schemas, validated queries, and business rules
docker exec -it agno-demo-api python -m agents.dash.scripts.load_knowledge

# Load F1 data (1950-2020)
docker exec -it agno-demo-api python -m agents.dash.scripts.load_data
```

**Try it:**
- "Who won the most F1 races in 2019?"
- "Show the points gap between Hamilton and Verstappen by season"
- "Which circuits had the most DNFs in 2020?"

</details>

<details>
<summary><strong>Gcode</strong> — lightweight coding agent</summary>

Writes, reviews, and iterates on code in an isolated `/workspace` directory. Each project is a git repo with worktree-based task isolation. Learns project conventions and gotchas as it works.

**Tools:** CodingTools, ReasoningTools
**Knowledge:** `gcode_knowledge`, `gcode_learnings`

**Try it:**
- "Build a command-line todo app: add, list, done, delete. Persist to JSON. Write pytest tests and run them."
- "Create a Python library that parses and evaluates math expressions like '2 + 3 * (4 - 1)', with tests."
- "Build a URL shortener with an in-memory store: shorten, resolve, list stats. Include a demo script."

</details>

<details>
<summary><strong>Pal</strong> — personal knowledge agent</summary>

Saves notes, bookmarks, people, and projects into `pal_`-prefixed tables it creates on demand. Over time the database becomes a structured map of the user's world. Also searches the web via Exa.

**Tools:** SQL (dynamic table creation), Exa web search
**Knowledge:** `pal_knowledge`, `pal_learnings`

**Try it:**
- "Save a note: quarterly planning meeting moved to Friday 3pm"
- "What notes have I saved recently?"
- "Save a bookmark: https://docs.agno.com -- Agno documentation"

</details>

<details>
<summary><strong>Scout</strong> — enterprise knowledge navigator</summary>

Finds answers — not just files — across internal documents. Navigates folder structures, reads full documents, and remembers which search paths work. Learns routing rules and source locations over time.

**Tools:** File operations, content search, source navigation, Exa web search
**Knowledge:** `scout_knowledge`, `scout_learnings`

**Operations:**

```sh
# Load source metadata, routing rules, and patterns
docker exec -it agno-demo-api python -m agents.scout.scripts.load_knowledge

# Recreate from scratch
docker exec -it agno-demo-api python -m agents.scout.scripts.load_knowledge --recreate
```

**Try it:**
- "What is our PTO policy?"
- "Find the incident response runbook"
- "How do I request a new laptop?"

</details>

<details>
<summary><strong>Seek</strong> — deep research agent</summary>

Conducts exhaustive multi-source research and produces structured, well-sourced reports. Uses web search, company/people research, URL crawling, and parallel search — all via Exa. Learns which sources are reliable and what research patterns work.

**Tools:** Web search, company research, people search, URL crawling, parallel search (all via Exa)
**Knowledge:** `seek_knowledge`, `seek_learnings`

**Try it:**
- "What is Agno?"
- "Compare agno to other agent frameworks"
- "How do I build the best agentic system?"

</details>

<details>
<summary><strong>Guard</strong> — human-in-the-loop demo</summary>

IT operations helpdesk agent demonstrating all three HITL patterns: confirmation (service restarts), user input (ticket priority), and external execution (diagnostics).

**Tools:** restart_service, create_support_ticket, run_diagnostic, UserFeedbackTools

**Try it:**
- "The auth service is timing out, can you check it?"
- "Create a support ticket for the slow dashboard"
- "Run diagnostics on the payment service"

</details>

<details>
<summary><strong>Relay</strong> — user feedback demo</summary>

Planning concierge that collects structured preferences via `ask_user` before making recommendations. Demonstrates Agno's UserFeedbackTools for presenting choices with predefined options.

**Tools:** UserFeedbackTools (ask_user)

**Try it:**
- "Plan a weekend trip to Tokyo"
- "Help me plan a team dinner"
- "Organize a birthday party for 20 people"

</details>

<details>
<summary><strong>Sentinel</strong> — approvals demo</summary>

Compliance and finance agent that gates sensitive operations behind approval workflows. Refunds and account deletions require explicit approval; data exports and reports are logged to an audit trail.

**Tools:** process_refund, delete_user_account, export_customer_data, generate_report

**Try it:**
- "Process a $150 refund for customer C-1234"
- "Delete the account for user U-5678"
- "Export all data for customer C-9012"

</details>

### Teams

| Team | Description |
|------|-------------|
| **Research Team** | Coordinates Seek and Scout to combine external research with internal knowledge |

### Workflows

| Workflow | Description |
|----------|-------------|
| **Daily Brief** | Scheduled morning briefing — calendar, email, news, and priorities |

## Common Tasks

<details>
<summary><strong>Add your own agent</strong></summary>

1. Create `agents/my_agent/` with three files:

**`agents/my_agent/agent.py`**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from db import get_postgres_db

my_agent = Agent(
    id="my-agent",
    name="My Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    db=get_postgres_db(),
    instructions="You are a helpful assistant.",
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
    enable_agentic_memory=True,
)
```

**`agents/my_agent/__init__.py`**
```python
from agents.my_agent.agent import my_agent
```

**`agents/my_agent/__main__.py`**
```python
from agents.my_agent.agent import my_agent

my_agent.print_response("Hello!", stream=True)
```

2. Register in `app/main.py`:

```python
from agents.my_agent import my_agent

agent_os = AgentOS(
    agents=[..., my_agent],
    ...
)
```

3. Add quick prompts to `app/config.yaml` using the agent's `id`

4. Restart: `docker compose restart`

</details>

<details>
<summary><strong>Add tools to an agent</strong></summary>

Agno includes 100+ tool integrations. See the [full list](https://docs.agno.com/tools/toolkits).

```python
from agno.tools.slack import SlackTools
from agno.tools.google_calendar import GoogleCalendarTools

my_agent = Agent(
    ...
    tools=[
        SlackTools(),
        GoogleCalendarTools(),
    ],
)
```

</details>

<details>
<summary><strong>Add dependencies</strong></summary>

1. Edit `pyproject.toml`
2. Regenerate requirements: `./scripts/generate_requirements.sh`
3. Rebuild: `docker compose up -d --build`

</details>

<details>
<summary><strong>Use a different model provider</strong></summary>

1. Add your API key to `.env` (e.g., `ANTHROPIC_API_KEY`)
2. Update agents to use the new provider:

```python
from agno.models.anthropic import Claude

model=Claude(id="claude-sonnet-4-5")
```
3. Add dependency: `anthropic` in `pyproject.toml`

</details>

---

## Local Development

For development without Docker:

```sh
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
./scripts/venv_setup.sh
source .venv/bin/activate

# Start PostgreSQL (required)
docker compose up -d agno-demo-db

# Run the app
python -m app.main
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `GITHUB_TOKEN` | No | - | GitHub PAT for Gcode to clone private repos ([setup](#giving-gcode-access-to-github)) |
| `PORT` | No | `8000` | API server port |
| `DB_HOST` | No | `localhost` | Database host |
| `DB_PORT` | No | `5432` | Database port |
| `DB_USER` | No | `ai` | Database user |
| `DB_PASS` | No | `ai` | Database password |
| `DB_DATABASE` | No | `ai` | Database name |
| `RUNTIME_ENV` | No | `prd` | Set to `dev` for auto-reload |

<details>
<summary><strong>Giving Gcode access to GitHub</strong></summary>

Gcode can clone and push to GitHub repos when you provide a **Fine-grained Personal Access Token**. Do not use a Classic PAT — fine-grained tokens let you scope access to specific repos.

### Create the token

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → [Fine-grained tokens](https://github.com/settings/personal-access-tokens/new)**
2. Click **Generate new token**

### Configure it

| Field | Value |
|-------|-------|
| **Token name** | `gcode` (or whatever helps you identify it) |
| **Expiration** | 90 days (set a calendar reminder to rotate) |
| **Repository access** | **Only select repositories** — pick the repos Gcode should work on |

### Set permissions

| Permission | Access | Why |
|-----------|--------|-----|
| **Contents** | Read and write | Clone, read files, commit, push |
| **Metadata** | Read-only | Required by GitHub for all token operations |

That's it — two permissions. Add more only if needed (e.g., **Pull requests** read/write for opening PRs).

### Pass it to Gcode

Add it to your `.env` file:

```bash
GITHUB_TOKEN=github_pat_xxxxxxxxxxxxxxxxxxxxx
```

The container's git credential helper reads this from the environment at runtime. The token is never written to disk — Gcode just runs `git clone https://github.com/...` and authentication happens transparently.

### Rotating tokens

When a token expires, generate a new one with the same settings, update `.env`, and restart: `docker compose up -d`.

</details>

## Learn More

- [Agno Documentation](https://docs.agno.com)
- [AgentOS Documentation](https://docs.agno.com/agent-os/introduction)
- [Agno Discord](https://agno.com/discord)
