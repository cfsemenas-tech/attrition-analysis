"""
Generates a before/after visual showing where confirmed fraud transactions
were classified under the old (broken) vs. new (fixed) scoring logic.
Saved to: output/fraud_detection_before_after.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

os.makedirs("output", exist_ok=True)

COLORS = {
    "high":   "#C0392B",
    "medium": "#E67E22",
    "low":    "#27AE60",
    "bg":     "#F7F9FC",
    "text":   "#2C3E50",
    "subtext":"#7F8C8D",
}

before = {"High Risk": 0, "Medium Risk": 0, "Low Risk": 8}
after  = {"High Risk": 7, "Medium Risk": 1, "Low Risk": 0}
total  = 8

fig = plt.figure(figsize=(13, 7), facecolor=COLORS["bg"])
fig.patch.set_facecolor(COLORS["bg"])

gs = gridspec.GridSpec(
    1, 3, width_ratios=[2, 0.2, 2], left=0.07, right=0.96,
    top=0.82, bottom=0.18, wspace=0.55
)

ax_before = fig.add_subplot(gs[0])
ax_after  = fig.add_subplot(gs[2])

for ax in (ax_before, ax_after):
    ax.set_facecolor(COLORS["bg"])

bar_colors = [COLORS["high"], COLORS["medium"], COLORS["low"]]
labels = ["High Risk", "Medium Risk", "Low Risk"]
y = np.arange(len(labels))
height = 0.52

def draw_bars(ax, data, title, is_after=False):
    values = [data[l] for l in labels]
    bars = ax.barh(y, values, height=height, color=bar_colors,
                   edgecolor="white", linewidth=1.2, zorder=3)

    ax.set_xlim(0, 9.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=13, color=COLORS["text"], fontweight="bold")
    ax.set_xlabel("Confirmed Fraud Transactions (out of 8)", fontsize=10,
                  color=COLORS["subtext"], labelpad=8)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.tick_params(axis="x", colors=COLORS["subtext"])
    ax.tick_params(axis="y", length=0)

    for bar, val in zip(bars, values):
        label_x = val + 0.15 if val > 0 else 0.15
        pct = f"{int(round(val/total*100))}%"
        ax.text(label_x, bar.get_y() + bar.get_height() / 2,
                f"{val} ({pct})", va="center", ha="left",
                fontsize=12, fontweight="bold", color=COLORS["text"])

    color = "#C0392B" if not is_after else "#1A5276"
    ax.set_title(title, fontsize=15, fontweight="bold", color=color,
                 pad=14, loc="center")

draw_bars(ax_before, before, "BEFORE FIX", is_after=False)
draw_bars(ax_after,  after,  "AFTER FIX",  is_after=True)

ax_mid = fig.add_subplot(gs[1])
ax_mid.set_facecolor(COLORS["bg"])
ax_mid.axis("off")
ax_mid.annotate("", xy=(0.85, 0.5), xytext=(0.15, 0.5),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="#2C3E50",
                                lw=2.5, mutation_scale=20))

fig.suptitle(
    "Where Did Confirmed Fraud Land? — Before vs. After the Logic Fix",
    fontsize=16, fontweight="bold", color=COLORS["text"], y=0.95
)

fig.text(
    0.5, 0.055,
    "4 scoring signals were inverted: high-risk devices, international transactions, "
    "card-testing velocity, and prior chargebacks\n"
    "all lowered the fraud score instead of raising it.  Fixing the signs moved 7 of 8 "
    "confirmed fraud cases from Low → High Risk.",
    ha="center", fontsize=9.5, color=COLORS["subtext"], style="italic",
    wrap=True
)

plt.savefig("output/fraud_detection_before_after.png", dpi=150, bbox_inches="tight")
print("Chart saved to output/fraud_detection_before_after.png")
