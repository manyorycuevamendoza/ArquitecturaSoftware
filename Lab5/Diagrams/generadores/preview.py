# -*- coding: utf-8 -*-
"""Vista previa aproximada del lienzo, para revisar la composición sin abrir Excalidraw."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyArrow

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "problema2.excalidraw")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    os.environ.get("TEMP") or "/tmp", "problema2-preview.png")
E = json.load(open(src, encoding="utf-8"))["elements"]

xs = [e["x"] for e in E] + [e["x"] + e["width"] for e in E]
ys = [e["y"] for e in E] + [e["y"] + e["height"] for e in E]
W, H = max(xs) - min(xs), max(ys) - min(ys)
fig, ax = plt.subplots(figsize=(W / 60, H / 60), dpi=100)

for e in E:
    x, y, w, h = e["x"], e["y"], e["width"], e["height"]
    col = e.get("strokeColor", "#000")
    ls = "--" if e.get("strokeStyle") == "dashed" else "-"
    if e["type"] == "rectangle":
        ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=col, ls=ls, lw=1))
    elif e["type"] == "ellipse":
        ax.add_patch(Ellipse((x + w / 2, y + h / 2), w, h, fill=False, ec=col, lw=1))
    elif e["type"] in ("arrow", "line"):
        p = e["points"]
        ax.plot([x + p[0][0], x + p[-1][0]], [y + p[0][1], y + p[-1][1]],
                color=col, ls=ls, lw=1)
    elif e["type"] == "text":
        fs = e["fontSize"]
        lines = e["text"].split("\n")
        mono = e.get("fontFamily") == 3
        ha = {"left": "left", "center": "center"}[e.get("textAlign", "left")]
        tx = x + (w / 2 if ha == "center" else 0)
        for i, ln in enumerate(lines):
            ax.text(tx, y + (i + 0.85) * fs * 1.25, ln, fontsize=fs * 0.78,
                    color=col, ha=ha, va="baseline",
                    family="monospace" if mono else "sans-serif")

ax.set_xlim(min(xs) - 20, max(xs) + 20)
ax.set_ylim(max(ys) + 20, min(ys) - 20)
ax.axis("off")
fig.tight_layout(pad=0)
fig.savefig(out, facecolor="white")
print(out)
