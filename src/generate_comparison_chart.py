"""
Generates a side-by-side bar chart comparing the old (buggy) vs. new (correct)
attrition rate calculation by job satisfaction level.
Saved to: output/satisfaction_rate_comparison.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_csv("data/employees.csv")

grouped = (
    df.groupby("job_satisfaction")
    .agg(
        total_employees=("employee_id", "count"),
        leavers=("attrition", lambda s: (s == "Yes").sum()),
    )
    .reset_index()
)

total_leavers = (df["attrition"] == "Yes").sum()
grouped["old_rate"] = round((grouped["leavers"] / total_leavers) * 100, 2)
grouped["new_rate"] = round((grouped["leavers"] / grouped["total_employees"]) * 100, 2)

labels = [f"Satisfaction\nLevel {int(v)}" for v in grouped["job_satisfaction"]]
x = range(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#F7F9FC")
ax.set_facecolor("#F7F9FC")

bars_old = ax.bar(
    [i - width / 2 for i in x],
    grouped["old_rate"],
    width,
    color="#E07070",
    label="Old formula (wrong): share of all leavers",
    zorder=3,
)
bars_new = ax.bar(
    [i + width / 2 for i in x],
    grouped["new_rate"],
    width,
    color="#4A90D9",
    label="New formula (correct): % of group who left",
    zorder=3,
)

ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylabel("Attrition Rate (%)", fontsize=12)
ax.set_title(
    "What Changed: Attrition Rate by Job Satisfaction\n"
    "Old formula measured share of leavers — New formula measures who actually left",
    fontsize=13,
    fontweight="bold",
    pad=16,
)
ax.yaxis.grid(True, linestyle="--", alpha=0.7, zorder=0)
ax.set_axisbelow(True)

for bar in bars_old:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{bar.get_height():.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
        color="#C0392B",
        fontweight="bold",
    )
for bar in bars_new:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{bar.get_height():.1f}%",
        ha="center",
        va="bottom",
        fontsize=10,
        color="#1A5276",
        fontweight="bold",
    )

red_patch = mpatches.Patch(color="#E07070", label="Old formula: % share of ALL leavers (misleading)")
blue_patch = mpatches.Patch(color="#4A90D9", label="New formula: % of each group who left (accurate)")
ax.legend(handles=[red_patch, blue_patch], loc="upper right", fontsize=10, framealpha=0.9)

note = (
    "Example: Level 1 employees didn't suddenly become less of a risk — the old\n"
    "number just told you their share of departures, not their actual leave rate."
)
fig.text(0.5, -0.04, note, ha="center", fontsize=9, color="#555555", style="italic")

os.makedirs("output", exist_ok=True)
plt.tight_layout()
plt.savefig("output/satisfaction_rate_comparison.png", dpi=150, bbox_inches="tight")
print("Chart saved to output/satisfaction_rate_comparison.png")
