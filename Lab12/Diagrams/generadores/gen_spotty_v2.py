# -*- coding: utf-8 -*-
"""Spotty v2: misma arquitectura (control local + workers EC2 Spot), nodos cortos."""
import json, os

LH = 1.25
INK = "#1e1e1e"
E = []


def _base(el, eid):
    el.update({"id": eid, "angle": 0, "strokeWidth": 1.5, "strokeStyle": "solid",
               "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
               "seed": len(E) + 1, "version": 1, "versionNonce": len(E) + 1,
               "isDeleted": False, "boundElements": [], "updated": 1,
               "link": None, "locked": False})
    el.setdefault("strokeColor", INK)
    el.setdefault("backgroundColor", "transparent")
    el.setdefault("fillStyle", "solid")
    E.append(el)
    return el


def text(x, y, s, size=16, color=INK, align="left", eid=None, container=None, w=None):
    lines = s.split("\n")
    if w is None:
        w = max(len(l) for l in lines) * size * 0.6
    return _base({"type": "text", "x": x, "y": y, "width": w,
                  "height": len(lines) * size * LH, "text": s, "originalText": s,
                  "fontSize": size, "fontFamily": 1, "textAlign": align,
                  "verticalAlign": "middle", "containerId": container,
                  "autoResize": True, "lineHeight": LH, "roundness": None,
                  "strokeColor": color, "strokeWidth": 1},
                 eid or f"t{len(E)}")


def box(eid, x, y, w, h, label, stroke, fill, size=17, dashed=False):
    r = _base({"type": "rectangle", "x": x, "y": y, "width": w, "height": h,
               "roundness": {"type": 3}, "strokeColor": stroke,
               "backgroundColor": fill}, eid)
    if dashed:
        r["strokeStyle"] = "dashed"
    if label:
        lines = label.split("\n")
        th = len(lines) * size * LH
        text(x + 8, y + (h - th) / 2, label, size, INK, "center",
             f"{eid}-text", eid, w - 16)
        r["boundElements"].append({"type": "text", "id": f"{eid}-text"})
    return r


def zone(eid, x, y, w, h, label, stroke, fill, dashed=False):
    box(eid, x, y, w, h, None, stroke, fill, dashed=dashed)
    text(x + 20, y + 14, label, 19, stroke, eid=f"{eid}-label")


def _find(eid):
    return next(e for e in E if e["id"] == eid)


def arrow(eid, src, dst, pts, color=INK, label=None, lpos=None, dashed=False, both=False):
    x0, y0 = pts[0]
    a = _base({"type": "arrow", "x": x0, "y": y0,
               "width": max(p[0] for p in pts) - min(p[0] for p in pts),
               "height": max(p[1] for p in pts) - min(p[1] for p in pts),
               "points": [[px - x0, py - y0] for px, py in pts],
               "strokeColor": color, "roundness": None,
               "startBinding": {"elementId": src, "focus": 0, "gap": 1},
               "endBinding": {"elementId": dst, "focus": 0, "gap": 1},
               "startArrowhead": "arrow" if both else None,
               "endArrowhead": "arrow", "lastCommittedPoint": None}, eid)
    if dashed:
        a["strokeStyle"] = "dashed"
    for n in (src, dst):
        _find(n)["boundElements"].append({"type": "arrow", "id": eid})
    if label:
        text(lpos[0], lpos[1], label, 14, color)


# --- Títulos y zonas -------------------------------------------------------
text(40, 20, "SPOTTY — ARQUITECTURA", 28)
text(40, 62, "Control y datos en la universidad · AWS solo ejecuta workers EC2 Spot", 16, "#868e96")

zone("local", 40, 110, 990, 640, "UNIVERSIDAD (durable)", "#1971c2", "#f8fbff")
zone("aws", 1070, 110, 490, 640, "AWS — solo EC2 Spot", "#e67700", "#fff9f0", dashed=True)

# --- Local -----------------------------------------------------------------
box("student", 70, 175, 160, 70, "Estudiante\napp móvil", "#5f3dc4", "#f3f0ff")
box("teacher", 70, 300, 160, 70, "Profesor\ndesktop", "#5f3dc4", "#f3f0ff")
box("api", 310, 235, 160, 75, "API local", "#5f3dc4", "#e5dbff")
box("postgres", 550, 225, 190, 95, "PostgreSQL\ncola de jobs", "#1971c2", "#e7f5ff")
box("scheduler", 820, 225, 180, 95, "Scheduler\nprioridad por slack", "#2b8a3e", "#ebfbee")
box("nas", 550, 435, 190, 95, "NAS\nentregas · notas\ncheckpoints", "#0b7285", "#e3fafc")
box("registry", 820, 435, 180, 95, "Registry\nimagen por curso", "#0b7285", "#e3fafc")

box("n-lease", 70, 600, 280, 110,
    "Lease ≠ Lock\nSpot cae → lease vence\n→ QUEUED → otro worker", "#a61e4d", "#fff0f6", 15)
