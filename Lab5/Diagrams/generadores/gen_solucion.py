# -*- coding: utf-8 -*-
"""Diagrama de solucion de Genius, en el estilo de cajas del profesor."""
import json, os

TS = 1725494400000
LH = 1.25
INK = "#1e1e1e"
GREY = "#868e96"

ACTOR_A = "#a5d8ff"   # ingeniero de soporte
ACTOR_B = "#b2f2bb"   # ingeniero de desarrollo / data science
ACTOR_C = "#ffec99"   # incident manager / cliente
SERV = "#ffc9c9"      # servicios
LOGIC = "#d0bfff"     # auth, orquestador, LLM
DB = "#99e9f2"        # bases de datos
EXT = "#b2f2bb"       # externos
DASH = "#d8f5a2"      # metricas

FS = 16
LFS = 13

E = []


def _base(el, t):
    el.update({"seed": 1, "updated": TS, "link": None, "locked": False,
               "angle": 0, "opacity": 100, "groupIds": [], "boundElements": [],
               "strokeColor": INK, "strokeWidth": 1.5, "strokeStyle": "solid",
               "roughness": 1, "id": f"{t}{len(E)}"})
    E.append(el)
    return el


def text(x, y, s, size=FS, color=INK, align="center", w=None):
    lines = s.split("\n")
    if w is None:
        w = int(max(len(l) for l in lines) * size * 0.58) + 10
    el = {"type": "text", "x": x, "y": y, "width": w,
          "height": len(lines) * size * LH, "text": s, "fontSize": size,
          "fontFamily": 1, "textAlign": align, "verticalAlign": "top",
          "baseline": size, "containerId": None, "originalText": s,
          "lineHeight": LH, "roundness": None, "fillStyle": "solid",
          "backgroundColor": "transparent"}
    _base(el, "t")
    el["strokeColor"] = color
    el["strokeWidth"] = 1
    return el


class Node:
    def __init__(self, x, y, w, h, shape):
        self.x, self.y, self.w, self.h, self.shape = x, y, w, h, shape

    @property
    def cx(self): return self.x + self.w / 2

    @property
    def cy(self): return self.y + self.h / 2

    def left(self): return (self.x, self.cy)
    def right(self): return (self.x + self.w, self.cy)
    def top(self): return (self.cx, self.y)
    def bottom(self): return (self.cx, self.y + self.h)


def box(x, y, label, fill, w=160, shape="rect"):
    lines = label.split("\n")
    h = max(84, len(lines) * FS * LH + 30)
    el = {"type": "rectangle" if shape == "rect" else "ellipse", "x": x, "y": y,
          "width": w, "height": h, "roundness": {"type": 3 if shape == "rect" else 2},
          "fillStyle": "solid", "backgroundColor": fill}
    _base(el, "r")
    text(x, y + (h - len(lines) * FS * LH) / 2, label, FS, INK, "center", w)
    return Node(x, y, w, h, shape)


def ell(x, y, label, fill=DB, w=170):
    lines = label.split("\n")
    h = max(100, len(lines) * FS * LH + 46)
    el = {"type": "ellipse", "x": x, "y": y, "width": w, "height": h,
          "roundness": {"type": 2}, "fillStyle": "solid",
          "backgroundColor": fill}
    _base(el, "e")
    text(x, y + (h - len(lines) * FS * LH) / 2, label, FS, INK, "center", w)
    return Node(x, y, w, h, "ell")


def _anchor(a, b):
    dx = b.cx - a.cx
    dy = b.cy - a.cy
    if abs(dx) > abs(dy) * 1.1:
        return (a.right(), b.left()) if dx > 0 else (a.left(), b.right())
    return (a.bottom(), b.top()) if dy > 0 else (a.top(), b.bottom())


def arrow(a, b, label=None, pts=None, lpos=None, start=None, end=None):
    if pts is None:
        s, e = _anchor(a, b)
        if start: s = start
        if end: e = end
        path = [s, e]
    else:
        path = [start] + pts + [end]
    x0, y0 = path[0]
    rel = [[p[0] - x0, p[1] - y0] for p in path]
    xs = [p[0] for p in path]; ys = [p[1] for p in path]
    el = {"type": "arrow", "x": x0, "y": y0, "width": max(xs) - min(xs),
          "height": max(ys) - min(ys), "roundness": {"type": 2},
          "points": rel, "lastCommittedPoint": None, "startBinding": None,
          "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow",
          "fillStyle": "solid", "backgroundColor": "transparent"}
    _base(el, "a")
    el["strokeColor"] = GREY
    el["strokeWidth"] = 1.5
    if label:
        if lpos is None:
            mx = (path[0][0] + path[1][0]) / 2
            my = (path[0][1] + path[1][1]) / 2
            lpos = (mx, my - 22)
        t = text(0, 0, label, LFS, INK, "center")
        t["x"] = lpos[0] - t["width"] / 2
        t["y"] = lpos[1]
    return el


X = [40 + 220 * i for i in range(12)]
R1, R1b = 130, 275
R2, R2b = 500, 645
R3 = 825
R4, R4b = 975, 1115
C1, C2, C3, C4, C5 = 400, 445, 770, 945, 1240

