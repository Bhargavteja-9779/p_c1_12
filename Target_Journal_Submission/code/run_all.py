"""Regenerate all results from the raw PreDist data.

  python3 run_all.py --mode quick   # fast methods only, seed 0, M1 + M2 (~15 min on 4 CPU cores)
  python3 run_all.py --mode full    # every factorial cell, fleet-model seeds 0-9, locked M2 evaluation (~10 h)

Compute device: all models run on CPU (the autoencoders are small); torch uses CUDA/MPS automatically if
present, but results in the paper were produced on CPU. Steps whose outputs exist are skipped (delete
results/scores/<method> to force a rerun).
"""
import argparse, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
FAST = ["rule", "sigma3", "loop3s", "loop3s_c"]
HEAVY = ["iforest", "qnbm", "ae", "ae_cond", "ae_comfort"]


def sh(cmd):
    print(">>", cmd, flush=True)
    r = subprocess.run(cmd, shell=True, cwd=HERE)
    if r.returncode:
        sys.exit(f"step failed: {cmd}")


def par(cmds, n):
    with ThreadPoolExecutor(n) as ex:
        list(ex.map(sh, cmds))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    a = ap.parse_args(); full = a.mode == "full"
    sh(f"bash scripts/download_data.sh && {sys.executable} scripts/build_cache.py")
    py = sys.executable
    methods = FAST + (HEAVY if full else [])
    seeds = range(10) if full else [0]
    # 1. development data (M1): per-substation online detectors, then cross-fitted fleet models
    par([f"{py} scripts/run_online_method.py {m} {M} {k}/2" for M in (1, 2) for m in methods for k in (0, 1)], a.jobs)
    par([f"{py} scripts/run_srcr_components.py {s} && {py} scripts/round2_variants.py "
         f"{'srcr_comp' if s == 0 else f'srcr_comp_seed{s}'} v_g1l_noret,v_gate_1s_local" for s in seeds], max(1, a.jobs // 2))
    # 2. locked test (M2): fleet models trained on all M1 normal data, applied unchanged
    par([f"{py} scripts/run_m2_fleet.py {s}" for s in seeds], max(1, a.jobs // 2))
    # 3. pre-registered analysis
    if full:
        sh(f"{py} scripts/m2_evaluate.py 2")
    sh(f"{py} -m pytest -q tests")


if __name__ == "__main__":
    main()
