"""Fig: deployment-like recall across false-alarm budgets (A2 cells), benchmark winner vs deployment winner.
Usage: python3 scripts/make_fig_operator_curves.py PREDIST_VERSION  (legacy|leakfree)"""
import sys, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
V = sys.argv[1] if len(sys.argv) > 1 else "legacy"
D = "code/results/plan_v2/amendment_A2"; BS = [0.5, 1.0, 2.0, 4.0, 8.0]
BLUE, ORANGE, INK, INK2, GRID, GRAY = "#257de0", "#f47230", "#191919", "#666666", "#e6e6e6", "#c8c8c8"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2})
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.2), sharey=True)
for ax, (name, f) in zip(axs, [(f"PreDist ({ {'leakfree': 'leak-free'}.get(V, V)} rule)", f"{D}/predist1_{V}_seed0_cells.csv"), ("CARE", f"{D}/care_primary_seed0_cells.csv")]):
    X = pd.read_csv(f); be = X.loc[X.ET.idxmax()]; de = X.loc[X.CHA.idxmax()]
    for _, r in X.iterrows():
        ax.plot(BS, [r[f"CH_{b}"] for b in BS], color=GRAY, lw=1, zorder=1)
    for r, col, tag, dy in [(be, ORANGE, "benchmark winner", -14), (de, BLUE, "deployment winner", 8)]:
        y = [r[f"CH_{b}"] for b in BS]
        ax.plot(BS, y, color=col, lw=2.2, marker="o", ms=6, mec="white", mew=1.5, zorder=3, label=f"{tag}: {r.detector}")
    ax.set_xscale("log", base=2); ax.set_xticks(BS); ax.set_xticklabels(["0.5", "1", "2", "4", "8"])
    ax.set_xlabel("False-alarm budget B (per asset-year,\nthreshold chosen on held-out assets)"); ax.set_title(name, fontsize=9, color=INK)
    ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
axs[0].set_ylabel("Recall in continuous replay (CH_B)")
for ax in axs:
    ax.plot([], [], color=GRAY, lw=1, label="other detectors"); ax.legend(fontsize=7, frameon=False, loc="upper left")
axs[0].set_ylim(0, 0.62)
fig.tight_layout(); fig.savefig("submission/figures/fig5_operator_budget_curves.png", dpi=300); fig.savefig("submission/figures/fig5_operator_budget_curves.pdf")
print("ok")
