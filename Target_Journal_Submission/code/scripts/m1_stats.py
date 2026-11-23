"""M1 development statistics at B = 2 (primary budget): candidate C2 (rule OR AE), C1 (rule) vs baselines.
Operating points = M1-optimal at B (from results/m1_table.csv and results/round4/orfusion_best_*.csv)."""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O
from src.statistics.paired import per_sub_table, detected_vector, cluster_bootstrap, mcnemar_exact, holm

M, B = 1, int(sys.argv[1]) if len(sys.argv) > 1 else 2
subs = P.substations(M)
T = pd.read_csv("results/m1_table.csv")
F = pd.read_csv("results/round4/orfusion_best_ae_underdel_qnbm.csv")


def alarm(method, tau, c, s):
    sc = R.load_scores(method, M, s)
    return pd.Series(O.criticality_counter(sc, tau) >= c, index=sc.index)


def run(spec):
    res = []
    for s in subs:
        if spec[0] == "or":
            _, m1, t1, c1, m2, t2, c2 = spec
            a = alarm(m1, t1, c1, s); b = alarm(m2, t2, c2, s).reindex(a.index, fill_value=False)
            al = a | b
        else:
            al = alarm(*spec, s)
        res.append(C.evaluate_substation(al, C.substation_labels(M, s, al.index)))
    return res


specs = {}
for m in ["rule", "ae", "ae_cond", "sigma3", "loop3s", "iforest", "qnbm", "srcr_comp__v_gate_1s_local"]:
    r = T[(T.method == m) & (T.budget == B)].iloc[0]
    specs[m] = (m, float(r.tau), int(r.c_thr))
f = F[(F.partner == "ae") & (F.budget == B)].iloc[0]
specs["C2_rule_or_ae"] = ("or", "rule", float(f.rule_tau), int(f.rule_c), "ae", float(f.p_tau), int(f.p_c))
out = {k: run(v) for k, v in specs.items()}
tabs = {k: per_sub_table(v, subs) for k, v in out.items()}
dets = {k: detected_vector(v) for k, v in out.items()}
summ = {k: C.summarise(v) for k, v in out.items()}
rows = []
for cand in ["C2_rule_or_ae", "rule"]:
    pv = {}
    for base in [k for k in specs if k != cand and not (cand == "rule" and k == "C2_rule_or_ae")]:
        bs = cluster_bootstrap(tabs[cand], tabs[base])
        mc = mcnemar_exact(dets[cand], dets[base])
        pv[base] = mc["p"]
        rows.append({"candidate": cand, "baseline": base, "recall_cand": summ[cand]["recall"], "recall_base": summ[base]["recall"],
                     "fa_cand": summ[cand]["fa_per_sub_year"], "fa_base": summ[base]["fa_per_sub_year"],
                     "d_recall": bs["d_recall"], "d_recall_lo": bs["d_recall_ci"][0], "d_recall_hi": bs["d_recall_ci"][1],
                     "d_fa": bs["d_fa"], "d_fa_lo": bs["d_fa_ci"][0], "d_fa_hi": bs["d_fa_ci"][1],
                     "cand_only": mc["a_only"], "base_only": mc["b_only"], "mcnemar_p": mc["p"]})
    for b, p in holm(pv).items():
        for r in rows:
            if r["candidate"] == cand and r["baseline"] == b:
                r["mcnemar_p_holm"] = p
df = pd.DataFrame(rows)
os.makedirs("results/stats", exist_ok=True)
df.to_csv(f"results/stats/m1_paired_B{B}.csv", index=False)
json.dump({k: [str(x) for x in v] for k, v in specs.items()}, open(f"results/stats/m1_specs_B{B}.json", "w"), indent=1)
print(df.round(3).to_string(index=False))
