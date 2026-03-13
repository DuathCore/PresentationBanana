#!/bin/bash
# Launch Claude Code Agent Team for Scientific Presentation
cd /home/marek/PresentationBanana
unset CLAUDECODE
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
export GOOGLE_API_KEY=$(grep GOOGLE_API_KEY .env 2>/dev/null | cut -d= -f2)
PROMPT=$(cat prompts/scientific-presentation-teams.md)
claude --dangerously-skip-permissions -p "$PROMPT" 2>&1 | tee workspace/agent_team.log
echo "=== AGENT TEAM FINISHED ==="
sleep 999999
