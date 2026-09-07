# -*- coding: utf-8 -*-
"""Verifica el lienzo antes de abrirlo: solapes y textos fuera de su recuadro."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(os.path.dirname(HERE), "problema2.excalidraw")
d = json.load(open(path, encoding="utf-8"))
E = d["elements"]

ZONE = "#adb5bd"


def bb(e):
    return e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"]


def inter(a, b, pad=0):
    ax1, ay1, ax2, ay2 = bb(a)
    bx1, by1, bx2, by2 = bb(b)
    return not (ax2 <= bx1 + pad or bx2 <= ax1 + pad or
                ay2 <= by1 + pad or by2 <= ay1 + pad)


zonas = [e for e in E if e["type"] == "rectangle"
         and e["strokeStyle"] == "dashed" and e["width"] > 400]
zids = {id(z) for z in zonas}
cajas = [e for e in E if e["type"] in ("rectangle", "ellipse") and id(e) not in zids]
textos = [e for e in E if e["type"] == "text"]

fallos = 0

# 1. cajas que se pisan entre sí
for i, a in enumerate(cajas):
    for b in cajas[i + 1:]:
        if inter(a, b, pad=1):
            print("SOLAPE cajas", bb(a), bb(b))
            fallos += 1

# 2. texto que se sale de la caja que lo contiene (mismo centro)
for t in textos:
    tx1, ty1, tx2, ty2 = bb(t)
    for k in cajas:
        kx1, ky1, kx2, ky2 = bb(k)
        cx, cy = (tx1 + tx2) / 2, (ty1 + ty2) / 2
        if kx1 <= cx <= kx2 and ky1 <= cy <= ky2:
            if tx1 < kx1 - 1 or tx2 > kx2 + 1 or ty1 < ky1 - 1 or ty2 > ky2 + 1:
                print("DESBORDA", repr(t["text"][:40]), bb(t), "en", bb(k))
                fallos += 1
            break

# 3. texto suelto que pisa una caja ajena
for t in textos:
    tx1, ty1, tx2, ty2 = bb(t)
    cx, cy = (tx1 + tx2) / 2, (ty1 + ty2) / 2
    dentro = any(kx1 <= cx <= kx2 and ky1 <= cy <= ky2
                 for kx1, ky1, kx2, ky2 in map(bb, cajas))
    if dentro:
        continue
    for k in cajas:
        if inter(t, k, pad=2):
            print("TEXTO PISA CAJA", repr(t["text"][:40]), bb(t), "vs", bb(k))
            fallos += 1

# 4. elementos fuera de la banda de su zona
for z in zonas:
    zx1, zy1, zx2, zy2 = bb(z)
    for e in E:
        if e is z or e["type"] in ("line",):
            continue
        ex1, ey1, ex2, ey2 = bb(e)
        cx, cy = (ex1 + ex2) / 2, (ey1 + ey2) / 2
        if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
            if ex1 < zx1 - 1 or ex2 > zx2 + 1 or ey1 < zy1 - 1 or ey2 > zy2 + 1:
                print("FUERA DE ZONA", e["type"], repr((e.get("text") or "")[:40]),
                      bb(e), "zona", bb(z))
                fallos += 1

xs = [e["x"] for e in E] + [e["x"] + e["width"] for e in E]
ys = [e["y"] for e in E] + [e["y"] + e["height"] for e in E]
print(f"{len(E)} elementos  lienzo {min(xs):.0f},{min(ys):.0f}  a  {max(xs):.0f},{max(ys):.0f}")
print("OK" if not fallos else f"{fallos} problemas")
sys.exit(1 if fallos else 0)
