#!/usr/bin/env bash
# G8 / D-30: leak-free PreDist plan_v2 analysis for seeds 0-4 (and plan_v3 for seed 0). Builds a scratch copy of code/
# whose score files are symlinks to the main tree except subs 4 and 7 (the only subs whose fits change, see
# results/leak_sensitivity/affected_m1.csv), rescores those with PREDIST_EXCL_RULE=leakfree, and runs the unchanged
# analysis scripts there. Waits for each seed's panel jobs. Idempotent. Copies outputs to
# code/results/leak_sensitivity/leakfree_outputs/seed<S>/. Usage (from Target_Journal_Submission/):
#   nohup bash scripts/leak_seed_chain.sh [SCRATCH_DIR] &
set -u
P=$(cd "$(dirname "$0")/.." && pwd); C=$P/code; S=${1:-$P/../.leakfree_tree}; L=$P/logs/leak_seed_chain.log
mkdir -p $S/code/results
[ -f $S/code/.copied ] || { (cd $C && tar cf - --exclude=./data --exclude=./results --exclude='*/__pycache__' .) | (cd $S/code && tar xf -); ln -sfn $C/data $S/code/data; touch $S/code/.copied; }
link_dir() { # $1 = main dir, $2 = scratch dir: symlink every file except s4/s7
  mkdir -p "$2"; for f in "$1"/*; do b=$(basename "$f"); case $b in s4.parquet|s7.parquet) ;; *) ln -sfn "$f" "$2/$b";; esac; done; }
for d in rule loop3s qnbm ae ae_cond; do link_dir $C/results/scores/$d/m1 $S/code/results/scores/$d/m1; done
for s in 0 1 2 3 4; do
  out=$C/results/leak_sensitivity/leakfree_outputs/seed$s
  [ -f $out/summary.json ] && continue
  until python3 -c "
import json,sys;q=json.load(open('$P/state/queue.json'))
r=[j for j in q['jobs'] if 'run_panel.py predist1 $s ' in j['cmd']+' ']
sys.exit(0 if r and all(j['status']=='done' for j in r) else 1)"; do sleep 120; done
  for d in $C/results/scores_panel/predist1/seed$s/*; do link_dir $d $S/code/results/scores_panel/predist1/seed$s/$(basename $d); done
  (cd $S/code && export PREDIST_EXCL_RULE=leakfree && \
   for d in rule loop3s qnbm ae ae_cond; do nice -n 5 python3 scripts/run_online_method.py $d 1 >/dev/null || echo "FAIL $d"; done && \
   nice -n 5 python3 scripts/run_panel.py predist1 $s 0/1 >/dev/null && \
   nice -n 5 python3 scripts/plan_v2_analysis.py predist1 $s > $S/planv2_s$s.log 2>&1 && \
   { [ $s != 0 ] || nice -n 5 python3 scripts/plan_v3_window_arm.py predist1 > $S/planv3.log 2>&1; }) >> $L 2>&1
  mkdir -p $out && cp $S/code/results/plan_v2/predist1/seed$s/* $out/ 2>/dev/null
  [ $s = 0 ] && cp $S/code/results/plan_v3/predist1/summary.json $out/plan_v3_summary.json && cp $S/code/results/plan_v3/predist1/window_arm.csv $out/
  echo "leakfree seed $s done $(date -u +%H:%M) $(ls $out | wc -l) files" >> $L
done
echo "leak chain DONE $(date -u +%H:%M)" >> $L
