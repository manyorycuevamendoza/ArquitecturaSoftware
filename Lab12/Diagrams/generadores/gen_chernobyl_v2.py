# -*- coding: utf-8 -*-
"""Save Chernobyl v2: misma arquitectura, más nodos y menos texto."""
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


def box(eid, x, y, w, h, label, stroke, fill, size=16, dashed=False):
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
    text(x + 20, y + 12, label, 18, stroke, eid=f"{eid}-label")


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
        text(lpos[0], lpos[1], label, 13, color)



GREEN, BLUE, RED, ORANGE, PURPLE, PINK = "#2b8a3e", "#1971c2", "#c92a2a", "#e67700", "#5f3dc4", "#a61e4d"

# --- Títulos y zonas -------------------------------------------------------
text(40, 20, "SAVE CHERNOBYL — ARQUITECTURA v2", 28)
text(40, 62, "— flujo principal    - - - respaldo / asíncrono", 15, "#868e96")

zone("edge", 40, 140, 520, 360, "BORDE", GREEN, "#f4fcf5")
zone("pilot", 220, 560, 370, 150, "PILOTO LIB NUEVA", ORANGE, "#fff9f0", dashed=True)
zone("core", 580, 140, 580, 375, "BUS + CONTROL HA", BLUE, "#f8fbff")
zone("mig", 1180, 140, 790, 200, "MIGRACIÓN", "#2f9e44", "#f6fff7")
zone("leg", 1570, 350, 400, 220, "LEGACY", RED, "#fff8f8", dashed=True)
zone("ops", 1570, 600, 580, 250, "AUDITORÍA", PURPLE, "#f9f7ff")

# --- Borde -----------------------------------------------------------------
for i, y in enumerate((180, 300, 420)):
    n = i + 1
    box(f"s{n}", 60, y, 140, 60, f"Sensores R{n}", GREEN, "#ebfbee")
    box(f"lc{n}", 240, y, 150, 60, f"Ctrl local R{n}", GREEN, "#d3f9d8")
    if n == 3:
        box(f"buf{n}", 410, y, 110, 60, "Sidecar R3\nbuffer\nlib NUEVA", ORANGE, "#ffec99", 13, dashed=True)
    else:
        box(f"buf{n}", 410, y, 110, 60, f"Sidecar R{n}\nbuffer\nlib actual", GREEN, "#ebfbee", 13)
    arrow(f"a-s{n}", f"s{n}", f"lc{n}", [(200, y + 30), (240, y + 30)], GREEN)
    arrow(f"a-b{n}", f"lc{n}", f"buf{n}", [(390, y + 30), (410, y + 30)], GREEN)

# --- Piloto ----------------------------------------------------------------
# El ctrl local no cambia: publica a su sidecar; el sidecar elige la librería por flag
box("pflag", 240, 600, 140, 55, "Flag lib_nueva\nsolo R3", ORANGE, "#fff4e6", 14, dashed=True)
box("pmet", 430, 600, 140, 55, "Métricas p99\nactual vs nueva", ORANGE, "#fff4e6", 14)
arrow("a-pflag", "pflag", "buf3", [(310, 600), (310, 540), (450, 540), (450, 480)], ORANGE, dashed=True)
arrow("a-pmet", "buf3", "pmet", [(500, 480), (500, 600)], ORANGE, dashed=True)
text(235, 665, "rollback: apagar flag → vuelve a lib actual", 13, ORANGE)

# --- Control HA ------------------------------------------------------------
# Bus A: un carril (cola) por reactor y por tipo de mensaje, no una cola única
box("busa", 595, 175, 240, 250, None, BLUE, "#e7f5ff")
text(610, 180, "Bus A (activo)", 15, BLUE)
for i in range(3):
    n = i + 1
    box(f"qa{n}", 605, 205 + i * 35, 220, 28, f"Alertas R{n}", RED, "#ffe3e3", 13)
    box(f"qt{n}", 605, 315 + i * 35, 220, 28, f"Telemetría R{n}", BLUE, "#d0ebff", 13)
