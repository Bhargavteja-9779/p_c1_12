"""Fig. 1 / graphical abstract: the 2x2 protocol design. No data."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BLUE, ORANGE, INK, INK2, BG = "#257de0", "#f47230", "#191919", "#666666", "#f4f4f4"
fig, ax = plt.subplots(figsize=(7.2, 3.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
def box(x, y, w, h, title, body, edge, fill="white", lw=1.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fill, ec=edge, lw=lw))
    ax.text(x + w / 2, y + h - 0.28, title, ha="center", va="top", fontsize=8.5, weight="bold", color=INK)
    ax.text(x + w / 2, y + h - 0.68, body, ha="center", va="top", fontsize=7, color=INK2, linespacing=1.35)
# left: shared inputs
box(0.1, 1.2, 2.2, 2.6, "Same online scores", "15-17 detectors\nretrained every 90 d\non each asset's past\n\nPreDist: 35 substations\nCARE: 36 turbines", INK2, BG)
ax.annotate("", xy=(2.75, 2.5), xytext=(2.35, 2.5), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
# 2x2 grid
ax.text(5.05, 4.75, "Thresholds tuned on\nthe evaluated events", ha="center", va="center", fontsize=7.5, color=INK)
ax.text(7.75, 4.75, "Thresholds chosen\nout of sample (B FA/asset-yr)", ha="center", va="center", fontsize=7.5, color=INK)
ax.text(3.05, 3.35, "Event\nwindows", ha="center", va="center", fontsize=7.5, color=INK, rotation=90)
ax.text(3.05, 1.35, "Continuous\nreplay", ha="center", va="center", fontsize=7.5, color=INK, rotation=90)
box(3.7, 2.45, 2.7, 1.8, "ET  benchmark practice", "balanced fault + curated\nnormal windows, event F0.5\n\nlooks good: F0.5 0.57-0.84", ORANGE)
box(6.4 + 0.05, 2.45, 2.7, 1.8, "EH", "same windows,\nheld-out threshold", BLUE)
box(3.7, 0.45, 2.7, 1.8, "CT", "every 10-min step,\nin-sample threshold", BLUE)
box(6.4 + 0.05, 0.45, 2.7, 1.8, "CH  deployment-like", "every step, held-out\nthreshold, recall at budget\n\nfinds 0-32% of faults", BLUE, "#e8f1fc", 2.2)
ax.text(9.95, 0.05, "Measured: false-alarm burden of ET thresholds; curated-normal bias; rank agreement with CH",
        ha="right", va="bottom", fontsize=7, color=INK2, style="italic")
fig.tight_layout(); fig.savefig("submission/figures/fig1_protocol_design.png", dpi=300); fig.savefig("submission/figures/fig1_protocol_design.pdf")
