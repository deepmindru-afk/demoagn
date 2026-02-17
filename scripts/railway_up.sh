#!/bin/bash

############################################################################
#
#    Agno Railway Deployment
#
#    Usage: ./scripts/railway_up.sh
#
#    Prerequisites:
#      - Railway CLI installed
#      - Logged in via `railway login`
#      - OPENAI_API_KEY set in environment
#
############################################################################

set -e

# Colors
ORANGE='\033[38;5;208m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${ORANGE}"
cat << 'BANNER'
     █████╗  ██████╗ ███╗   ██╗ ██████╗
    ██╔══██╗██╔════╝ ████╗  ██║██╔═══██╗
    ███████║██║  ███╗██╔██╗ ██║██║   ██║
    ██╔══██║██║   ██║██║╚██╗██║██║   ██║
    ██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝
BANNER
echo -e "${NC}"

# Load .env if it exists
if [[ -f .env ]]; then
    set -a
    source .env
    set +a
    echo -e "${DIM}Loaded .env${NC}"
fi

# Preflight
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Install: https://docs.railway.app/guides/cli"
    exit 1
fi

if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "OPENAI_API_KEY not set."
    exit 1
fi

echo -e "${BOLD}Initializing project...${NC}"
echo ""
railway init -n "agno-demo"

echo ""
echo -e "${BOLD}Deploying PgVector database...${NC}"
echo ""
railway deploy -t 3jJFCA

echo ""
echo -e "${DIM}Waiting 10s for database...${NC}"
sleep 10

echo ""
echo -e "${BOLD}Creating application service...${NC}"
echo ""
railway add --service agno-demo \
    --variables 'DB_USER=${{pgvector.PGUSER}}' \
    --variables 'DB_PASS=${{pgvector.PGPASSWORD}}' \
    --variables 'DB_HOST=${{pgvector.PGHOST}}' \
    --variables 'DB_PORT=${{pgvector.PGPORT}}' \
    --variables 'DB_DATABASE=${{pgvector.PGDATABASE}}' \
    --variables "DB_DRIVER=postgresql+psycopg" \
    --variables "RUNTIME_ENV=prd" \
    --variables "WAIT_FOR_DB=True" \
    --variables "OPENAI_API_KEY=${OPENAI_API_KEY}" \
    --variables "PORT=8000"

# Pass optional API keys if set
[[ -n "$ANTHROPIC_API_KEY" ]] && railway variables set "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}" --service agno-demo
[[ -n "$GOOGLE_API_KEY" ]]    && railway variables set "GOOGLE_API_KEY=${GOOGLE_API_KEY}" --service agno-demo
[[ -n "$EXA_API_KEY" ]]       && railway variables set "EXA_API_KEY=${EXA_API_KEY}" --service agno-demo
[[ -n "$PARALLEL_API_KEY" ]]  && railway variables set "PARALLEL_API_KEY=${PARALLEL_API_KEY}" --service agno-demo
[[ -n "$GITHUB_TOKEN" ]]      && railway variables set "GITHUB_TOKEN=${GITHUB_TOKEN}" --service agno-demo

echo ""
echo -e "${BOLD}Creating volumes...${NC}"
echo ""
railway volume add --service agno-demo --mount /workspace
railway volume add --service agno-demo --mount /documents

echo ""
echo -e "${BOLD}Deploying application...${NC}"
echo ""
railway up --service agno-demo -d

echo ""
echo -e "${BOLD}Creating domain...${NC}"
echo ""
railway domain --service agno-demo

echo ""
echo -e "${BOLD}Done.${NC} Domain may take ~5 minutes."
echo -e "${DIM}Logs: railway logs --service agno-demo${NC}"
echo ""
