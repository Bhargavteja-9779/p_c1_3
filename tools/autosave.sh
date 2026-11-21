#!/usr/bin/env bash
# Commit and push experiment progress every INTERVAL seconds (default 600) so that work
# survives container resets / usage-limit pauses. Run: setsid nohup tools/autosave.sh &
cd "$(dirname "$0")/.." || exit 1
BR=$(git rev-parse --abbrev-ref HEAD); INTERVAL=${INTERVAL:-600}
while true; do
  sleep "$INTERVAL"
  if [ -n "$(git status --porcelain)" ]; then
    git add -A && git commit -qm "Autosave: experiment progress $(date -u +%F' '%H:%M) UTC

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y77ATz74PaAyJV343yNWx2"
    for i in 1 2 3 4; do git push -q origin "$BR" && break; sleep $((2**i*5)); done
  fi
done
