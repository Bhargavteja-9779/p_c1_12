"""Regenerate every manuscript figure from result CSVs (no number is typed by hand).
Usage: make_figures.py  -> ../manuscript/figures/fig*.png (300 dpi) + .pdf
Palette: validated categorical slots (blue, orange, aqua); every series also has its own marker and a
direct label, so the figures read in grayscale and for colour-vision deficiency.
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(HERE, "..", "..", "manuscript", "figures")
os.makedirs(OUT, exist_ok=True)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "legend.frameon": False, "savefig.dpi": 300, "savefig.bbox": "tight"})
LABEL = {"rule": "Rule", "loop3s_c": "Loop-3σ-C", "srcr_c": "SRCR-C", "loop3s": "Loop-3σ", "srcr_all": "SRCR-all",
         "ae_comfort": "AE-comfort", "sigma3": "3σ", "iforest": "iForest", "qnbm": "qNBM", "ae": "AE (PreDist)",
         "ae_cond": "AE-cond"}


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"))
    plt.close(fig); print("wrote", name)


def fig_transfer():
    """M1 (development, in-sample thresholds) vs M2 (locked) recall at a budget of 2 false alarms/sub-yr."""
    o = pd.read_csv(os.path.join(RES, "locked_m2_operating_points.csv")); o = o[o.budget == 2].copy()
    o = o.sort_values("m1_recall")
    fig, ax = plt.subplots(figsize=(3.5, 3.4))
    y = np.arange(len(o))
    for yi, (_, r) in zip(y, o.iterrows()):
        ax.plot([r.recall, r.m1_recall], [yi, yi], color=GRID, lw=2, zorder=1)
    ax.scatter(o.m1_recall, y, s=28, marker="o", color=BLUE, label="Manufacturer 1 (development)", zorder=3,
               edgecolor="white", linewidth=0.8)
    ax.scatter(o.recall, y, s=30, marker="s", color=ORANGE, label="Manufacturer 2 (locked test)", zorder=3,
               edgecolor="white", linewidth=0.8)
    ax.set_yticks(y, [LABEL[c] for c in o.cell]); ax.set_xlabel("Share of faults detected (recall)")
    ax.set_xlim(-0.02, 0.5); ax.grid(axis="y", visible=False)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=1, fontsize=7, handletextpad=0.3)
    save(fig, "fig_transfer")


def fig_chance():
    """Observed recall vs recall of random alarms at the same achieved false-alarm rate (M2)."""
    d = pd.read_csv(os.path.join(RES, "chance_level.csv")); d = d[(d.m == 2) & (d.budget == 2)].sort_values("recall")
    fig, ax = plt.subplots(figsize=(3.5, 3.4)); y = np.arange(len(d))
    for yi, (_, r) in zip(y, d.iterrows()):
        ax.plot([r.chance_recall, r.recall], [yi, yi], color=GRID, lw=2, zorder=1)
    ax.scatter(d.chance_recall, y, s=26, marker="D", color=MUTED, label="Random alarms, same rate", zorder=3)
    ax.scatter(d.recall, y, s=30, marker="s", color=ORANGE, label="Detector", zorder=3, edgecolor="white", linewidth=0.8)
    for yi, (_, r) in zip(y, d.iterrows()):
        if r.above_chance_holm05:
            ax.annotate("above chance*", (r.recall, yi), xytext=(6, -3), textcoords="offset points", fontsize=6.5, color=INK)
    ax.set_yticks(y, [LABEL[c] for c in d.cell]); ax.set_xlabel("Share of faults detected, manufacturer 2")
    ax.set_xlim(-0.01, 0.42); ax.grid(axis="y", visible=False); ax.legend(loc="lower right", fontsize=7)
    ax.set_title("* one-sided binomial test, Holm-corrected over 66 tests", fontsize=6.5, color=MUTED, loc="left")
    save(fig, "fig_chance")


def fig_certification():
    """T1: false-alarm burden a balanced protocol can certify with n clean normal weeks (95% upper bound)."""
    wk = 365.25 / 7; n = np.arange(10, 400)
    qu = 1 - 0.05 ** (1 / n)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.plot(n, qu * wk, color=BLUE, lw=2)
    for nn, lab in ((30, "PreDist M2 (30)"), (35, "M1 (35)"), (65, "both (65)"), (155, "155")):
        v = (1 - 0.05 ** (1 / nn)) * wk
        ax.scatter([nn], [v], s=22, color=ORANGE, marker="o", zorder=3, edgecolor="white", linewidth=0.8)
        ax.annotate(f"{lab}: ≤{v:.1f}", (nn, v), xytext=(6, 4), textcoords="offset points", fontsize=6.5, color=INK)
    ax.set_xlabel("Normal weeks in the benchmark, all without a false alarm")
    ax.set_ylabel("Certifiable alarm-weeks per\nsubstation-year (95% upper bound)")
    ax.set_ylim(0, 8)
    save(fig, "fig_certification")


def fig_cold_start():
    d = pd.read_csv(os.path.join(RES, "secondary_cold_start.csv")); d = d[d.m == 2]
    bins = [b for b in ("<90 d", "90-365 d", ">365 d") if b in set(d.bin)]
    piv = d.pivot_table(index="cell", columns="bin", values="recall").reindex(columns=bins)
    nf = d.groupby("bin").n_faults.first().reindex(bins)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    x = np.arange(len(bins)); best = piv.max(axis=0); med = piv.median(axis=0)
    ax.bar(x - 0.18, best, width=0.34, color=BLUE, label="Best detector")
    ax.bar(x + 0.18, med, width=0.34, color=AQUA, hatch="///", edgecolor="white", label="Median detector")
    for xi, v in zip(x - 0.18, best): ax.annotate(f"{v:.2f}", (xi, v), xytext=(0, 2), textcoords="offset points", ha="center", fontsize=6.5, color=INK)
    for xi, v in zip(x + 0.18, med): ax.annotate(f"{v:.2f}", (xi, v), xytext=(0, 2), textcoords="offset points", ha="center", fontsize=6.5, color=INK)
    ax.set_xticks(x, [f"{b}\n(n={int(nf[b])} faults)" for b in bins]); ax.set_ylabel("Recall, manufacturer 2")
    ax.set_xlabel("Substation history before the fault report"); ax.legend(fontsize=7); ax.grid(axis="x", visible=False)
    save(fig, "fig_cold_start")


if __name__ == "__main__":
    for f in (fig_transfer, fig_chance, fig_certification, fig_cold_start):
        try:
            f()
        except FileNotFoundError as e:
            print("skip", f.__name__, e)
