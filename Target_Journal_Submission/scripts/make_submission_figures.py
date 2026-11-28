"""Figures for the submission. Reads committed result files only (no new analysis).
PreDist = leak-free primary (D-30); CARE = plan_v2. Run from Target_Journal_Submission/."""
import json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = "code/results"; OUT = "submission/figures"
BLUE, ORANGE, INK, INK2, GRID = "#257de0", "#f47230", "#191919", "#666666", "#e6e6e6"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "font.family": "DejaVu Sans"})
DS = {"PreDist (district heating)": f"{R}/leak_sensitivity/leakfree_outputs/seed0",
      "CARE (wind turbines)": f"{R}/plan_v2/care/seed0"}
LBL = {"ET": "Event windows,\ntest-tuned\nthresholds", "EH": "Event windows,\nout-of-sample\nthresholds",
       "CT": "Continuous,\ntest-tuned\nthresholds"}

# Fig 2: Kendall tau with deployment-like reference (CH), per cell, bootstrap 95% CI.
# PreDist: leak-free primary (filled + CI); legacy exclusion rule = hollow sensitivity marker.
F2 = {"PreDist (district heating)": (f"{R}/leak_sensitivity/leakfree_outputs/seed0", f"{R}/plan_v2/predist1/seed0"),
      "CARE (wind turbines)": (f"{R}/plan_v2/care/seed0", None)}
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
for ax, (name, (d, lf)) in zip(axs, F2.items()):
    s = json.load(open(f"{d}/summary.json")); b = pd.read_csv(f"{d}/bootstrap.csv")
    for i, c in enumerate(["ET", "EH", "CT"]):
        lo, hi = np.percentile(b[f"tau_{c}"], [2.5, 97.5]); v = s[f"tau_{c}"]
        col = ORANGE if c == "ET" else BLUE
        ax.plot([i, i], [lo, hi], color=col, lw=2, solid_capstyle="round")
        ax.plot(i, v, "o", ms=8, color=col, mec="white", mew=2, zorder=3)
        ax.annotate(f"{v:.2f}", (i, v), xytext=(-12, -3), textcoords="offset points", color=INK, fontsize=8, ha="right")
        if lf:
            w = json.load(open(f"{lf}/summary.json"))[f"tau_{c}"]
            ax.plot(i + 0.22, w, "o", ms=7, mfc="white", mec=col, mew=1.8, zorder=3)
            ax.annotate(f"{w:.2f}", (i + 0.22, w), xytext=(7, -3), textcoords="offset points", color=INK2, fontsize=7)
    ax.set_xticks(range(3)); ax.set_xticklabels([LBL[c] for c in ["ET", "EH", "CT"]], fontsize=7.5)
    ax.set_xlim(-0.5, 2.8); ax.axhline(0, color=INK2, lw=0.8); ax.set_ylim(-0.5, 1.05)
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_title(f"{name}\n{s['n_detectors']} detectors, {s['n_assets']} assets, seed 0", fontsize=9, color=INK)
axs[0].plot([], [], "o", color=INK2, label="estimate, 95% bootstrap CI"); axs[0].plot([], [], "o", mfc="white", mec=INK2, label="legacy exclusion rule (sensitivity)")
axs[0].legend(fontsize=7, frameon=False, loc="lower right")
axs[0].set_ylabel("Kendall's tau with the\ndeployment-like ranking (CH)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig2_tau_by_cell.png", dpi=300); fig.savefig(f"{OUT}/fig2_tau_by_cell.pdf")

# Fig 3: benchmark score (ET, event F0.5) vs deployment recall (CH) per detector
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.2))
for ax, (name, d) in zip(axs, DS.items()):
    c = pd.read_csv(f"{d}/cells.csv")
    ax.scatter(c.ET, c.CH, s=40, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3)
    top_et = c.loc[c.ET.idxmax()]; top_ch = c.loc[c.CH.idxmax()]
    for r, tag in [(top_et, "best on benchmark"), (top_ch, "best in deployment")]:
        ax.annotate(f"{r.detector}\n({tag})", (r.ET, r.CH), xytext=(-60, 12 if tag.endswith("t") else -26),
                    textcoords="offset points", fontsize=7, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
    ax.set_xlabel("Benchmark score: event F0.5,\nthresholds tuned on the evaluated events (ET)")
    ax.set_title(name, fontsize=9, color=INK); ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_ylim(-0.02, max(0.36, c.CH.max() + 0.05))
axs[0].set_ylabel("Deployment-like recall (CH):\ncontinuous, out-of-sample, 2 FA/asset-yr")
fig.tight_layout(); fig.savefig(f"{OUT}/fig3_benchmark_vs_deployment.png", dpi=300); fig.savefig(f"{OUT}/fig3_benchmark_vs_deployment.pdf")

# Fig 4: selection effect: alarm-hit ratio curated normal events / random normal windows, per detector
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.8), sharex=True)
for ax, (name, d) in zip(axs, DS.items()):
    p = pd.read_csv(f"{d}/selection_per_detector.csv").sort_values("ratio", na_position="first")
    y = np.arange(len(p)); r = p.ratio.clip(upper=2.0).fillna(0)
    ax.barh(y, r, height=0.6, color=BLUE)
    for yi, (raw, rr) in enumerate(zip(p.ratio, r)):
        if pd.isna(raw): ax.text(0.03, yi, "undefined (no alarms)", va="center", fontsize=6.5, color=INK2)
        elif raw == 0: ax.text(0.03, yi, "0", va="center", fontsize=6.5, color=INK2)
        elif raw > 2: ax.text(1.97, yi, f"{raw:.2f} (axis cut)", va="center", ha="right", fontsize=6.5, color="white")
    ax.axvline(1, color=INK, lw=1, ls="--")
    ax.set_yticks(y); ax.set_yticklabels(p.detector, fontsize=7); ax.set_title(name, fontsize=9, color=INK)
    ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True); ax.set_xlim(0, 2.05)
    ax.set_xlabel("Alarm-hit rate ratio, curated normal\nevents / random normal windows (1 = equal)", fontsize=8)
fig.tight_layout(); fig.savefig(f"{OUT}/fig4_selection_effect.png", dpi=300); fig.savefig(f"{OUT}/fig4_selection_effect.pdf")

# Fig 5: robustness across seeds (PreDist legacy seeds 0-4 + leak-free seed 0; CARE seeds 0-4)
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
for ax, (name, base) in zip(axs, [("PreDist", f"{R}/plan_v2/predist1"), ("CARE", f"{R}/plan_v2/care")]):
    for k, (h, col) in enumerate([("H7a", BLUE), ("H7b", ORANGE)]):
        ps = [json.load(open(f"{base}/seed{s}/summary.json"))[f"{h}_p"] for s in range(5)]
        ax.plot(np.arange(5) + (k - 0.5) * 0.15, ps, "o", ms=8, color=col, mec="white", mew=2,
                label={"H7a": "H7a threshold source", "H7b": "H7b window design"}[h])
    ax.axhline(0.05, color=INK, lw=1, ls="--"); ax.set_yscale("log"); ax.set_xticks(range(5))
    ax.set_xticklabels([f"seed {s}" for s in range(5)], fontsize=7.5); ax.set_title(name + " (legacy exclusion rule)" if name=="PreDist" else name, fontsize=8.5, color=INK); ax.set_ylim(1e-3, 1)
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
axs[0].set_ylabel("One-sided bootstrap p"); axs[0].legend(fontsize=7, frameon=False, loc="upper left", ncol=2)
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_seed_robustness.png", dpi=300); fig.savefig(f"{OUT}/fig5_seed_robustness.pdf")
print("ok")