box("n-states", 375, 600, 300, 110,
    "QUEUED → RUNNING → DONE\nOOM / timeout → FAILED\n(máx. intentos, no reintenta)", "#a61e4d", "#fff0f6", 15)
box("n-fitness", 700, 600, 300, 110,
    "Fitness functions\nP99 por tipo de curso\nnotas < 48 h · cola vs capacidad", "#2b8a3e", "#ebfbee", 15)

# --- AWS -------------------------------------------------------------------
box("scaling", 1100, 160, 430, 55, "Escalado programado antes del deadline",
    "#e67700", "#fff4e6", 15)
box("pool", 1100, 245, 430, 120, None, "#e67700", "#fff4e6")
text(1115, 252, "EC2 Spot · multi-tipo / multi-AZ", 14, "#e67700")
box("w-cpu", 1120, 280, 185, 70, "Workers CPU", "#e67700", "#ffec99")
box("w-gpu", 1325, 280, 185, 70, "Workers GPU", "#e67700", "#ffec99")
box("sandbox", 1215, 425, 200, 80, "Sandbox\npor intento", "#c92a2a", "#fff5f5")
box("cache", 1215, 560, 200, 70, "Caché de imagen\nen disco", "#0b7285", "#e3fafc", 15)
text(1100, 660, "Sandbox: sin credenciales · red cerrada\nlímites CPU / RAM / GPU / tiempo", 14, "#c92a2a")

# --- Flechas ---------------------------------------------------------------
arrow("a-student", "student", "api", [(230, 210), (270, 210), (270, 255), (310, 255)], "#5f3dc4")
arrow("a-teacher", "teacher", "api", [(230, 335), (270, 335), (270, 290), (310, 290)], "#5f3dc4")
text(240, 150, "entrega / estado / notas", 14, "#5f3dc4")
arrow("a-api-db", "api", "postgres", [(470, 272), (550, 272)], "#1971c2", "job", (493, 250))
arrow("a-api-nas", "api", "nas", [(390, 310), (390, 482), (550, 482)], "#0b7285", "archivo", (400, 455))
arrow("a-db-sched", "postgres", "scheduler", [(740, 272), (820, 272)], "#2b8a3e", "claim", (755, 250), both=True)
arrow("a-sched-scaling", "scheduler", "scaling", [(910, 225), (910, 187), (1100, 187)], "#e67700",
      "deadlines", (925, 162), dashed=True)
arrow("a-pool-sched", "pool", "scheduler", [(1100, 305), (1000, 305)], "#7048e8",
      "pull + heartbeat\n(mTLS)", (1005, 315), dashed=True)
arrow("a-pool-sandbox", "pool", "sandbox", [(1315, 365), (1315, 425)], "#c92a2a", "ejecuta", (1325, 385))
arrow("a-pool-nas", "pool", "nas", [(1180, 365), (1180, 395), (645, 395), (645, 435)], "#0b7285",
      "checkpoint / resultado", (700, 372), dashed=True)
arrow("a-reg-cache", "registry", "cache", [(1000, 500), (1060, 500), (1060, 595), (1215, 595)], "#0b7285",
      "pre-carga", (1090, 570), dashed=True)

# --- Explicación -----------------------------------------------------------
zone("explain", 1600, 110, 560, 640, "¿CÓMO FUNCIONA?", "#495057", "#f8f9fa")
text(1620, 155, "\n".join([
    "1. Entrega",
    "   El alumno sube su código desde la app. La API guarda",
    "   el archivo en el NAS y crea un job QUEUED en PostgreSQL.",
    "",
    "2. Prioridad",
    "   El scheduler ordena por recurso (CPU/GPU), cuota por",
    "   curso y menor slack = deadline − ahora − restante.",
    "   Los jobs de GPU pueden esperar: hay 2 días para notas.",
    "",
    "3. Capacidad",
    "   Antes de cada deadline se encienden workers Spot de",
    "   varios tipos y AZ, y precargan la imagen del curso",
    "   (3–5 GB) para no bajarla en el pico de 30 minutos.",
    "",
    "4. Ejecución",
    "   El worker hace pull de un job con lease y heartbeat.",
    "   Corre el código en un sandbox aislado con límites",
    "   de CPU / RAM / GPU / tiempo: código no confiable.",
    "",
    "5. Fallas",
    "   Spot reclamada (aviso 2 min) → checkpoint, el lease",
    "   vence y otro worker retoma. OOM o timeout del alumno",
    "   → FAILED con nota, no se reintenta.",
    "",
    "6. Resultado",
    "   El resultado va al NAS; solo un intento gana (CAS).",
    "   Alumno y profesor consultan el estado vía API.",
    "",
    "Atributos: reliability (lease + checkpoint),",
    "scalability (escalado por deadline), caching (imágenes),",
    "availability (datos durables fuera de Spot).",
]), 15)

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": E,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}
out = os.path.join(os.path.dirname(__file__), "..", "spotty-arquitectura-v2.excalidraw")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
print("ok", os.path.abspath(out), len(E))
