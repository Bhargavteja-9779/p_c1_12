"""plan_v2 analysis (experiments/plan_v2.md): 2x2 protocol factorial + panel selection test.
Usage: plan_v2_analysis.py {predist1|care} SEED      -> results/plan_v2/<ds>/seed<SEED>/
Committed before any panel score existed. Uses only score files; no model fitting."""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau
from src.models import online as O
from src.models.panel import GENERIC
from src.evaluation import continuous as C
from src.evaluation.runner import TAU_GRID

DS, SEED = sys.argv[1], int(sys.argv[2])
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
B, NBOOT, NWIN = 2.0, int(os.environ.get("PLANV2_NBOOT", 2000)), 2000
ROOT = os.environ.get("PLANV2_ROOT", "results")  # dry runs only: point to scratch
OUT = f"{ROOT}/plan_v2/{DS}/seed{SEED}"; os.makedirs(OUT, exist_ok=True)
CACHE = f"{ROOT}/plan_v2/{DS}/cache"; os.makedirs(CACHE, exist_ok=True)
T, CN = len(TAU_GRID), len(C_GRID)

if DS == "care":
    from src.data import care
    from src.evaluation import care_eval as CE
    ASSETS = [(f, a) for f in care.FARMS for a in care.assets(f)]
    aname = lambda k: f"{k[0]}_{k[1]}"
    FOLD = np.array([care.FARMS.index(f) for f, _ in ASSETS]); NF = 3
    EXTRA = ["temp3s", "ae", "ae_cond"]
    def load(det, k):
        if det in GENERIC:
            return pd.read_parquet(f"{ROOT}/scores_panel/care/seed{SEED}/{det}/{aname(k)}.parquet")["score"]
        return CE.load_scores(det, *k)
    def labels(k, idx): return CE.labels(k[0], k[1], idx)
    def events(k):
        E = care.events(k[0]); E = E[E.asset == k[1]]
        return [(r.event_start, r.event_end, int(r.event_label == "anomaly")) for r in E.itertuples()]
    NORMAL_LENS = [(e - s).total_seconds() / 86400 for k in ASSETS for s, e, y in events(k) if y == 0]
else:
    from src.data import predist as P
    from src.evaluation import runner as R
    M = int(DS[-1]); SUBS = P.substations(M); ASSETS = SUBS
    aname = lambda s: f"s{s}"
    perm = np.random.default_rng(0).permutation(len(SUBS)); FOLD = np.empty(len(SUBS), int); FOLD[perm] = np.arange(len(SUBS)) % 5; NF = 5
    EXTRA = ["rule", "loop3s", "qnbm", "ae", "ae_cond"]
    def load(det, s):
        if det in GENERIC:
            return pd.read_parquet(f"{ROOT}/scores_panel/{DS}/seed{SEED}/{det}/s{s}.parquet")["score"]
        return R.load_scores(det, M, s)
    def labels(s, idx): return C.substation_labels(M, s, idx)
    W7 = pd.Timedelta(days=7); FA, NE = P.faults(M), P.normal_events(M)
    def events(s):
        F = FA[(FA["sub"] == s) & (FA.efd_possible == True)]; N = NE[NE["sub"] == s]
        return [(r - W7, r, 1) for r in F["Report date"]] + [(a, b, 0) for a, b in zip(N["Event start"], N["Event end"])]
    NORMAL_LENS = [7.0]
DETS = GENERIC + EXTRA
A = len(ASSETS)

# ---- fixed event set and random windows (defined from z_max coverage of this seed's panel)
rng = np.random.default_rng(0)
EV, RW, LABS = [], [], {}
for i, k in enumerate(ASSETS):
    sc = load("z_max", k); lab = labels(k, sc.index); LABS[i] = (sc.index, lab)
    for s_, e_, y in events(k):
        w = (sc.index >= s_) & (sc.index < e_)
        if w.any() and sc[w].notna().any():
            EV.append((i, s_, e_, y))
tries = 0
while len(RW) < NWIN and tries < 200000:
    tries += 1; i = int(rng.integers(A)); idx, lab = LABS[i]
    L = pd.Timedelta(days=float(rng.choice(NORMAL_LENS)))
    lo, hi = lab.start, lab.end - L
    if hi <= lo: continue
    s_ = (lo + (hi - lo) * rng.random()).floor("h")
    blocked = list(zip(lab.targets.win_start, lab.targets.report)) + lab.exclusions
    if any(a < s_ + L and s_ < b for a, b in blocked): continue
    sc = load("z_max", ASSETS[i]); w = (sc.index >= s_) & (sc.index < s_ + L)
    if w.any() and sc[w].notna().mean() >= 0.5: RW.append((i, s_, s_ + L))
