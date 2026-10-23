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


# ── rejilla top-down ─────────────────────────────────────
C = [60 + 220 * i for i in range(8)]          # columnas
Y = [140 + 150 * i for i in range(10)]         # filas de servicios
YD1, YD2 = 1660, 1810                          # capa de datos y modelo
GUT = {i: C[i] + 195 for i in range(7)}        # canaleta a la derecha de cada columna
MARGEN_I, MARGEN_D = 25, 1800


def dash(el):
    el["strokeStyle"] = "dashed"
    return el


text(60, 30, "Genius — Diagrama de solución (top-down)", 24, INK, "left")
text(60, 66, "usuarios arriba · servicios en el medio · datos y modelo abajo", 13,
     GREY, "left")

# ── fila 0: usuarios ─────────────────────────────────────
sop = box(C[0], Y[0], "Ingeniero\nde soporte", ACTOR_A)
dev = box(C[3], Y[0], "Ingeniero de\ndesarrollo", ACTOR_B)
im = box(C[5], Y[0], "Incident\nManager", ACTOR_C)
ds = box(C[6], Y[0], "Data\nScience", ACTOR_B)
cli = box(C[1], Y[0], "Cliente\n(empresa)", ACTOR_C)
sist = box(C[7], Y[0], "Sistemas del\ncliente", ACTOR_C)

# ── fila 1: acceso e ingesta ─────────────────────────────
auth1 = box(C[0], Y[1], "Auth y rol\nservice", LOGIC)
auth2 = box(C[3], Y[1], "Auth y rol\nservice", LOGIC)
auth3 = box(C[1], Y[1], "Auth y rol\n(solo sus\nincidencias)\nservice", LOGIC)
inge = box(C[6], Y[1], "Ingesta de data\ndel cliente\nservice", SERV)

# ── fila 2: admisión ─────────────────────────────────────
cola = box(390, Y[2], "Cola por prioridad\ncliente > ingeniería\nservice", SERV)
cura = box(C[6], Y[2], "Curación de\nconocimiento\nservice", SERV)
metr = box(C[7], Y[2], "Métricas y\ndashboard\nservice", DASH)

# ── fila 3: entrada de cada carril ───────────────────────
interp = box(C[0], Y[3], "Interpretación\nde la pregunta\nservice", SERV)
incid = box(C[3], Y[3], "Incidencia\nescalada\nservice", SERV)
enriq = box(C[6], Y[3], "Enriquecimiento\ndel LLM\nservice", SERV)

# ── fila 4 ───────────────────────────────────────────────
cache = box(C[0], Y[4], "Caché de\npreguntas\nfrecuentes\nservice", SERV)
degr = box(C[1], Y[4], "Modo degradado\nservice", SERV)
orq = box(C[3], Y[4], "Orquestador de\nherramientas\nservice", LOGIC)
kill = box(C[4], Y[4], "Kill switch de\nacciones\nservice", SERV)
evalset = box(C[6], Y[4], "Eval set de\nrespuestas\nconocidas\nservice", SERV)
aprcon = box(C[6], Y[5], "Aprobación de\ncambios al\nconocimiento\nservice", SERV)

# ── fila 5 ───────────────────────────────────────────────
match = box(C[0], Y[5], "Match\ndeterminístico\nservice", SERV)
estado = box(C[1], Y[5], "Estado de\nincidencia\nservice", SERV)
cons = box(C[3], Y[5], "Consulta de\nsolo lectura\nservice", SERV)
simil = box(C[4], Y[5], "Incidencias\nsimilares\nservice", SERV)

# ── fila 6 ───────────────────────────────────────────────
resp = box(C[0], Y[6], "Respuesta con\nhora del dato\nservice", SERV)
abst = box(C[1], Y[6], "Abstención\nservice", SERV)
impac = box(C[3], Y[6], "Vista previa\nde impacto\nservice", SERV)

# ── fila 7 ───────────────────────────────────────────────
evid = box(C[0], Y[7], "Evidencia de la\nincidencia\nservice", SERV)
perm = box(C[3], Y[7], "Permisos del\ningeniero\nservice", SERV)
bloq = box(C[4], Y[7], "Bloqueo de\nescritura\nservice", SERV)
aprob = box(C[5], Y[7], "Aprobación de\nla acción\nservice", SERV)

# ── fila 8 ───────────────────────────────────────────────
score = box(C[0], Y[8], "Score y motivo\nde la respuesta\nservice", SERV)
borra = box(C[5], Y[8], "Borrado de\nincidencia\nservice", SERV)
ejec = box(C[3], Y[8], "Ejecución\nservice", SERV)
audit = box(C[4], Y[8], "Auditoría\nservice", SERV)

