#!/usr/bin/env python3
"""Print project status from state/ files only (safe, read-only). Usage: python scripts/status.py"""
import collections, json, os, subprocess, time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = lambda *p: os.path.join(ROOT, "state", *p)


def load(p, d=None):
    try:
        return json.load(open(p))
    except Exception:
        return d


st = load(S("agent_state.json"), {})
print("== agent:", json.dumps({k: st.get(k) for k in ("status", "cycle", "phase", "step", "last_action", "updated")}, indent=1))
q = load(S("queue.json"), {"jobs": []})
by = collections.defaultdict(collections.Counter)
for j in q["jobs"]:
    by[j["group"]][j["status"]] += 1
print("== queue:")
for g, c in by.items():
    print(f"  {g}: {dict(c)}")
for j in q["jobs"]:
    if j["status"] == "running":
        print(f"  RUNNING pid={j.get('pid')} {j['cmd']}")
    if j["status"] == "failed":
        print(f"  FAILED  {j['id']} {j['cmd']}  (log: logs/jobs/{j['id']}.log)")
b = load(S("budget.json"), {})
if b:
    cyc = b.get("cycles", {})
    tot = sum(x.get("machine_h", 0) for x in cyc.values())
    cur = cyc.get(str(b.get("cycle")), {})
    print(f"== budget: cycle {b.get('cycle')}: {cur.get('machine_h', 0):.2f}/{b.get('cycle_budget_h')} machine-h, "
          f"core-h {cur.get('core_h', 0):.1f}; global ledgered {tot:.2f}/{b.get('global_ceiling_h')} h")
try:
    hb = open(S("heartbeat")).read().strip()
    age = time.time() - os.path.getmtime(S("heartbeat"))
    print(f"== heartbeat: {hb} (age {age/60:.1f} min){'  <-- STALE (>20 min): restart runner' if age > 1200 else ''}")
except FileNotFoundError:
    print("== heartbeat: none (no runner has run on this machine)")
r = subprocess.run("tmux ls 2>/dev/null", shell=True, capture_output=True, text=True).stdout.strip()
print("== tmux sessions:", r or "none")
print("== gates: see HANDOFF.md section 'Gate status'")
