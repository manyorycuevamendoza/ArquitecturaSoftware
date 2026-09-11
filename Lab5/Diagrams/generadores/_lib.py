# -*- coding: utf-8 -*-
"""Librería de dibujo para los diagramas del Problema 1 de RemoteSchooly.

Estilo fijo: fondo transparente en todas las figuras, el color vive en el borde.
"""
import json

TS = 1725494400000
LH = 1.25

# paleta de bordes
ACTOR = "#1971c2"   # azul       personas
SERV  = "#e03131"   # rojo       servicios que mueven datos
LOGIC = "#6741d9"   # morado     componentes que deciden
DB    = "#0c8599"   # cyan       bases de datos y almacenes
OK    = "#2f9e44"   # verde      resultado bueno
WARN  = "#e8590c"   # naranja    resultado degradado
BAD   = "#c92a2a"   # rojo       fallo o rechazo
ZONE  = "#adb5bd"   # gris       zonas y marcos
MUTE  = "#868e96"   # gris texto secundario
INK   = "#1e1e1e"
BODY  = "#3f3f46"


class Canvas:
    def __init__(self):
        self.E = []

    def _add(self, el):
        el["seed"] = 1
        el["updated"] = TS
        el["link"] = None
        el["locked"] = False
        el["angle"] = 0
        el["opacity"] = 100
        el["groupIds"] = []
        el["boundElements"] = []
        el["fillStyle"] = "solid"
        el["backgroundColor"] = "transparent"
        el["id"] = f"{el['type'][0]}{len(self.E)}"
        self.E.append(el)
        return el

    def rect(self, x, y, w, h, stroke, dashed=False, rough=1, sw=2):
        return self._add({"type": "rectangle", "x": x, "y": y, "width": w,
            "height": h, "strokeColor": stroke, "strokeWidth": sw,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": rough, "roundness": {"type": 3}})

    def ell(self, x, y, w, h, stroke):
        return self._add({"type": "ellipse", "x": x, "y": y, "width": w,
            "height": h, "strokeColor": stroke, "strokeWidth": 2,
            "strokeStyle": "solid", "roughness": 1, "roundness": {"type": 2}})

    def txt(self, x, y, s, size=13, color=INK, align="left", w=None, fam=1):
        lines = s.split("\n")
        k = 0.60 if fam == 3 else 0.56
        if w is None:
            w = int(max(len(l) for l in lines) * size * k) + 8
        return self._add({"type": "text", "x": x, "y": y, "width": w,
            "height": len(lines) * size * LH, "strokeColor": color,
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
            "roundness": None, "text": s, "fontSize": size, "fontFamily": fam,
            "textAlign": align, "verticalAlign": "top", "baseline": size,
            "containerId": None, "originalText": s, "lineHeight": LH})

    def arw(self, x1, y1, x2, y2, color="#5c5c5c", dashed=False):
        return self._add({"type": "arrow", "x": x1, "y": y1,
            "width": abs(x2-x1), "height": abs(y2-y1), "strokeColor": color,
            "strokeWidth": 2, "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1, "roundness": {"type": 2},
            "points": [[0, 0], [x2-x1, y2-y1]], "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow"})

    def line(self, x1, y1, x2, y2, color="#d4d4d8"):
        return self._add({"type": "line", "x": x1, "y": y1,
            "width": abs(x2-x1), "height": abs(y2-y1), "strokeColor": color,
            "strokeWidth": 1, "strokeStyle": "dashed", "roughness": 0,
            "roundness": None, "points": [[0, 0], [x2-x1, y2-y1]],
            "lastCommittedPoint": None, "startBinding": None,
            "endBinding": None, "startArrowhead": None, "endArrowhead": None})

    # ── figuras compuestas ────────────────────────────────
    def box(self, x, y, w, h, stroke, title, subs=(), tsize=14,
            ssize=10, dashed=False):
        """Caja con título centrado y hasta dos subtítulos."""
        self.rect(x, y, w, h, stroke, dashed=dashed)
        if subs is None:
            subs = ()
        elif isinstance(subs, str):
            subs = (subs,)
        th = len(title.split("\n")) * tsize * LH
        sh = sum(len(s.split("\n")) * ssize * LH + 2 for s in subs)
        top = y + (h - th - sh) / 2
        self.txt(x, top, title, tsize, stroke, "center", w)
        cy = top + th + 2
        for i, s in enumerate(subs):
            self.txt(x, cy, s, ssize, MUTE if i else BODY, "center", w)
            cy += len(s.split("\n")) * ssize * LH + 2

    def dbox(self, x, y, w, h, title, subs=(), stroke=DB):
        """Elipse para bases de datos y almacenes."""
        self.ell(x, y, w, h, stroke)
        if subs is None:
            subs = ()
        elif isinstance(subs, str):
            subs = (subs,)
        th = len(title.split("\n")) * 13 * LH
        sh = sum(len(s.split("\n")) * 10 * LH + 1 for s in subs)
        top = y + (h - th - sh) / 2
        self.txt(x, top, title, 13, stroke, "center", w)
        cy = top + th + 1
        for s in subs:
            self.txt(x, cy, s, 10, MUTE, "center", w)
            cy += len(s.split("\n")) * 10 * LH + 1

    def header(self, x, y, num, titulo, sub):
        self.txt(x, y, f"ITERACIÓN #{num}", 17, INK)
        self.txt(x, y + 24, titulo, 13, MUTE)
        return y + 56

    def zona(self, x, y, w, h, etiqueta):
        self.rect(x, y, w, h, ZONE, dashed=True, rough=0, sw=1)
        self.txt(x + 12, y + 6, etiqueta, 11, MUTE)

    def save(self, path):
        out = {"type": "excalidraw", "version": 2,
               "source": "https://excalidraw.com", "elements": self.E,
               "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
               "files": {}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False)
        return len(self.E)


def titulo(c, t, sub):
    c.txt(20, 20, t, 24, INK)
    c.txt(20, 56, sub, 13, MUTE)
    c.line(10, 88, 1200, 88)
