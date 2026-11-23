"""D6 round 3 (M1 only): daily decision unit, fleet / adaptive conformal alarm budgets, under-delivery fusion.
Usage: round3_daily.py METHOD[+CHANNEL] [...]   e.g. srcr_comp__v_gate_1s_local ae srcr_comp__v_gate_1s_local+underdel"""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, daily as DL
from src.evaluation.runner import load_scores
from src.models.fusion import m1_folds, level

m = 1; subs = P.substations(m); folds = m1_folds(seed=0)
BUDGETS = (1, 2, 4)
SWEEP_K = (0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12)


def load(method):
    out = {}
    for s in subs:
        sc = load_scores(method, m, s)
        lab = C.substation_labels(m, s, sc.index)
        D = DL.daily(sc)
        out[s] = dict(idx=sc.index, lab=lab, D=D, N=DL.normal_days(D, lab))
    return out


def fused(parts):
    """parts: list of per-channel dicts. Per fold: map each channel's D to a level vs training-fold normal D."""
    out = {}
    for test in folds:
        train = [s for s in subs if s not in test]
        cal = [np.sort(np.concatenate([p[s]["N"].to_numpy() for s in train])) for p in parts]
        for s in subs:   # levels for every substation with THIS fold's calibration; keep test subs only
            lv = None
            for p, c in zip(parts, cal):
                L = pd.Series(level(p[s]["D"].to_numpy(float), c), index=p[s]["D"].index)
                lv = L if lv is None else pd.concat([lv, L], axis=1).max(axis=1)
            if s in test:
                out[s] = dict(idx=parts[0][s]["idx"], lab=parts[0][s]["lab"], D=lv, N=DL.normal_days(lv, parts[0][s]["lab"]))
            out.setdefault("_train_" + str(folds.index(test)), {})[s] = lv
    return out


def evaluate(data, thr_of):
    res, per = [], {}
    for s in subs:
        d = data[s]
        r = C.evaluate_substation(DL.alarm_from_daily(d["D"], thr_of(s), d["idx"]), d["lab"])
        res.append(r); per[s] = len(r["false_alarms"])
    out = C.summarise(res)
    fa = np.sort(np.array(list(per.values())))[::-1]
    out["top5_share"] = fa[:5].sum() / max(1, fa.sum())
    out["subs_with_fa"] = int((fa > 0).sum())
    out["detected"] = sorted(int(x["event_id"]) for r in res for x in r["detections"] if x["detected"])
    return out


rows = []
for spec in sys.argv[1:]:
    parts = [load(x) for x in spec.split("+")]
    data = parts[0] if len(parts) == 1 else fused(parts)
    fold_of = {s: k for k, f in enumerate(folds) for s in f}

    def train_normals(k):
        if len(parts) == 1:
            return np.concatenate([data[s]["N"].to_numpy() for s in subs if fold_of[s] != k])
        tr = data["_train_" + str(k)]
        return np.concatenate([DL.normal_days(tr[s], parts[0][s]["lab"]).to_numpy() for s in subs if fold_of[s] != k])

    pooled = np.concatenate([data[s]["N"].to_numpy() for s in subs])
    for k_ in SWEEP_K:   # H3a: in-sample threshold sweep (same protocol as the 10-min counter sweep)
        thr = DL.conformal_threshold(pooled, k_ / 365.25)
        r = evaluate(data, lambda s: thr); r.update(method=spec, mode="sweep", budget=k_, thr=thr); rows.append(r)
    for B in BUDGETS:    # H3b fleet conformal (cross-fitted) and H3c adaptive
        a = B / 365.25
        thr_k = {k: DL.conformal_threshold(train_normals(k), a) for k in range(len(folds))}
        r = evaluate(data, lambda s: thr_k[fold_of[s]]); r.update(method=spec, mode="conformal", budget=B); rows.append(r)
        ad = {s: DL.adaptive_threshold(data[s]["D"], thr_k[fold_of[s]], a) for s in subs}
        r = evaluate(data, lambda s: ad[s]); r.update(method=spec, mode="adaptive", budget=B); rows.append(r)
    for r in rows:
        if r["method"] == spec:
            print(spec, r["mode"], r["budget"], f"rec={r['recall']:.3f} fa={r['fa_per_sub_year']:.2f} nfa={r['n_false_alarms']} top5={r['top5_share']:.2f}", flush=True)
os.makedirs("results", exist_ok=True)
tag = "_".join(a.replace("+", "-") for a in sys.argv[1:])[:120]
pd.DataFrame(rows).to_csv(f"results/round3_{tag}.csv", index=False)