ev_a = np.array([e[0] for e in EV]); ev_y = np.array([e[3] for e in EV]); rw_a = np.array([r[0] for r in RW])
nrm = ev_y == 0


def tables(det):
    """cont (A,T,CN,4) n_tgt n_det n_fa expo; ev_mx (nev,T); rw_mx (nrw,T)."""
    cp = f"{CACHE}/{det}_seed{SEED if det in GENERIC else 'x'}.npz"
    if os.path.exists(cp):
        z = np.load(cp); return z["cont"], z["ev"], z["rw"]
    cont = np.zeros((A, T, CN, 4)); evm = np.zeros((len(EV), T)); rwm = np.zeros((len(RW), T))
    for i, k in enumerate(ASSETS):
        try:
            sc = load(det, k)
        except FileNotFoundError:
            continue
        lab = labels(k, sc.index)
        for ti, tau in enumerate(TAU_GRID):
            cnt = O.criticality_counter(sc, tau); ci = pd.Series(cnt, index=sc.index)
            for ci_, c in enumerate(C_GRID):
                r = C.evaluate_substation(ci >= c, lab)
                cont[i, ti, ci_] = (len(r["detections"]), sum(d["detected"] for d in r["detections"]), len(r["false_alarms"]), r["exposure_days"])
            for j in np.where(ev_a == i)[0]:
                w = (sc.index >= EV[j][1]) & (sc.index < EV[j][2]); evm[j, ti] = cnt[w].max() if w.any() else 0
            for j in np.where(rw_a == i)[0]:
                w = (sc.index >= RW[j][1]) & (sc.index < RW[j][2]); rwm[j, ti] = cnt[w].max() if w.any() else 0
    np.savez(cp, cont=cont, ev=evm, rw=rwm); return cont, evm, rwm


def pooled(cont, w):
    g = np.tensordot(w, cont, axes=(0, 0))  # (T,CN,4)
    rec = g[..., 1] / np.maximum(g[..., 0], 1e-9); fa = g[..., 2] / np.maximum(g[..., 3] / 365.25, 1e-9)
    return rec, fa


def best_point(cont, w):
    rec, fa = pooled(cont, w); ok = fa <= B
    if not ok.any(): return (T - 1, CN - 1)
    sc = np.where(ok, rec * 1e6 - fa, -np.inf); return np.unravel_index(np.argmax(sc), sc.shape)


def heldout_points(cont, w):
    pts = {}
    for f in range(NF):
        wf = w * (FOLD != f); pts[f] = best_point(cont, wf)
    return pts


def f05(evm, w_ev, ti, c):
    pred = evm[:, ti] >= c; tp = (w_ev * (pred & (ev_y == 1))).sum(); fp = (w_ev * (pred & (ev_y == 0))).sum()
    fn = (w_ev * (~pred & (ev_y == 1))).sum(); p = tp / (tp + fp) if tp + fp else 0.0; r = tp / (tp + fn) if tp + fn else 0.0
    return 1.25 * p * r / (0.25 * p + r) if p + r else 0.0


def cells(cont, evm, w, pts_fixed=None):
    w_ev = w[ev_a]
    et = max(f05(evm, w_ev, ti, c) for ti in range(T) for c in C_GRID)
    pts = pts_fixed if pts_fixed is not None else heldout_points(cont, np.ones(A))
    # EH: per-event point of its asset's fold
    pred = np.array([evm[j, pts[FOLD[ev_a[j]]][0]] >= C_GRID[pts[FOLD[ev_a[j]]][1]] for j in range(len(EV))])
    tp = (w_ev * (pred & (ev_y == 1))).sum(); fp = (w_ev * (pred & (ev_y == 0))).sum(); fn = (w_ev * (~pred & (ev_y == 1))).sum()
    p = tp / (tp + fp) if tp + fp else 0.0; r = tp / (tp + fn) if tp + fn else 0.0
    eh = 1.25 * p * r / (0.25 * p + r) if p + r else 0.0
    ti, ci = best_point(cont, w); rec, _ = pooled(cont, w); ct = rec[ti, ci]
    g = sum(np.tensordot(w * (FOLD == f), cont[:, pts[f][0], pts[f][1]], axes=(0, 0)) for f in range(NF))
    ch = g[1] / max(g[0], 1e-9)
    return et, eh, ct, ch, pts


tab = {d: tables(d) for d in DETS}
ones = np.ones(A)
point = {}
rows = []
for d in DETS:
    et, eh, ct, ch, pts = cells(tab[d][0], tab[d][1], ones); point[d] = pts
    rows.append({"detector": d, "ET": et, "EH": eh, "CT": ct, "CH": ch})
