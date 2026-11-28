"""plan_v2 Amendment A3 (experiments/plan_v2_amendment_A3.md). Usage: plan_v2_amendment_A3.py {predist1|care} SEED
Env A3_VERSION (label), A3_OUT (absolute output dir), PLANV2_ROOT as for plan_v2. Reuses the plan_v2 setup code
verbatim (events, random windows, folds, cached tables); no new scores."""
import os, sys, json
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan_v2_analysis.py")
code = open(SRC).read(); head = code[:code.index("tab = {d: tables(d) for d in DETS}")]
os.environ.setdefault("PLANV2_NBOOT", "0"); sys.argv = [SRC] + sys.argv[1:3]
g = {"__file__": SRC, "__name__": "planv2_head"}; exec(compile(head, SRC, "exec"), g)
np, pd = g["np"], g["pd"]
DETS, A, FOLD, T, CN, DS, SEED, C_GRID = (g[k] for k in ["DETS", "A", "FOLD", "T", "CN", "DS", "SEED", "C_GRID"])
EV, RW, LABS, ev_a, ev_y, rw_a, nrm = (g[k] for k in ["EV", "RW", "LABS", "ev_a", "ev_y", "rw_a", "nrm"])
f05, heldout_points = g["f05"], g["heldout_points"]
VER = os.environ.get("A3_VERSION", "main"); OUTD = os.environ.get("A3_OUT", "results/plan_v2/amendment_A3"); os.makedirs(OUTD, exist_ok=True)
ones = np.ones(A); w_ev = ones[ev_a]; res = {"dataset": DS, "seed": SEED, "version": VER}

# A3.1 full-panel burden at the benchmark-optimal point
rows, HITS = [], {}
for d in DETS:
    cont, evm, rwm = g["tables"](d)
    best, bp = -1, None
    for ti in range(T):
        for ci, c in enumerate(C_GRID):
            v = f05(evm, w_ev, ti, c)
            if v > best: best, bp = v, (ti, ci)
    ti, ci = bp; pred = evm[:, ti] >= C_GRID[ci]
    tp, fp = int((pred & (ev_y == 1)).sum()), int((pred & (ev_y == 0)).sum())
    n_tgt, n_det, n_fa, expo = cont[:, ti, ci].sum(axis=0)
    fa_yr = n_fa / (expo / 365.25); dprec = n_det / (n_det + n_fa) if n_det + n_fa > 0 else float("nan")
    eprec = tp / (tp + fp) if tp + fp else float("nan")
    rows.append({"detector": d, "ET": best, "event_precision": eprec, "cont_FA_per_asset_yr": fa_yr, "cont_recall": n_det / max(n_tgt, 1e-9),
                 "deployed_alarm_precision": dprec, "inflation": eprec / dprec if dprec and dprec == dprec and dprec > 0 else float("nan")})
    pts = heldout_points(cont, ones)
    HITS[d] = (np.array([evm[j, pts[FOLD[ev_a[j]]][0]] >= C_GRID[pts[FOLD[ev_a[j]]][1]] for j in np.where(nrm)[0]], float),
               np.array([rwm[j, pts[FOLD[rw_a[j]]][0]] >= C_GRID[pts[FOLD[rw_a[j]]][1]] for j in range(len(RW))], float))
X = pd.DataFrame(rows); X.to_csv(f"{OUTD}/{DS}_{VER}_seed{SEED}_burden.csv", index=False)
fin = X.inflation[np.isfinite(X.inflation)]
res["A3_1"] = {"FA_range": [float(X.cont_FA_per_asset_yr.min()), float(X.cont_FA_per_asset_yr.max())],
               "FA_median": float(X.cont_FA_per_asset_yr.median()), "n_FA_gt_4": int((X.cont_FA_per_asset_yr > 4).sum()),
               "inflation_range": [float(fin.min()), float(fin.max())] if len(fin) else None, "inflation_median": float(fin.median()) if len(fin) else None,
               "n_inflation_undefined": int((~np.isfinite(X.inflation)).sum()), "n_detectors": len(X)}

# A3.2 chance baselines
nf, ne = int(ev_y.sum()), len(ev_y); p0 = nf / ne
res["A3_2"] = {"always_alarm_event_F05": 1.25 * p0 / (0.25 * p0 + 1), "n_fault_events": nf, "n_events": ne}
L = np.array([(e[2] - e[1]).total_seconds() / 86400 for e in EV if e[3] == 1])
rand = {b: float(np.mean(1 - np.exp(-b * L / 365.25))) for b in [0.5, 1, 2, 4, 8]}
res["A3_2"]["random_alarm_recall"] = rand
a2 = f"{os.path.dirname(OUTD)}/amendment_A2/{DS}_{VER}_seed{SEED}_cells.csv"
if os.path.exists(a2):
    C2 = pd.read_csv(a2)
    res["A3_2"]["n_detectors_above_random"] = {b: int((C2[f"CH_{b}"] > rand[b]).sum()) for b in rand}
    res["A3_2"]["n_detectors"] = len(C2)

# A3.3 selection-effect confound checks
ev_norm = np.where(nrm)[0]
m_ev = np.array([EV[j][1].month for j in ev_norm]); m_rw = np.array([RW[j][1].month for j in range(len(RW))])
sh_ev = pd.Series(m_ev).value_counts(normalize=True); sh_rw = pd.Series(m_rw).value_counts(normalize=True)
w_season = np.array([sh_ev.get(m, 0.0) / sh_rw[m] for m in m_rw])
far = np.ones(len(RW), bool); D30 = pd.Timedelta(days=30)
for j, (i, s_, e_) in enumerate(RW):
    lab = LABS[i][1]
    marks = [(t - D30, t + D30) for t in lab.targets.report] + [(a - D30, b + D30) for a, b in lab.exclusions]
    far[j] = not any(a < e_ and s_ < b for a, b in marks)
HN = np.stack([HITS[d][0] for d in DETS]); HR = np.stack([HITS[d][1] for d in DETS])


def ratio(wa, wr):
    we = wa[ev_a[ev_norm]]; wrr = wa[rw_a] * wr
    num = (HN * we).sum() / (we.sum() * len(DETS)); den = (HR * wrr).sum() / (wrr.sum() * len(DETS))
    return num / den if den > 0 else float("nan")


out = {}
for name, wr in [("all_random", np.ones(len(RW))), ("season_matched", w_season), ("far_from_records", far.astype(float))]:
    est = ratio(ones, wr); rng = np.random.default_rng(0); bs = []
    for _ in range(2000):
        wa = np.bincount(rng.integers(A, size=A), minlength=A).astype(float)
        if wa[ev_a[ev_norm]].sum() == 0 or (wa[rw_a] * wr).sum() == 0: continue
        bs.append(ratio(wa, wr))
    ci = [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))]
    out[name] = {"ratio": float(est), "ci": ci, "n_random_windows_used": int((wr > 0).sum())}
res["A3_3"] = out
res["A3_3"]["robust_to_confound"] = bool(all(out[k]["ratio"] < 1 and out[k]["ci"][1] < 1 for k in ["season_matched", "far_from_records"]))
json.dump(res, open(f"{OUTD}/{DS}_{VER}_seed{SEED}.json", "w"), indent=1, default=float)
print(X.round(3).to_string(index=False)); print(json.dumps(res, indent=1, default=float))
