#!/usr/bin/env bash
# Commit and push run outputs every 10 minutes so progress survives a session/usage-limit stop.
cd "$(dirname "$0")/.."
BR=$(git rev-parse --abbrev-ref HEAD)
while true; do
  sleep 600
  git add -A Target_Journal_Submission/results Target_Journal_Submission/results_full_stdout*.log \
    Target_Journal_Submission/tables Target_Journal_Submission/figures PROJECT_STATE.md 2>/dev/null || true
  if ! git diff --cached --quiet; then
    git commit -q -m "Autosave: experiment run checkpoint $(date -u +%H:%M)" \
      -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_01CVvjt3MtzviSjKLxVxQKb7" || true
    for i in 1 2 3 4; do git push -q origin "$BR" && break; sleep $((i*10)); done
  fi
done
