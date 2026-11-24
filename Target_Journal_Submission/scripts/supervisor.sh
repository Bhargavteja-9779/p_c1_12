#!/usr/bin/env bash
# Layer B supervisor: restarts the agent CLI headlessly until state/agent_state.json says FINISHED.
# Start:  tmux new-session -d -s supervisor "bash scripts/supervisor.sh"     (from Target_Journal_Submission/)
# Stop:   touch state/STOP_SUPERVISOR   (or: tmux kill-session -t supervisor)
#
# HONEST LIMITS (see HANDOFF.md): in a claude.ai cloud container this only lives as long as the container;
# the container is reclaimed after inactivity, so it does not survive an account switch. On a machine you own,
# install it with scripts/install_autostart.sh. Never run it while an interactive agent session is working in
# the same checkout (two agents would edit the same files).
set -u
cd "$(dirname "$0")/.."
LOG=logs/supervisor.log; mkdir -p logs
CLI=""
for c in claude; do command -v "$c" >/dev/null 2>&1 && CLI="$c" && break; done
if [ -z "$CLI" ]; then echo "$(date -u +%FT%TZ) no headless agent CLI found; paste BOOTSTRAP_PROMPT.txt manually" | tee -a "$LOG"; exit 1; fi
delays=(300 900 1800 3600); i=0
while true; do
  [ -f state/STOP_SUPERVISOR ] && { echo "$(date -u +%FT%TZ) stop file found" >> "$LOG"; exit 0; }
  grep -q '"status": *"FINISHED"' state/agent_state.json 2>/dev/null && { echo "$(date -u +%FT%TZ) FINISHED" >> "$LOG"; exit 0; }
  echo "$(date -u +%FT%TZ) starting $CLI (attempt after delay index $i)" >> "$LOG"
  out=$(mktemp)
  "$CLI" -p "$(cat BOOTSTRAP_PROMPT.txt)" --dangerously-skip-permissions > "$out" 2>&1; rc=$?
  tail -n 20 "$out" >> "$LOG"; echo "$(date -u +%FT%TZ) agent exited rc=$rc" >> "$LOG"
  # If the CLI printed a reset time ("resets at 3pm" / ISO time), sleep until then; else exponential backoff.
  reset=$(grep -oiE 'reset[s]? (at )?[0-9]{1,2}(:[0-9]{2})? ?(am|pm)?' "$out" | head -1 | grep -oiE '[0-9]{1,2}(:[0-9]{2})? ?(am|pm)?$')
  rm -f "$out"
  if [ -n "$reset" ] && t=$(date -d "$reset" +%s 2>/dev/null); then
    now=$(date +%s); [ "$t" -le "$now" ] && t=$((t+86400)); s=$((t-now+60))
    echo "$(date -u +%FT%TZ) usage limit; sleeping ${s}s until reset ($reset)" >> "$LOG"; sleep "$s"; i=0; continue
  fi
  d=${delays[$i]}; [ $i -lt 3 ] && i=$((i+1))
  [ $rc -eq 0 ] && i=0 && d=300
  echo "$(date -u +%FT%TZ) sleeping ${d}s" >> "$LOG"; sleep "$d"
done
