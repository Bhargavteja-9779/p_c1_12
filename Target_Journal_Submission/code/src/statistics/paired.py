"""Paired inference for detectors evaluated on the same faults and substations (protocol v1):
cluster bootstrap over substations (recall difference, FA-rate difference) and exact McNemar on faults."""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import binomtest


def per_sub_table(results: list[dict], subs: list) -> pd.DataFrame:
    """results: evaluate_substation outputs in the order of subs -> per-substation detections/FA/exposure."""
    rows = []
    for s, r in zip(subs, results):
        det = r["detections"]
        rows.append({"sub": s, "n_faults": len(det), "n_det": sum(d["detected"] for d in det),
                     "n_fa": len(r["false_alarms"]), "expo_days": r["exposure_days"]})
    return pd.DataFrame(rows).set_index("sub")


def detected_vector(results: list[dict]) -> pd.Series:
    return pd.Series({d["event_id"]: bool(d["detected"]) for r in results for d in r["detections"]})


def cluster_bootstrap(a: pd.DataFrame, b: pd.DataFrame, n_boot=10000, seed=0) -> dict:
    """a, b: per_sub_table of method A and B on the same substations. Returns point estimates and 95% CIs of
    recall_A - recall_B and FA/sub-yr_A - FA/sub-yr_B (substation = resampling unit)."""
    rng = np.random.default_rng(seed)
    subs = a.index.to_numpy()
    A, Bt = a.loc[subs], b.loc[subs]
    nf, da, db = A.n_faults.to_numpy(), A.n_det.to_numpy(), Bt.n_det.to_numpy()
    ex, fa, fb = A.expo_days.to_numpy() / 365.25, A.n_fa.to_numpy(), Bt.n_fa.to_numpy()

    def stat(ix):
        f = nf[ix].sum()
        e = ex[ix].sum()
        return ((da[ix].sum() - db[ix].sum()) / f if f else np.nan, (fa[ix].sum() - fb[ix].sum()) / e)

    pt = stat(np.arange(len(subs)))
    bs = np.array([stat(rng.integers(0, len(subs), len(subs))) for _ in range(n_boot)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
    return {"d_recall": pt[0], "d_recall_ci": (lo[0], hi[0]), "d_fa": pt[1], "d_fa_ci": (lo[1], hi[1])}


def mcnemar_exact(da: pd.Series, db: pd.Series) -> dict:
    """Exact (binomial) McNemar on paired fault detections."""
    j = pd.concat([da, db], axis=1, keys=["a", "b"]).dropna()
    n10 = int((j.a & ~j.b).sum()); n01 = int((~j.a & j.b).sum())
    p = binomtest(n10, n10 + n01, 0.5).pvalue if n10 + n01 else 1.0
    return {"a_only": n10, "b_only": n01, "p": p}


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, out, run = len(items), {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out