# ── fila 9 ───────────────────────────────────────────────
escal = box(C[0], Y[9], "Escalamiento\npor tipo\nservice", SERV)
notif = box(C[1], Y[9], "Notificación al\ningeniero\nservice", SERV)
cierre = box(C[3], Y[9], "Cierre de\nincidencia\nservice", SERV)
e2e = box(C[4], Y[9], "Pruebas E2E\nservice", SERV)
undo = box(C[5], Y[9], "Deshacer\nacción\nservice", SERV)

# ── capa de datos y modelo ───────────────────────────────
bd1 = ell(C[1], YD1, "BD1\nestado\n(cada 5 min)")
bd2 = ell(C[5], YD1, "BD2\nhistórico,\nqueries, backup")
bd3 = ell(C[6], YD1, "BD3\ningesta\n+ scores")
llm = box(C[2], YD2, "LLM", LOGIC)
entorno = ell(C[4], YD2, "Entorno\nde pruebas", EXT)

# ── carril del ingeniero de soporte ──────────────────────
arrow(sop, auth1)
arrow(auth1, cola, "pico de demanda", start=(C[0] + 85, Y[1] + 84),
      pts=[(C[0] + 85, Y[1] + 125), (430, Y[1] + 125)], end=(430, Y[2]),
      lpos=(170, Y[1] + 130))
arrow(cola, interp, "pregunta", lpos=(250, Y[3] - 40))
arrow(interp, cache)
arrow(interp, degr, "LLM caído", lpos=(C[1] + 40, Y[4] - 42))
arrow(degr, estado, "solo BD1")
arrow(cache, match, "hit")
arrow(cache, estado, "miss", lpos=(C[1] - 20, Y[5] - 40))
arrow(match, resp)
arrow(estado, resp, "estado + hora", lpos=(C[1] - 20, Y[6] - 40))
arrow(estado, abst, "sin dato")
arrow(resp, evid)
arrow(evid, score)
arrow(score, escal, "excede a soporte")
arrow(escal, notif)

# ── carril del ingeniero de desarrollo ───────────────────
arrow(dev, auth2)
arrow(auth2, cola, "pico de demanda", lpos=(C[3] - 30, Y[1] + 120))
arrow(cola, incid, "trabajo escalado", lpos=(C[3] - 120, Y[3] - 40))
arrow(incid, orq)
arrow(orq, cons, "llama por MCP")
arrow(orq, simil, lpos=None)
arrow(cons, impac)
arrow(simil, impac)
arrow(impac, perm)
arrow(perm, ejec, "solo lectura")
arrow(perm, bloq, "cambia o borra")
arrow(bloq, aprob, "requiere\naprobación", lpos=(1135, Y[7] - 42))
arrow(aprob, ejec, "aprobado", lpos=(C[3] + 245, Y[8] - 36))
arrow(ejec, audit, "registra")
arrow(ejec, cierre)
arrow(ejec, e2e, "valida el fix", lpos=(C[4] + 40, Y[9] - 40))
arrow(audit, undo, "si fue error")

# ── incident manager ─────────────────────────────────────
arrow(im, kill, "apaga acciones,\nno consultas", start=(C[5], Y[0] + 42),
      pts=[(GUT[4], Y[0] + 42), (GUT[4], Y[4] - 25), (C[4] + 85, Y[4] - 25)],
      end=(C[4] + 85, Y[4]), lpos=(C[4] + 90, Y[2] + 20))
arrow(kill, orq)
arrow(im, aprob, "aprueba o rechaza", start=(C[5] + 85, Y[0] + 84), pts=[],
      end=(C[5] + 85, Y[7]), lpos=(1175, Y[3] + 110))

# ── data science y cliente ───────────────────────────────
arrow(ds, inge)
arrow(cli, auth3)
arrow(auth3, cola, "sus propias\nincidencias", lpos=(C[1] + 235, Y[1] + 118))
arrow(sist, inge, "su data", lpos=(C[6] + 245, Y[0] + 120))
arrow(inge, cura)
arrow(cura, enriq)
arrow(enriq, evalset)
arrow(evalset, aprcon, "pasa el eval")
arrow(im, aprcon, "aprueba el cambio", start=(C[5] + 130, Y[0] + 84),
      pts=[(C[5] + 130, Y[5] + 45)], end=(C[6], Y[5] + 45),
      lpos=(C[5] + 150, Y[4] + 95))
arrow(aprob, borra, "borrado aprobado", lpos=(C[5] + 5, Y[8] - 42))
arrow(borra, audit, "queda registrado", lpos=(C[5] + 90, Y[8] + 112))
arrow(borra, undo)

