"""Run a per-substation detector online on one manufacturer. Usage: run_online_method.py METHOD M [k/n] [seed]"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import torch; torch.set_num_threads(1)
from src.data import predist as P
from src.evaluation import runner as R
from src.models import online as O
from src.models import baselines as B
from src.models.ae import AEDetector
from src.models.channels import IntentChannel, DeliveryChannel, UnderDeliveryChannel
method, m = sys.argv[1], int(sys.argv[2])
part = sys.argv[3] if len(sys.argv) > 3 and "/" in sys.argv[3] else None
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
FACT = {"rule": lambda: B.RuleShortfall(), "sigma3": lambda: B.ThreeSigma(), "iforest": lambda: B.IForest(seed),
        "loop3s": lambda: B.LoopThreeSigma(), "qnbm": lambda: B.OwnQuantileNBM(seed),
        "intent": lambda: IntentChannel(seed), "delivery": lambda: DeliveryChannel(seed), "underdel": lambda: UnderDeliveryChannel(seed),
        "ae": lambda: AEDetector(conditional=False, seed=seed), "ae_cond": lambda: AEDetector(conditional=True, seed=seed),
        "loop3s_c": lambda: B.LoopThreeSigmaComfort(),
        "ae_comfort": lambda: AEDetector(conditional=False, seed=seed, columns=B.comfort_columns())}
subs = P.substations(m)
if part: k, n = map(int, part.split("/")); subs = subs[k::n]
name = method if seed == 0 else f"{method}_seed{seed}"
R.compute_scores(name, m, lambda X, lab: O.run_online(X, lab, FACT[method]), subs=subs)