Rt = pd.DataFrame(rows); Rt.to_csv(f"{OUT}/cells.csv", index=False)
kt = lambda x: kendalltau(Rt[x], Rt.CH).statistic
obs = {"tau_ET": kt("ET"), "tau_EH": kt("EH"), "tau_CT": kt("CT")}

# selection effect at held-out points (hits precomputed once: held-out points are fixed)
HITS = {}
for d in DETS:
    _, evm, rwm = tab[d]; pts = point[d]
    HITS[d] = (np.array([evm[j, pts[FOLD[ev_a[j]]][0]] >= C_GRID[pts[FOLD[ev_a[j]]][1]] for j in np.where(nrm)[0]], float),
               np.array([rwm[j, pts[FOLD[rw_a[j]]][0]] >= C_GRID[pts[FOLD[rw_a[j]]][1]] for j in range(len(RW))], float))
def sel(w):
    we, wr = w[ev_a[nrm]], w[rw_a]
    hn = sum((we * HITS[d][0]).sum() for d in DETS); hr = sum((wr * HITS[d][1]).sum() for d in DETS)
    nn, nr = we.sum() * len(DETS), wr.sum() * len(DETS)
    return (hn / nn) / (hr / nr) if hr > 0 and nn > 0 else np.nan

per_det_sel = []
for d in DETS:
    _, evm, rwm = tab[d]; pts = point[d]
    he = np.mean([evm[j, pts[FOLD[ev_a[j]]][0]] >= C_GRID[pts[FOLD[ev_a[j]]][1]] for j in np.where(nrm)[0]])
    hw = np.mean([rwm[j, pts[FOLD[rw_a[j]]][0]] >= C_GRID[pts[FOLD[rw_a[j]]][1]] for j in range(len(RW))])
    per_det_sel.append({"detector": d, "normal_event_hit": he, "random_window_hit": hw, "ratio": he / hw if hw > 0 else np.nan})
pd.DataFrame(per_det_sel).to_csv(f"{OUT}/selection_per_detector.csv", index=False)
obs["sel_ratio"] = sel(ones)

brng = np.random.default_rng(0); bs = []
for b in range(NBOOT):
    w = np.bincount(brng.integers(A, size=A), minlength=A).astype(float)
    if (w[ev_a] * (ev_y == 1)).sum() == 0 or (w[ev_a] * (ev_y == 0)).sum() == 0: continue
    rr = [cells(tab[d][0], tab[d][1], w, point[d]) for d in DETS]
    X = pd.DataFrame([r[:4] for r in rr], columns=["ET", "EH", "CT", "CH"])
    k_ = lambda x: kendalltau(X[x], X.CH).statistic
    bs.append({"tau_ET": k_("ET"), "tau_EH": k_("EH"), "tau_CT": k_("CT"), "sel_ratio": sel(w)})
Bt = pd.DataFrame(bs); Bt["dA"] = Bt.tau_EH - Bt.tau_ET; Bt["dB"] = Bt.tau_CT - Bt.tau_ET
Bt.to_csv(f"{OUT}/bootstrap.csv", index=False)
ci = lambda s: [float(np.nanpercentile(s, 2.5)), float(np.nanpercentile(s, 97.5))]
summ = {"dataset": DS, "seed": SEED, "n_detectors": len(DETS), "n_assets": A, "n_events": len(EV),
        "n_fault_events": int(ev_y.sum()), "n_random_windows": len(RW), "n_boot": len(Bt), **obs,
        "H7a_diff": obs["tau_EH"] - obs["tau_ET"], "H7a_ci": ci(Bt.dA), "H7a_p": float((Bt.dA <= 0).mean()),
        "H7b_diff": obs["tau_CT"] - obs["tau_ET"], "H7b_ci": ci(Bt.dB), "H7b_p": float((Bt.dB <= 0).mean()),
        "H7c_share_threshold": (obs["tau_EH"] - obs["tau_ET"]) / (1 - obs["tau_ET"]) if obs["tau_ET"] < 1 else np.nan,
        "H7c_share_window": (obs["tau_CT"] - obs["tau_ET"]) / (1 - obs["tau_ET"]) if obs["tau_ET"] < 1 else np.nan,
        "H7d_ci": ci(Bt.sel_ratio), "H7d_share_detectors_ratio_lt1": float(np.mean([r["ratio"] < 1 for r in per_det_sel if r["ratio"] == r["ratio"]]))}
summ["H7d_supported"] = bool(obs["sel_ratio"] < 1 and summ["H7d_ci"][1] < 1)
json.dump(summ, open(f"{OUT}/summary.json", "w"), indent=1, default=float)
print(Rt.round(3).to_string(index=False)); print(json.dumps(summ, indent=1, default=float))
