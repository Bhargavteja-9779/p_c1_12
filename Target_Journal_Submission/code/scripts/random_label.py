"""Random-label test (pre-registered addendum, RECHECK/stage4/preregistration_E.md).

At the locked operating points (tau, c_thr chosen on M1 per budget), each target fault's 7-day detection window is
moved to a random eligible normal week of the SAME substation (non-overlapping 7-day blocks inside the monitored
span, outside detection windows and exclusion intervals). Recall is recomputed; 200 permutations.
A detector whose real recall is inside the permutation distribution shows no skill on that manufacturer.
Usage: random_label.py [n_perm]  -> results/random_label.csv
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O
from m2_evaluate import CELLS, name_on

NPERM = int(sys.argv[1]) if len(sys.argv) > 1 else 200
W = pd.Timedelta(days=7)
RES = os.path.join(os.path.dirname(__file__), "..", "results")


def eligible_weeks(lab):
    blocked = list(zip(lab.targets["win_start"], lab.targets["report"])) + lab.exclusions
    out, t = [], lab.start
    while t + W <= lab.end:
        if not any(a < t + W and t < b for a, b in blocked):
            out.append(t)
        t += W
    return out


def main():
    ops = pd.read_csv(os.path.join(RES, "locked_m2_operating_points.csv"))
    rng = np.random.default_rng(20261123)
    rows = []
    for m in (1, 2):
        for cell in CELLS:
            name = name_on(cell, m)
            subs = []
            for s in P.substations(m):
                sc = R.load_scores(name, m, s); lab = C.substation_labels(m, s, sc.index)
                if len(lab.targets) == 0: continue
                subs.append((s, sc, lab, eligible_weeks(lab)))
            for _, o in ops[ops.cell == cell].iterrows():
                tau, c = float(o.tau), int(o.c_thr)
                starts = {}
                for s, sc, lab, wk in subs:
                    k = O.criticality_counter(sc, tau)
                    a = pd.Series(k >= c, index=sc.index); a = a[(a.index >= lab.start) & (a.index <= lab.end)]
                    starts[s] = C.alarm_starts(a)
                hit = lambda st, w0: bool(((st >= w0) & (st < w0 + W)).any())
                real = [hit(starts[s], w0) for s, _, lab, _ in subs for w0 in lab.targets["win_start"]]
                n = len(real); perm = []
                for _ in range(NPERM):
                    h = []
                    for s, _, lab, wk in subs:
                        for _w in range(len(lab.targets)):
                            if wk: h.append(hit(starts[s], wk[rng.integers(len(wk))]))
                    perm.append(np.mean(h) if h else np.nan)
                perm = np.array(perm); r = float(np.mean(real))
                rows.append(dict(m=m, cell=cell, budget=o.budget, tau=tau, c_thr=c, n_faults=n, real_recall=r,
                                 perm_mean=np.nanmean(perm), perm_q95=np.nanquantile(perm, 0.95),
                                 p_perm=(1 + np.sum(perm >= r)) / (1 + NPERM)))
                print(rows[-1], flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(RES, "random_label.csv"), index=False)


if __name__ == "__main__":
    main()