# ── servicios que usan la capa de datos ──────────────────
arrow(estado, bd1, "lee estado", start=(C[1] + 170, Y[5] + 45),
      pts=[(GUT[1], Y[5] + 45), (GUT[1], YD1 + 45)], end=(C[1] + 170, YD1 + 45),
      lpos=(540, Y[6] + 30))
arrow(cierre, bd1, "actualiza estado", start=(C[3] + 85, Y[9] + 90),
      pts=[(C[3] + 85, YD1 - 40), (C[1] + 85, YD1 - 40)], end=(C[1] + 85, YD1),
      lpos=(620, YD1 - 30))
arrow(cons, bd2, "queries", start=(C[3] + 170, Y[5] + 45),
      pts=[(GUT[3], Y[5] + 45), (GUT[3], YD1 + 45)], end=(C[5], YD1 + 45),
      lpos=(1050, YD1 + 12))
arrow(score, bd3, "guarda score", start=(C[0] + 85, Y[8] + 90),
      pts=[(C[0] + 85, YD1 - 60), (C[6] + 85, YD1 - 60)], end=(C[6] + 85, YD1),
      lpos=(620, YD1 - 84))
arrow(inge, bd3, "data del cliente", start=(C[6] + 170, Y[1] + 45),
      pts=[(GUT[6], Y[1] + 45), (GUT[6], YD1 + 45)], end=(C[6] + 170, YD1 + 45),
      lpos=(GUT[6] + 75, Y[4] + 20))
arrow(cura, bd3, "qué pasa a BD2", start=(C[6], Y[2] + 45),
      pts=[(C[6] - 25, Y[2] + 45), (C[6] - 25, YD1 + 45)], end=(C[6], YD1 + 45),
      lpos=(C[6] + 80, Y[6] + 10))
arrow(metr, bd3, "lee las tres", start=(C[7] + 85, Y[2] + 90),
      pts=[(C[7] + 85, YD1 + 85), (C[6] + 170, YD1 + 85)],
      end=(C[6] + 170, YD1 + 75), lpos=(C[7] + 140, Y[6] + 20))
arrow(e2e, entorno, "nunca producción", start=(C[4] + 85, Y[9] + 84), pts=[],
      end=(C[4] + 85, YD2), lpos=(1130, YD1 + 118))

# ── servicios que usan el LLM ────────────────────────────
arrow(interp, llm, "interpreta,\nno responde", start=(C[0], Y[3] + 45),
      pts=[(MARGEN_I, Y[3] + 45), (MARGEN_I, YD2 + 42)], end=(C[2], YD2 + 42),
      lpos=(300, YD2 + 46))
arrow(match, llm, "respuestas\ncandidatas", start=(C[0] + 170, Y[5] + 45),
      pts=[(GUT[0], Y[5] + 45), (GUT[0], YD2 + 20), (C[2] + 40, YD2 + 20)],
      end=(C[2] + 40, YD2), lpos=(GUT[0] + 80, Y[7] + 20))
arrow(orq, llm, "propone", start=(C[3], Y[4] + 45),
      pts=[(C[2] + 85, Y[4] + 45)], end=(C[2] + 85, YD2),
      lpos=(640, Y[7] + 40))
arrow(aprcon, llm, "publica versión", start=(C[6] + 170, Y[5] + 45),
      pts=[(MARGEN_D, Y[5] + 45), (MARGEN_D, YD2 + 130), (C[2] + 85, YD2 + 130)],
      end=(C[2] + 85, YD2 + 84), lpos=(C[4] + 60, YD2 + 138))

# ── dentro de la capa de datos ───────────────────────────
arrow(bd1, bd2, "backup (anti SPOF)")
arrow(bd3, bd2, "curado")
arrow(bd2, llm, "contexto", start=(C[5] + 85, YD1 + 106),
      pts=[(C[5] + 85, YD2 - 25), (C[2] + 130, YD2 - 25)], end=(C[2] + 130, YD2),
      lpos=(C[4] + 30, YD2 - 50))

# ── realimentación: lo único que sube ────────────────────
dash(arrow(notif, incid, "escalada", start=(C[1] + 170, Y[9] + 45),
           pts=[(GUT[2], Y[9] + 45), (GUT[2], Y[3] - 30), (C[3] + 130, Y[3] - 30)],
           end=(C[3] + 130, Y[3]), lpos=(620, Y[5] + 30)))

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "genius-solucion-topdown.excalidraw")
json.dump({"type": "excalidraw", "version": 2,
           "source": "https://excalidraw.com", "elements": E,
           "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
           "files": {}}, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(out, len(E))
