"""Bootstrap CIs (resampling substations) for the PreDist protocol gap. DESCRIPTIVE / POST HOC: M1 and M2 outputs
were already seen (M2 burned, state/decisions.md D-03). Usage: protocol_gap_ci.py M
Per method: (a) inflation_same = event precision / continuous alarm precision at the SAME benchmark-chosen (tau, c);
(b) inflation_B2 = event precision (benchmark-chosen) / continuous alarm precision at the in-sample B = 2 point;
plus continuous FA/sub-yr at the benchmark-chosen point. Event-protocol best point re-tuned inside every resample.
Writes results/protocol_gap/m{M}_ci.csv"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O
sys.path.insert(0, os.path.dirname(__file__))
from protocol_gap import events, C_GRID, METHODS

M = int(sys.argv[1]); NBOOT = 2000; rng = np.random.default_rng(0)
OUT = "results/protocol_gap"


def tables(meth):
    E = events(M); ev, cont = [], []
    for s in P.substations(M):
        try:
            sc = R.load_scores(meth, M, s)
        except FileNotFoundError:
            continue
        lab = C.substation_labels(M, s, sc.index); g = E[E["sub"] == s]
        for t in R.TAU_GRID:
            k = O.criticality_counter(sc, t)
            for _, e in g.iterrows():
                w = (sc.index >= e.a) & (sc.index < e.b)
                if not w.any() or np.isnan(sc.values[w]).all():
                    continue
                ev.append({"sub": s, "eid": e.eid, "y": e.fault, "tau": t, "mx": int(k[w].max())})
            for c in C_GRID:
                r = C.evaluate_substation(pd.Series(k >= c, index=sc.index), lab)
                cont.append({"sub": s, "tau": t, "c_thr": c, "n_tgt": len(r["detections"]),
                             "n_det": sum(d["detected"] for d in r["detections"]), "n_fa": len(r["false_alarms"]),
                             "expo": r["exposure_days"]})
    return pd.DataFrame(ev), pd.DataFrame(cont)


def ev_best(ev):
    best = None
    for t, g in ev.groupby("tau"):
        y = g.y.values.astype(bool); mx = g.mx.values
        for c in C_GRID:
            f = mx >= c; tp, fp = (f & y).sum(), (f & ~y).sum()
            p = tp / (tp + fp) if tp + fp else 0.0; r = tp / max(1, y.sum())
            f05 = 1.25 * p * r / (0.25 * p + r) if p + r else 0.0
            if best is None or (f05, r) > (best[2], best[1]):
                best = (p, r, f05, t, c)
    return best


def pooled(cont):
    """per (tau, c): recall, FA/sub-yr, alarm precision."""
    g = cont.groupby(["tau", "c_thr"])[["n_tgt", "n_det", "n_fa", "expo"]].sum()
    g["rec"] = g.n_det / g.n_tgt.clip(lower=1); g["fa"] = g.n_fa / (g.expo / 365.25)
    g["prec"] = g.n_det / (g.n_det + g.n_fa).clip(lower=1)
    return g


def stats(ev, cont):
    p, r, f, t, c = ev_best(ev); g = pooled(cont)
    ok = g[g.fa <= 2].sort_values(["rec", "fa"], ascending=[False, True])
    pb2 = ok.prec.iloc[0] if len(ok) else np.nan
    same = g.loc[(t, c)]
    return {"ev_prec": p, "ev_f05": f, "tau": t, "c": c, "cont_prec_same": same.prec, "cont_fa_same": same.fa,
            "cont_prec_B2": pb2, "infl_same": p / same.prec if same.prec > 0 else np.inf,
            "infl_B2": p / pb2 if pb2 and pb2 > 0 else np.inf}


rows = []
for meth in METHODS:
    ev, cont = tables(meth); subs = sorted(cont["sub"].unique())
    st = stats(ev, cont); bs = []
    evg = {s: d for s, d in ev.groupby("sub")}; cog = {s: d for s, d in cont.groupby("sub")}
    for _ in range(NBOOT):
        smp = rng.choice(subs, size=len(subs), replace=True)
        evb = pd.concat([evg[s] for s in smp if s in evg]); cob = pd.concat([cog[s] for s in smp])
        if evb.y.sum() == 0 or (evb.y == 0).sum() == 0:
            continue
        bs.append(stats(evb, cob))
    B = pd.DataFrame(bs)
    row = {"method": meth, **st, "n_boot": len(B)}
    for k in ("infl_same", "infl_B2", "cont_fa_same"):
        v = B[k].replace(np.inf, np.nan).dropna()
        row[f"{k}_lo"], row[f"{k}_hi"] = np.percentile(v, [2.5, 97.5]) if len(v) else (np.nan, np.nan)
        row[f"{k}_p_le5" if k != "cont_fa_same" else "cont_fa_p_le4"] = float((B[k] <= (5 if k != "cont_fa_same" else 4)).mean())
    rows.append(row); print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/m{M}_ci.csv", index=False)
