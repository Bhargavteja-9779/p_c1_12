#!/usr/bin/env bash
# Install / remove autostart for Layer A (queue runner) and Layer B (supervisor) via cron @reboot.
# For a machine YOU own. In a claude.ai cloud container there is no persistent boot, so this has no effect there.
#   bash scripts/install_autostart.sh install [--with-supervisor]
#   bash scripts/install_autostart.sh remove
set -eu
P=$(cd "$(dirname "$0")/.." && pwd)
A="@reboot cd $P && tmux new-session -d -s queue 'python3 scripts/queue_runner.py run --workers 4 >> logs/queue_runner.log 2>&1'  # p_c1_12-layerA"
B="@reboot cd $P && tmux new-session -d -s supervisor 'bash scripts/supervisor.sh'  # p_c1_12-layerB"
case "${1:-}" in
  install) { crontab -l 2>/dev/null | grep -v 'p_c1_12-layer'; echo "$A"; [ "${2:-}" = "--with-supervisor" ] && echo "$B"; } | crontab - ; crontab -l ;;
  remove)  crontab -l 2>/dev/null | grep -v 'p_c1_12-layer' | crontab - ; echo removed ;;
  *) echo "usage: $0 install [--with-supervisor] | remove"; exit 1 ;;
esac
