#!/usr/bin/env bash
# Runs plan_v2 CARE analysis for robustness seeds as soon as each seed's panel parts are done (idempotent:
# skips seeds whose summary.json exists). Usage (from Target_Journal_Submission/): nohup bash scripts/care_seed_chain.sh &
cd "$(dirname "$0")/.."
for s in 1 2 3 4; do
  [ -f code/results/plan_v2/care/seed$s/summary.json ] && continue
  until python3 -c "
import json,sys;q=json.load(open('state/queue.json'))
r=[j for j in q['jobs'] if 'run_panel.py care $s ' in j['cmd']+' ']
sys.exit(0 if r and all(j['status']=='done' for j in r) else 1)"; do sleep 60; done
  (cd code && nice -n 5 python3 scripts/plan_v2_analysis.py care $s > ../logs/planv2_care_s$s.log 2>&1)
  echo "care seed $s exit $? $(date -u +%H:%M)" >> logs/planv2_care_chain.log
done
(cd code && python3 scripts/plan_v2_summary.py > ../logs/planv2_summary_last.log 2>&1)
echo "care chain DONE $(date -u +%H:%M)" >> logs/planv2_care_chain.log
