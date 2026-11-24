"""Round 5 (pre-registered): peer-relative daily channels. Usage: round5_peer.py M
Writes score files peer_phys, peer_comfort, peer_all, own_change, fuse_peer_srcr for manufacturer M and,
for M = 1, evaluates them at budgets 1/2/4 and threshold-free (development)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import runner as R
from src.models import peer as PR

M = int(sys.argv[1])
subs = P.substations(M)
X = {s: P.load_substation(M, s) for s in subs}
daily = {s: PR.daily_features(X[s]) for s in subs}
zp, zc, zo = PR.peer_z(daily, PR.PHYS), PR.peer_z(daily, PR.COMFORT), PR.own_z(daily, PR.OWN)
srcr_name = "srcr_comp__v_g1l_noret" if M == 1 else "srcr_c"
for s in subs:
    idx = X[s].index
    ch = {"peer_phys": PR.to_steps(zp[s], idx), "peer_comfort": PR.to_steps(zc[s], idx),
          "peer_all": PR.to_steps(pd.concat([zp[s], zc[s]], axis=1), idx), "own_change": PR.to_steps(zo[s], idx)}
    srcr = R.load_scores(srcr_name, M, s).reindex(idx)
    ch["fuse_peer_srcr"] = pd.Series(np.fmax(ch["peer_all"].to_numpy(), srcr.to_numpy()), index=idx)
    for name, sc in ch.items():
        d = R.score_path(name, M); os.makedirs(d, exist_ok=True)
        pd.DataFrame({"score": sc.astype(float)}).to_parquet(os.path.join(d, f"s{s}.parquet"))
print("scores written", flush=True)
if M == 1:
    from src.evaluation.diagnose import fault_ranks
    res = []
    for name in ["peer_phys", "peer_comfort", "peer_all", "own_change", "fuse_peer_srcr"]:
        t, _ = R.best_at_budgets(name, 1); res.append(t)
        fr = fault_ranks(name, 1)[0]
        print(name, "| top2%:", int((fr.rank_frac <= .02).sum()), "| hydraulic in top2%:",
              fr[fr.rank_frac <= .02]["Fault label"].tolist(), flush=True)
        print(t[["budget", "tau", "c_thr", "recall", "fa_per_sub_year"]].round(3).to_string(index=False), flush=True)
    pd.concat(res).to_csv("results/round5_peer_m1.csv", index=False)
    # reference: best existing cells threshold-free
    for name in ["srcr_comp__v_g1l_noret", "rule", "loop3s_c", "sigma3", "ae", "qnbm", "ae_comfort"]:
        fr = fault_ranks(name, 1)[0]
        print("REF", name, "top2%:", int((fr.rank_frac <= .02).sum()), flush=True)