text(40, 24, "Genius — Diagrama de solución", 24, INK, "left")

# ── carril 1: ingeniero de soporte ───────────────────────
sop = box(X[0], R1, "Ingeniero\nde soporte", ACTOR_A)
auth1 = box(X[1], R1, "Auth y rol\nservice", LOGIC)
cola = box(X[1], R1b, "Cola: sale primero\nel cliente, después\ningeniería\nservice", SERV)
preg = box(X[2], R1, "Interpretación\nde la pregunta\nservice", SERV)
cache = box(X[3], R1, "Caché de\npreguntas\nfrecuentes\nservice", SERV)
match = box(X[4], R1, "Match\ndeterminístico\nservice", SERV)
resp = box(X[5], R1, "Respuesta con\nhora del dato\nservice", SERV)
evid = box(X[6], R1, "Evidencia de la\nincidencia\nservice", SERV)
score = box(X[7], R1, "Score y motivo\nde la respuesta\nservice", SERV)
escal = box(X[8], R1, "Escalamiento\npor tipo\nservice", SERV)
notif = box(X[9], R1, "Notificación al\ningeniero\nservice", SERV)
degr = box(X[3], R1b, "Modo degradado\nservice", SERV)
estado = box(X[4], R1b, "Estado de\nincidencia\nservice", SERV)
bd1 = ell(X[5], R1b, "BD1\nestado\n(cada 5 min)")
abst = box(X[6], R1b, "Abstención\nservice", SERV)

arrow(sop, auth1)
arrow(auth1, cola, "pico de demanda")
arrow(cola, preg, "pregunta", lpos=(X[1] + 250, R1 + 104))
arrow(preg, cache)
arrow(cache, match, "hit")
arrow(match, resp)
arrow(resp, evid)
arrow(evid, score)
arrow(score, escal, "excede a\nsoporte", lpos=(X[7] + 190, R1 - 4))
arrow(escal, notif)
arrow(cache, estado, "miss", lpos=(X[3] + 200, R1 + 120))
arrow(preg, degr, "LLM caído", lpos=(X[2] + 195, R1 + 120))
arrow(degr, estado, "solo BD1")
arrow(estado, bd1, "lee estado")
arrow(bd1, resp, "estado + hora", lpos=(X[5] + 255, R1b - 18))
arrow(bd1, abst, "sin dato")

# ── carril 2: ingeniero de desarrollo ────────────────────
dev = box(X[0], R2, "Ingeniero de\ndesarrollo", ACTOR_B)
auth2 = box(X[1], R2, "Auth y rol\nservice", LOGIC)
inc = box(X[2], R2, "Incidencia\nescalada\nservice", SERV)
orq = box(X[3], R2, "Orquestador de\nherramientas\nservice", LOGIC)
cons = box(X[4], R2, "Consulta de\nsolo lectura\nservice", SERV)
simil = box(X[5], R2, "Incidencias\nsimilares\nservice", SERV)
impac = box(X[6], R2, "Vista previa\nde impacto\nservice", SERV)
perm = box(X[7], R2, "Permisos del\ningeniero\nservice", SERV)
ejec = box(X[8], R2, "Ejecución\nservice", SERV)
audit = box(X[9], R2, "Auditoría\nservice", SERV)
undo = box(X[10], R2, "Deshacer\nacción\nservice", SERV)
llm = box(X[2], R2b, "LLM", LOGIC)
e2e = box(X[5], R2b, "Pruebas E2E\nservice", SERV)
entorno = ell(X[6], R2b, "Entorno\nde pruebas", EXT)
bloq = box(X[7], R2b, "Bloqueo de\nescritura\nservice", SERV)
cierre = box(X[9], R2b, "Cierre de\nincidencia\nservice", SERV)

arrow(dev, auth2)
arrow(auth2, cola, start=(X[1] + 80, R2), pts=[], end=(X[1] + 80, R1b + 110))
arrow(cola, inc, "trabajo\nescalado", start=(X[1] + 160, R1b + 55),
      pts=[], end=(X[2] + 40, R2), lpos=(X[2] + 30, R2 - 110))
arrow(inc, orq)
arrow(orq, cons, "llama por MCP")
arrow(cons, simil)
arrow(simil, impac)
arrow(impac, perm)
arrow(perm, ejec, "solo lectura")
arrow(ejec, audit)
arrow(audit, undo, "si fue error")
arrow(llm, orq, "propone")
arrow(orq, e2e, "prueba", start=(X[3] + 140, R2 + 90),
      pts=[(X[5] + 80, R2b - 35)], end=(X[5] + 80, R2b),
      lpos=(X[4] + 150, R2b - 70))
arrow(e2e, entorno, "nunca\nproducción", lpos=(X[5] + 190, R2b + 96))
arrow(perm, bloq, "escribe")
arrow(ejec, cierre, "resuelto", start=(X[8] + 160, R2 + 70),
      pts=[], end=(X[9], R2b + 45), lpos=(X[8] + 215, R2b - 30))