box("busb", 595, 445, 240, 50, "Bus B (réplica)", BLUE, "#e7f5ff", 15, dashed=True)
box("vto", 850, 300, 125, 45, "Timeout\nsensor caído", BLUE, "#e7f5ff", 13)
box("vanom", 850, 355, 125, 45, "Detector de\nanomalías", BLUE, "#e7f5ff", 13)
box("vote", 850, 410, 125, 45, "Votación\n(mediana)", BLUE, "#d0ebff", 13)
arrow("a-vto-anom", "vto", "vanom", [(912, 345), (912, 355)], BLUE)
arrow("a-anom-vote", "vanom", "vote", [(912, 400), (912, 410)], BLUE)
text(850, 462, "sensor excluido\n+ aviso mantenimiento", 12, PINK)
box("mca", 1005, 200, 130, 60, "MC A\nactivo", BLUE, "#d0ebff", 15)
box("mcb", 1005, 340, 130, 60, "MC B\npasivo", BLUE, "#e7f5ff", 15, dashed=True)

# El ctrl local clasifica: lo que supera el umbral va al carril de alertas
for n, y in ((1, 210), (2, 330), (3, 450)):
    ja, jt = 532 + n * 8, 560 + n * 8
    arrow(f"a-buf{n}-qa", f"buf{n}", f"qa{n}",
          [(520, y), (ja, y), (ja, 219 + (n - 1) * 35), (605, 219 + (n - 1) * 35)], RED)
    arrow(f"a-buf{n}-qt", f"buf{n}", f"qt{n}",
          [(520, y + 10), (jt, y + 10), (jt, 329 + (n - 1) * 35), (605, 329 + (n - 1) * 35)], BLUE)
text(395, 150, "ctrl local clasifica: alerta | telemetría", 13, RED)
arrow("a-bus-rep", "busa", "busb", [(715, 425), (715, 445)], BLUE, dashed=True, both=True)
arrow("a-qa-mca", "busa", "mca", [(835, 240), (1005, 240)], RED, "prioridad", (870, 218))
arrow("a-qt-vote", "busa", "vto", [(835, 322), (850, 322)], BLUE)
arrow("a-vote-mca", "vote", "mca", [(975, 432), (990, 432), (990, 290), (1040, 290), (1040, 260)], BLUE)
arrow("a-vote-mcb", "vote", "mcb", [(990, 370), (1005, 370)], BLUE, dashed=True)
arrow("a-hb", "mca", "mcb", [(1100, 260), (1100, 340)], PINK, "heartbeat", (1040, 310), dashed=True, both=True)
arrow("a-emerg", "lc3", "mca", [(315, 480), (315, 505), (1150, 505), (1150, 215), (1135, 215)], RED,
      "línea directa · respaldo: solo alarmas críticas", (330, 510), dashed=True)

# --- Migración -------------------------------------------------------------
box("facade", 1200, 270, 130, 60, "Facade", "#2f9e44", "#ebfbee")
box("flags", 1200, 400, 130, 60, "Feature flags", ORANGE, "#fff4e6", 15, dashed=True)
box("strangler", 1390, 270, 140, 60, "Strangler", "#2f9e44", "#d3f9d8")
box("new", 1590, 180, 150, 60, "Lógica nueva", "#2f9e44", "#ebfbee", 15)
box("cmp", 1800, 180, 150, 60, "Comparador", ORANGE, "#fff4e6", 15)
box("panel", 2000, 180, 130, 60, "Panel", PURPLE, "#e5dbff")

arrow("a-mca-fac", "mca", "facade", [(1135, 230), (1170, 230), (1170, 300), (1200, 300)], "#2f9e44")
arrow("a-fac-str", "facade", "strangler", [(1330, 300), (1390, 300)], "#2f9e44")
arrow("a-flag-str", "flags", "strangler", [(1330, 430), (1460, 430), (1460, 330)], ORANGE, dashed=True)
arrow("a-str-new", "strangler", "new", [(1530, 290), (1560, 290), (1560, 210), (1590, 210)], "#2f9e44",
      "nuevo", (1535, 255))
