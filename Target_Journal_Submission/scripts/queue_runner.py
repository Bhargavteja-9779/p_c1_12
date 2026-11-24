#!/usr/bin/env python3
"""Layer A job queue (no LLM needed). Safe to run twice: a lock file prevents two copies.

  python scripts/queue_runner.py add --group G --cwd code --file code/scripts/jobs.txt [--cycle N]
  python scripts/queue_runner.py run [--workers 4]        # detached: see HANDOFF.md
  python scripts/queue_runner.py reset-running            # after a crash: running -> pending

Jobs are shell commands. Every job script in this project skips outputs that already exist, so a
re-run resumes at per-asset granularity (that is the checkpoint unit; no job holds state only in memory).
Budget = machine wall-hours while >= 1 job runs (decision D-2026-11-24-04), plus CPU-core-hours from rusage.
"""
import argparse, fcntl, hashlib, json, os, subprocess, sys, threading, time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "state")
QF, BF, HB, LOCK = (os.path.join(ST, n) for n in ("queue.json", "budget.json", "heartbeat", "queue.lock"))
LOGD = os.path.join(ROOT, "logs", "jobs")
MAX_ATTEMPTS = 3  # first try + 2 retries
_mu = threading.Lock()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(p, default):
    try:
        with open(p) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save(p, obj):  # atomic: temp file -> rename
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, p)


def budget():
    return load(BF, {"cycle": 4, "cycle_budget_h": 15, "global_ceiling_h": 120, "cycles": {},
                     "note": "machine wall-hours with >=1 job running; core_h = CPU user+sys"})


def add(a):
    q = load(QF, {"jobs": []}); ids = {j["id"] for j in q["jobs"]}; n = 0
    for line in open(a.file):
        cmd = line.strip()
        if not cmd or cmd.startswith("#"):
            continue
        jid = a.group + "-" + hashlib.sha1((a.cwd + "|" + cmd).encode()).hexdigest()[:10]
        if jid in ids:
            continue
        q["jobs"].append({"id": jid, "group": a.group, "cycle": a.cycle, "cwd": a.cwd, "cmd": cmd,
                          "status": "pending", "attempts": 0, "added": now()}); n += 1
    save(QF, q); print(f"added {n} jobs to group {a.group}")


def reset_running(_=None):
    q = load(QF, {"jobs": []})
    for j in q["jobs"]:
        if j["status"] == "running":
            j["status"] = "pending"
    save(QF, q)


def run(a):
    os.makedirs(LOGD, exist_ok=True)
    lk = open(LOCK, "w")
    try:
        fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another queue_runner holds the lock; exiting"); return
    lk.write(str(os.getpid())); lk.flush()
    reset_running()  # anything 'running' belongs to a dead runner
    active = {}  # id -> Popen
    stop = threading.Event()

    def beat():
        last = time.time()
        while not stop.is_set():
            time.sleep(30)
            with _mu:
                t = time.time(); dt = t - last; last = t
                with open(HB, "w") as f:
                    f.write(now() + f" pid={os.getpid()} running={len(active)}\n")
                if active:
                    b = budget(); c = b["cycles"].setdefault(str(b["cycle"]), {"machine_h": 0.0, "core_h": 0.0})
                    c["machine_h"] += dt / 3600; save(BF, b)
    th = threading.Thread(target=beat, daemon=True); th.start()

    def over_budget():
        b = budget(); c = b["cycles"].get(str(b["cycle"]), {"machine_h": 0})
        tot = sum(x["machine_h"] for x in b["cycles"].values()) + b.get("prior_h_unledgered", 0)
        return c["machine_h"] >= b["cycle_budget_h"] or tot >= b["global_ceiling_h"]

    while True:
        with _mu:
            q = load(QF, {"jobs": []}); byid = {j["id"]: j for j in q["jobs"]}
            # reap finished
            for jid, p in list(active.items()):
                r = p.poll()
                if r is None:
                    continue
                j = byid[jid]; ru = p.rusage if hasattr(p, "rusage") else None
                j["finished"] = now(); j["returncode"] = r
                j["status"] = "done" if r == 0 else ("failed" if j["attempts"] >= MAX_ATTEMPTS else "pending")
                del active[jid]
            pend = [j for j in q["jobs"] if j["status"] == "pending" and j["id"] not in active]
            if over_budget():
                for j in pend:
                    j["status"] = "skipped_budget"
                pend = []
            while pend and len(active) < a.workers:
                j = pend.pop(0); j["attempts"] += 1; j["status"] = "running"; j["started"] = now()
                log = open(os.path.join(LOGD, j["id"] + ".log"), "a")
                log.write(f"\n=== {now()} attempt {j['attempts']}: {j['cmd']}\n"); log.flush()
                active[j["id"]] = subprocess.Popen(j["cmd"], shell=True, cwd=os.path.join(ROOT, j["cwd"]),
                                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                j["pid"] = active[j["id"]].pid
            save(QF, q)
            if not active and not pend:
                break
        time.sleep(10)
    stop.set()
    # CPU core-hours of all children (cumulative for this runner process)
    import resource
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    b = budget(); c = b["cycles"].setdefault(str(b["cycle"]), {"machine_h": 0.0, "core_h": 0.0})
    c["core_h"] += (ru.ru_utime + ru.ru_stime) / 3600; save(BF, b)
    print("queue empty; runner exits")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add"); p.add_argument("--group", required=True); p.add_argument("--cwd", default="code")
    p.add_argument("--file", required=True); p.add_argument("--cycle", type=int, default=4)
    p = sp.add_parser("run"); p.add_argument("--workers", type=int, default=4)
    sp.add_parser("reset-running")
    a = ap.parse_args(); {"add": add, "run": run, "reset-running": reset_running}[a.cmd](a)