# ── carril 3: incident manager ───────────────────────────
im = box(X[0], R3, "Incident\nManager", ACTOR_C)
kill = box(X[3], R3, "Kill switch de\nacciones\nservice", SERV)
aprob = box(X[8], R3, "Aprobación de\nla acción\nservice", SERV)

arrow(im, kill)
arrow(kill, orq, "apaga acciones,\nno consultas",
      start=(X[3] + 80, R3), pts=[], end=(X[3] + 80, R2 + 90),
      lpos=(X[3] + 80, R2b + 30))
arrow(im, aprob, "aprueba o rechaza", start=(X[0] + 80, R3 + 84),
      pts=[(X[0] + 80, C4), (X[8] + 80, C4)], end=(X[8] + 80, R3 + 90),
      lpos=(X[4] + 60, C4 - 30))
arrow(bloq, aprob, "requiere aprobación", lpos=(X[7] + 230, R3 - 40))
arrow(aprob, ejec, "aprobado", start=(X[8] + 80, R3), pts=[],
      end=(X[8] + 80, R2 + 84), lpos=(X[8] + 145, R2b + 20))

# ── carril 4: data science y cliente ─────────────────────
cli = box(X[0], R4, "Cliente\n(empresa)", ACTOR_C)
ds = box(X[0], R4b, "Data\nScience", ACTOR_B)
inge = box(X[1], R4, "Ingesta de data\ndel cliente\nservice", SERV)
bd3 = ell(X[2], R4, "BD3\ningesta\n+ scores")
cura = box(X[3], R4, "Curación de\nconocimiento\nservice", SERV)
bd2 = ell(X[4], R4, "BD2\nhistórico,\nqueries, backup")
enriq = box(X[5], R4, "Enriquecimiento\ndel LLM\nservice", SERV)
evalset = box(X[6], R4, "Eval set de\nrespuestas\nconocidas\nservice", SERV)
metr = box(X[3], R4b, "Métricas y\ndashboard\nservice", DASH)

arrow(cli, inge)
arrow(ds, inge)
arrow(inge, bd3)
arrow(bd3, cura)
arrow(cura, bd2, "conocimiento\nválido", lpos=(X[3] + 190, R4 + 6))
arrow(bd2, enriq)
arrow(enriq, evalset)
arrow(metr, bd3)
arrow(metr, bd2)

# ── enlaces largos entre carriles ────────────────────────
# notificacion -> ingeniero de desarrollo
arrow(notif, dev, "escalada, mantiene\nprioridad de cliente", start=(X[9] + 80, R1 + 90),
      pts=[(X[9] + 80, C1), (X[0] + 80, C1)], end=(X[0] + 80, R2),
      lpos=(X[5] + 340, C1 - 28))
# cierre -> BD1
arrow(cierre, bd1, "actualiza estado", start=(X[9] + 160, R2b + 45),
      pts=[(X[10] + 190, R2b + 45), (X[10] + 190, C2), (X[5] + 85, C2)],
      end=(X[5] + 85, R1b + 106), lpos=(X[7] + 130, C2 - 28))
# score -> BD3
arrow(score, bd3, "guarda score", start=(X[7] + 160, R1 + 65),
      pts=[(X[7] + 190, R1 + 65), (X[7] + 190, C5), (X[2] + 85, C5)],
      end=(X[2] + 85, R4 + 106), lpos=(X[4] + 60, C5 + 8))
# consulta de solo lectura -> BD2
arrow(cons, bd2, "queries", start=(X[4] + 80, R2 + 90), pts=[],
      end=(X[4] + 80, R4), lpos=(X[4] + 140, R3 + 40))
# BD1 -> BD2 (backup anti SPOF)
arrow(bd1, bd2, "backup\n(anti SPOF)", start=(X[5], R1b + 53),
      pts=[(X[5] - 30, R1b + 53), (X[5] - 30, R4 + 53)],
      end=(X[4] + 170, R4 + 53), lpos=(X[4] + 250, R2b + 150))
# eval set -> LLM
arrow(evalset, llm, "publica versión", start=(X[6] + 80, R4),
      pts=[(X[6] + 80, C3), (X[2] + 80, C3)], end=(X[2] + 80, R2b + 84),
      lpos=(X[4] + 60, C3 - 28))
# LLM -> interpretacion de la pregunta
arrow(llm, preg, "interpreta,\nno responde", start=(X[2], R2b + 42),
      pts=[(X[1] + 190, R2b + 42), (X[1] + 190, R1 + 70)],
      end=(X[2], R1 + 70), lpos=(X[1] + 100, R2b - 45))
# LLM -> match deterministico
arrow(llm, match, "respuestas\ncandidatas", start=(X[2] + 160, R2b + 42),
      pts=[(X[3] + 200, R2b + 42), (X[3] + 200, R1 + 55)],
      end=(X[4], R1 + 55), lpos=(X[3] + 275, R1b + 135))

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "genius-solucion.excalidraw")
json.dump({"type": "excalidraw", "version": 2,
           "source": "https://excalidraw.com", "elements": E,
           "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
           "files": {}}, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(out, len(E))
