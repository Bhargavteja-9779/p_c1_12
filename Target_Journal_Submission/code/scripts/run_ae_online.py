import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import torch; torch.set_num_threads(1)
from src.evaluation import runner as R
from src.models import online as O
from src.models.ae import AEDetector
m = int(sys.argv[1]); cond = sys.argv[2] == "cond"; part = sys.argv[3] if len(sys.argv) > 3 else None
from src.data import predist as P
subs = P.substations(m)
if part: k, n = map(int, part.split("/")); subs = subs[k::n]
name = "ae_cond" if cond else "ae"
R.compute_scores(name, m, lambda X, lab: O.run_online(X, lab, lambda: AEDetector(conditional=cond)), subs=subs)