arrow("a-new-cmp", "new", "cmp", [(1740, 210), (1800, 210)], "#2f9e44")
arrow("a-cmp-panel", "cmp", "panel", [(1950, 210), (2000, 210)], ORANGE, "alerta", (1955, 188))
arrow("a-cmd", "cmp", "lc1", [(1875, 180), (1875, 115), (315, 115), (315, 180)], ORANGE,
      "comandos R1 · R2 · R3", (900, 92))

# --- Legacy ----------------------------------------------------------------
box("acl", 1590, 400, 150, 60, "ACL", RED, "#ffe3e3")
box("legacy", 1800, 400, 150, 60, "Legacy", RED, "#ffc9c9")
box("legdb", 1800, 490, 150, 60, "BD legacy", RED, "#fff5f5", 15)
box("cdc", 1590, 490, 150, 60, "CDC", RED, "#fff5f5")

arrow("a-str-acl", "strangler", "acl", [(1530, 310), (1560, 310), (1560, 430), (1590, 430)], RED,
      "legacy", (1500, 370))
arrow("a-acl-leg", "acl", "legacy", [(1740, 430), (1800, 430)], RED, both=True)
arrow("a-leg-cmp", "legacy", "cmp", [(1875, 400), (1875, 240)], RED)
arrow("a-leg-db", "legacy", "legdb", [(1875, 460), (1875, 490)], RED)
arrow("a-db-cdc", "legdb", "cdc", [(1800, 520), (1740, 520)], RED)
arrow("a-cdc-bus", "cdc", "busa", [(1590, 530), (845, 530), (845, 410), (835, 410)], RED, "eventos legacy", (1300, 535),
      dashed=True)

# --- Auditoría -------------------------------------------------------------
box("mon", 1590, 660, 150, 60, "Monitoring", PURPLE, "#f3f0ff", 15)
box("side", 1800, 660, 150, 60, "Sidecar", PURPLE, "#e5dbff")
box("audit", 1800, 770, 150, 60, "Audit log", PURPLE, "#f3f0ff")
arrow("a-panel-side", "panel", "side", [(2065, 240), (2065, 690), (1950, 690)], PURPLE, dashed=True)
arrow("a-side-mon", "side", "mon", [(1800, 690), (1740, 690)], PURPLE)
arrow("a-side-audit", "side", "audit", [(1875, 720), (1875, 770)], PURPLE)

# --- Criterios hipotéticos de escalabilidad (texto) ------------------------
zone("scale", 2200, 140, 600, 710, "CRITERIOS HIPOTÉTICOS DE ESCALABILIDAD", "#495057", "#f8f9fa")
text(2220, 180, "\n".join([
    "Sin datos reales aún: umbrales supuestos a validar.",
    "",
    "CARGA BASE",
    "3 reactores × 100 sensores × 20 Hz = 6.000 msg/s",
    "≈ 2.000 msg/s por reactor · ~1,2 MB/s (200 B/msg)",
    "",
    "CUÁNDO ESCALAR",
    "• Lag carril alertas > 10 ms → + lectores dedicados",
    "• Alertas descartadas > 0 → alarma máxima",
    "• Lag telemetría > 100 ms por 1 min → + consumidor",
    "• CPU consumidores > 70 % por 5 min → escalar horizontal",
    "• p99 decisión crítica > 50 ms → mover lógica al borde",
    "• Telemetría descartada > 5 % → revisar capacidad",
    "• Audit log > 70 % disco → rotar a almacenamiento frío",
    "",
    "CÓMO CRECE",
    "• + sensores → más particiones del carril telemetría",
    "• + reactor → nuevo carril (alertas + telemetría)",
    "  + controlador local; no afecta a los demás",
    "• + operadores → más réplicas del panel",
    "",
    "CÓMO SE VALIDAN",
    "• Pruebas de carga a 2× y 5× la carga base",
    "• Revisar umbrales tras 2–4 semanas de datos reales",
    "",
    "Lo crítico escala con el borde, no con el central.",
]), 15)

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": E,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}
out = os.path.join(os.path.dirname(__file__), "..", "chernobyl-arquitectura-v2.excalidraw")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
print("ok", os.path.abspath(out), len(E))
