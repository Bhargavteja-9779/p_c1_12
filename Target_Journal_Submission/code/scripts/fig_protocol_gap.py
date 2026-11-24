"""Figure: protocol gap (F19). For each method at its event-F0.5-optimal operating point:
(a) event-protocol precision vs continuous alarm precision (log scale, dumbbell);
(b) false alarms per substation-year that operating point produces under continuous monitoring (budget B = 2 marked).
One row per manufacturer whose results/protocol_gap/m{M}_gap.csv exists. Output: figures/fig_protocol_gap.{png,pdf}"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAMES = {"rule": "Setpoint rule", "sigma3": "Three-sigma", "loop3s": "Loop three-sigma", "iforest": "Isolation Forest",
         "qnbm": "Quantile NBM", "ae": "Autoencoder (benchmark)", "ae_cond": "Conditional AE",
         "srcr_comp__v_gate_1s_local": "SRCR (fleet)"}
EV, CO, INK, INK2, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"
ms = [m for m in (1, 2) if os.path.exists(f"results/protocol_gap/m{m}_gap.csv")]
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(len(ms), 2, figsize=(7.2, 2.9 * len(ms)), squeeze=False, gridspec_kw={"width_ratios": [1.2, 1]})
for i, m in enumerate(ms):
    g = pd.read_csv(f"results/protocol_gap/m{m}_gap.csv")
    g = g.sort_values("cont_fa_per_sub_year").reset_index(drop=True)
    y = range(len(g)); lab = [NAMES.get(x, x) for x in g.method]
    a = axes[i, 0]
    for k, r in g.iterrows():
        a.plot([r.cont_alarm_precision, r.ev_precision], [k, k], color=GRID, lw=2, zorder=1)
    a.scatter(g.ev_precision, y, s=40, color=EV, zorder=3, label="Balanced event protocol", edgecolor="white", linewidth=1.5)
    a.scatter(g.cont_alarm_precision, y, s=40, color=CO, zorder=3, label="Continuous monitoring", edgecolor="white", linewidth=1.5, marker="s")
    for k, r in g.iterrows():
        a.text(r.ev_precision * 1.3, k, f"{r.precision_ratio:.0f}x", va="center", fontsize=8, color=INK2)
    a.set_xscale("log"); a.set_xlim(0.002, 3); a.set_ylim(-1.4, len(g) - 0.5); a.set_yticks(list(y)); a.set_yticklabels(lab)
    a.set_xlabel("Precision of alarms (log scale)"); a.grid(axis="x", color=GRID, lw=0.6); a.set_axisbelow(True)
    a.set_title(f"({'ac'[i]}) Manufacturer {m}: precision", loc="left", fontsize=9, color=INK)
    if i == 0:
        a.legend(frameon=False, fontsize=8, loc="lower left", bbox_to_anchor=(0, 1.08), ncol=2)
    b = axes[i, 1]
    b.barh(list(y), g.cont_fa_per_sub_year, color=CO, height=0.6)
    b.axvline(2, color=INK, lw=1, ls="--"); b.text(2.3, -0.9, "budget B = 2", fontsize=8, color=INK, va="center")
    for k, r in g.iterrows():
        b.text(max(r.cont_fa_per_sub_year, 2) + 0.3, k, f"{r.cont_fa_per_sub_year:.1f}", va="center", fontsize=8, color=INK2)
    b.set_yticks(list(y)); b.set_yticklabels([]); b.set_xlabel("False alarms per substation-year")
    b.grid(axis="x", color=GRID, lw=0.6); b.set_axisbelow(True)
    b.set_xlim(0, max(g.cont_fa_per_sub_year) * 1.18); b.set_ylim(-1.4, len(g) - 0.5)
    b.set_title(f"({'bd'[i]}) Same operating point, continuous", loc="left", fontsize=9, color=INK)
fig.tight_layout()
os.makedirs("../figures", exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(f"../figures/fig_protocol_gap.{ext}", dpi=300, bbox_inches="tight")
print("saved", ms)
