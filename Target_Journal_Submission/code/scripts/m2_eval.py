"""Locked M2 evaluation (protocol Amendment A1). Run ONCE after all M2 scores exist.
1) Every frozen method at its M1-chosen operating point per budget, applied unchanged to M2.
2) C2 / AE per seed 0-9 -> mean +- SD.
3) Pooled M1+M2 paired inference at B = 2 (seed 0): cluster bootstrap, exact McNemar, Holm.
4) Curve endpoint: separate script (m2_curves.py), descriptive."""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O
from src.statistics.paired import per_sub_table, detected_vector, cluster_bootstrap, mcnemar_exact, holm

BUDGETS = (1, 2, 4)
BASE = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "srcr_comp__v_gate_1s_local"]
T = pd.concat([pd.read_csv("results/m1_table.csv"), pd.read_csv("results/m1_table_aeseeds.csv")])
F = pd.concat([pd.read_csv("results/round4/orfusion_best_ae_underdel_qnbm.csv"),
               pd.read_csv("results/round4/orfusion_best_" + "_".join(f"ae_seed{k}" for k in range(1, 10)) + ".csv")])
F = F[F.partner.str.startswith("ae")]
OUT = "results/m2"; os.makedirs(OUT, exist_ok=True)
_cache = {}


def scores(method, m, s):
    k = (method, m, s)
    if k not in _cache:
        _cache[k] = R.load_scores(method, m, s)
    return _cache[k]


def alarm(method, m, s, tau, c):
    sc = scores(method, m, s)
    return pd.Series(O.criticality_counter(sc, tau) >= c, index=sc.index)


def evaluate(spec, m):
    res = []
    for s in P.substations(m):
        if spec[0] == "or":
            _, m1, t1, c1, m2_, t2, c2 = spec
            a = alarm(m1, m, s, t1, c1); al = a | alarm(m2_, m, s, t2, c2).reindex(a.index, fill_value=False)
        else:
            al = alarm(spec[0], m, s, spec[1], spec[2])
        res.append(C.evaluate_substation(al, C.substation_labels(m, s, al.index)))
    return res


def spec_of(name, B):
    if name.startswith("C2"):
        partner = "ae" if name == "C2" else name.split(":")[1]
        f = F[(F.partner == partner) & (F.budget == B)].iloc[0]
        return ("or", "rule", float(f.rule_tau), int(f.rule_c), partner, float(f.p_tau), int(f.p_c))
    r = T[(T.method == name) & (T.budget == B)].iloc[0]
    return (name, float(r.tau), int(r.c_thr))


if __name__ == "__main__":
    rows, results = [], {}
    names = BASE + ["C2"] + [f"ae_seed{k}" for k in range(1, 10)] + [f"C2:ae_seed{k}" for k in range(1, 10)]
    for B in BUDGETS:
        for n in names:
            sp = spec_of(n, B)
            for m in (1, 2):
                res = evaluate(sp, m)
                results[(n, B, m)] = res
                r = C.summarise(res); r.update(method=n, budget=B, m=m, spec=str(sp)); rows.append(r)
            print(B, n, round(rows[-2]["recall"], 3), round(rows[-1]["recall"], 3), round(rows[-1]["fa_per_sub_year"], 2), flush=True)
    tab = pd.DataFrame(rows); tab.to_csv(f"{OUT}/m2_locked_table.csv", index=False)
    # seeds summary
    seeds = []
    for B in BUDGETS:
        for fam, pat in (("AE", ["ae"] + [f"ae_seed{k}" for k in range(1, 10)]), ("C2", ["C2"] + [f"C2:ae_seed{k}" for k in range(1, 10)])):
            for m in (1, 2):
                g = tab[(tab.budget == B) & (tab.m == m) & tab.method.isin(pat)]
                seeds.append({"family": fam, "budget": B, "m": m, "recall_mean": g.recall.mean(), "recall_sd": g.recall.std(),
                              "fa_mean": g.fa_per_sub_year.mean(), "fa_sd": g.fa_per_sub_year.std()})
    pd.DataFrame(seeds).to_csv(f"{OUT}/m2_seed_summary.csv", index=False)
    print(pd.DataFrame(seeds).round(3).to_string(index=False))
    # pooled paired inference at B = 2 (seed 0)
    B = 2
    pooled = {}
    for n in BASE + ["C2"]:
        res = results[(n, B, 1)] + results[(n, B, 2)]
        subs = [f"1_{s}" for s in P.substations(1)] + [f"2_{s}" for s in P.substations(2)]
        pooled[n] = (per_sub_table(res, subs), pd.concat([detected_vector(results[(n, B, 1)]).rename(lambda e: f"1_{e}"),
                     detected_vector(results[(n, B, 2)]).rename(lambda e: f"2_{e}")]), C.summarise(res))
    prow = []
    for cand, bases in (("C2", [b for b in BASE]), ("rule", ["ae"])):
        pv = {}
        for b in bases:
            if b == cand:
                continue
            bs = cluster_bootstrap(pooled[cand][0], pooled[b][0]); mc = mcnemar_exact(pooled[cand][1], pooled[b][1])
            pv[b] = mc["p"]
            prow.append({"candidate": cand, "baseline": b, "recall_cand": pooled[cand][2]["recall"], "recall_base": pooled[b][2]["recall"],
                         "fa_cand": pooled[cand][2]["fa_per_sub_year"], "fa_base": pooled[b][2]["fa_per_sub_year"],
                         "d_recall": bs["d_recall"], "d_recall_lo": bs["d_recall_ci"][0], "d_recall_hi": bs["d_recall_ci"][1],
                         "d_fa": bs["d_fa"], "d_fa_lo": bs["d_fa_ci"][0], "d_fa_hi": bs["d_fa_ci"][1],
                         "cand_only": mc["a_only"], "base_only": mc["b_only"], "mcnemar_p": mc["p"]})
        for b, p in holm(pv).items():
            for r in prow:
                if r["candidate"] == cand and r["baseline"] == b:
                    r["p_holm"] = p
    P_ = pd.DataFrame(prow); P_.to_csv(f"{OUT}/pooled_paired_B2.csv", index=False)
    print(P_.round(3).to_string(index=False))
    # detection lists for error analysis
    det = pd.DataFrame({n: pooled[n][1] for n in BASE + ["C2"]})
    det.to_csv(f"{OUT}/pooled_detections_B2.csv")
