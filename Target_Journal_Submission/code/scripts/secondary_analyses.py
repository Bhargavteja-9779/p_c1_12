"""Pre-registered secondary analyses (protocol v1 'Robustness / generalisation / other analyses', A4 pooled).
Thresholds always come from M1 (B in {1, 2, 4}); nothing here selects or tunes anything.

1. Per-fault detections at the M1-chosen operating points, M1 (cross-fitted / online) and M2 (locked)
   -> results/secondary_fault_detections.csv
2. Cold start: recall and false-alarm rate by days of own history (days since the substation's first record)
   -> results/secondary_cold_start.csv
3. Pooled M1+M2 threshold-free paired comparisons (HF1-HF3 pairs, Wilcoxon on log10 rank fractions; ranks are
   computed within each manufacturer)  -> results/secondary_pooled_ranks.csv
4. Error analysis by fault label (M1+M2, B = 2)  -> results/secondary_by_label.csv
Usage: secondary_analyses.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import wilcoxon
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.evaluation.diagnose import fault_ranks
from src.models import online as O
sys.argv = sys.argv[:1] + ["2"]  # m2_evaluate parses M at import; the locked script is left unchanged
sys.path.insert(0, os.path.dirname(__file__))
from m2_evaluate import CELLS, HF1, HF2, HF3, name_on

BINS = [0, 90, 365, 100000]; BLAB = ["<90 d", "90-365 d", ">365 d"]


def chosen_points():
    out = {}
    for cell in CELLS:
        t, _ = R.best_at_budgets(name_on(cell, 1), 1)
        out[cell] = {int(r.budget): (r.tau, int(r.c_thr)) for r in t.itertuples()}
    return out


def run():
    ch = chosen_points()
    det_rows, fa_rows = [], []
    for M in (1, 2):
        for cell in CELLS:
            for s in P.substations(M):
                sc = R.load_scores(name_on(cell, M), M, s); lab = C.substation_labels(M, s, sc.index)
                t0 = sc.index.min()
                for B, (tau, c) in ch[cell].items():
                    k = O.criticality_counter(sc, tau)
                    r = C.evaluate_substation(pd.Series(k >= c, index=sc.index), lab)
                    for d in r["detections"]:
                        det_rows.append(dict(m=M, cell=cell, budget=B, sub=s, event_id=d["event_id"], detected=d["detected"],
                                             lead_h=d["lead_h"], history_days=(d["report"] - t0).days))
                    if B == 2:
                        # false alarms and exposure by history bin
                        blocked = list(zip(lab.targets["win_start"], lab.targets["report"])) + lab.exclusions
                        days = pd.Series(1, index=sc[(sc.index >= lab.start) & (sc.index <= lab.end)].index).resample("D").count()
                        days = [d for d in days[days > 0].index if not any(a <= d + pd.Timedelta(hours=12) < b for a, b in blocked)]
                        hd = np.array([(d - t0).days for d in days]); fd = np.array([(f - t0).days for f in r["false_alarms"]])
                        for i, lb in enumerate(BLAB):
                            fa_rows.append(dict(m=M, cell=cell, sub=s, bin=lb, expo_days=int(((hd >= BINS[i]) & (hd < BINS[i + 1])).sum()),
                                                n_fa=int(((fd >= BINS[i]) & (fd < BINS[i + 1])).sum()) if len(fd) else 0))
            print("tabulated", M, cell, flush=True)
    D = pd.DataFrame(det_rows); D.to_csv("results/secondary_fault_detections.csv", index=False)
    Fa = pd.DataFrame(fa_rows)
    D2 = D[D.budget == 2].copy(); D2["bin"] = pd.cut(D2.history_days, BINS, right=False, labels=BLAB)
    rec = D2.groupby(["m", "cell", "bin"], observed=False).agg(n_faults=("detected", "size"), recall=("detected", "mean")).reset_index()
    fa = Fa.groupby(["m", "cell", "bin"]).agg(n_fa=("n_fa", "sum"), expo_days=("expo_days", "sum")).reset_index()
    fa["fa_per_sub_year"] = fa.n_fa / (fa.expo_days / 365.25)
    cs = rec.merge(fa, on=["m", "cell", "bin"], how="outer"); cs.to_csv("results/secondary_cold_start.csv", index=False)
    with pd.option_context("display.width", 200):
        print(cs.pivot_table(index="cell", columns=["m", "bin"], values=["recall", "fa_per_sub_year"], observed=False).round(2).to_string())
    # pooled threshold-free ranks
    rk = {}
    for cell in CELLS:
        rk[cell] = pd.concat([fault_ranks(name_on(cell, M), M)[0].assign(m=M) for M in (1, 2)]).set_index(["m", "event_id"])["rank_frac"]
    rows = []
    for fam, pairs in (("HF1", HF1), ("HF2", HF2), ("HF3", HF3)):
        for a, b in pairs:
            d = np.log10(rk[a].clip(lower=1e-5)) - np.log10(rk[b].clip(lower=1e-5))
            rows.append(dict(family=fam, a=a, b=b, n=len(d), a_better=int((d < 0).sum()), b_better=int((d > 0).sum()),
                             median_rank_a=rk[a].median(), median_rank_b=rk[b].median(),
                             p_wilcoxon=wilcoxon(d[d != 0]).pvalue if (d != 0).sum() else 1.0))
    T = pd.DataFrame(rows); T.to_csv("results/secondary_pooled_ranks.csv", index=False); print(T.round(4).to_string(index=False))
    # by fault label (B = 2)
    F = pd.concat([P.faults(M)[["Event ID", "Fault label"]].assign(m=M) for M in (1, 2)]).rename(columns={"Event ID": "event_id"})
    L = D2.merge(F, on=["m", "event_id"], how="left").pivot_table(index="Fault label", columns="cell", values="detected", aggfunc="sum")
    L.insert(0, "n", D2[D2.cell == "rule"].merge(F, on=["m", "event_id"]).groupby("Fault label").size())
    L.to_csv("results/secondary_by_label.csv"); print(L.to_string())


if __name__ == "__main__":
    run()
