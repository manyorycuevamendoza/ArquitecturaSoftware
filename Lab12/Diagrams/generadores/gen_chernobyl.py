# -*- coding: utf-8 -*-
"""Save Chernobyl: modernización legacy (README 12) + reliability / fault tolerance."""
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


# --- Títulos y zonas -------------------------------------------------------
text(40, 20, "SAVE CHERNOBYL — ARQUITECTURA (Lab 12)", 28)
text(40, 62, "Migración evolutiva del legacy (Strangler + Parallel Run) · decisión crítica en el borde · sin SPOF",
     16, "#868e96")

zone("edge", 40, 110, 460, 890, "BORDE — 3 REACTORES (tiempo real)", "#2b8a3e", "#f4fcf5")
zone("core", 540, 110, 560, 890, "MENSAJERÍA + CONTROL (alta disponibilidad)", "#1971c2", "#f8fbff")
zone("legacy", 1140, 110, 460, 600, "LEGACY — no se detiene", "#c92a2a", "#fff8f8", dashed=True)
zone("ops", 1140, 740, 460, 260, "OPERACIÓN + AUDITORÍA", "#5f3dc4", "#f9f7ff")

# --- Borde: reactores ------------------------------------------------------
for i in range(3):
    y = 160 + i * 235
    n = i + 1
    box(f"s{n}", 60, y, 180, 80, f"100 sensores R{n}\n1 lectura / 0.05 s", "#2b8a3e", "#ebfbee", 15)
    extra = "\npiloto lib. eventos" if n == 3 else ""
    box(f"lc{n}", 270, y, 210, 110,
        f"Controlador local R{n}\nrefrigeración + alertas\nFAIL-SAFE · par redundante{extra}",
        "#2b8a3e", "#d3f9d8", 14)
    arrow(f"a-s{n}", f"s{n}", f"lc{n}", [(240, y + 40), (270, y + 40)], "#2b8a3e")

box("bba", 60, 880, 420, 100,
    "BRANCH BY ABSTRACTION\nEventTransport → lib actual | lib nueva\nfeature flag usar_libreria_nueva (solo R3)",
    "#e67700", "#fff4e6", 14)

# --- Núcleo ----------------------------------------------------------------
box("bus", 570, 160, 500, 90, "MESSAGE BUS (BMQ)  A activo ↔ B réplica\nparticionado por reactor: R1 · R2 · R3",
    "#1971c2", "#e7f5ff", 15)
box("vote", 570, 290, 500, 70, "Validación de sensores\ntimeout · votación (mediana) · outliers", "#1971c2", "#e7f5ff", 15)
box("mca", 570, 400, 240, 90, "Main Controller A\nACTIVO", "#1971c2", "#d0ebff")
box("mcb", 830, 400, 240, 90, "Main Controller B\nPASIVO (standby)", "#1971c2", "#e7f5ff", dashed=True)
box("strangler", 570, 530, 500, 90, "STRANGLER + FACADE\nruteo por reactor con feature flag (R1 → R2 → R3)",
    "#2f9e44", "#ebfbee", 15)
box("cmp", 570, 660, 500, 90, "PARALLEL RUN — Comparador\nlógica nueva vs legacy: coinciden → comando\ndiscrepan → no actúa, manda el legacy",
    "#e67700", "#fff4e6", 14)
box("spof", 570, 790, 500, 190,
    "SPOF → MITIGACIÓN\n"
    "Main Controller → activo/pasivo + heartbeat\n"
    "Bus → réplica B + buffer local en el borde\n"
    "Controlador local → par redundante + protección física\n"
    "Sensor → votación entre los 100 del reactor\n"
    "Strangler / BD auditoría → 2 instancias / replicación\n"
    "Red → enlaces redundantes; el borde opera aislado",
    "#a61e4d", "#fff0f6", 14)

# --- Legacy ----------------------------------------------------------------
box("acl", 1170, 160, 400, 80, "ACL — Anticorruption Layer\nformato antiguo ↔ JSON moderno", "#c92a2a", "#ffe3e3", 15)
box("leg", 1170, 280, 400, 100, "SISTEMA LEGACY\ncontrol actual · fuente de verdad", "#c92a2a", "#ffc9c9")
box("legdb", 1170, 420, 190, 80, "BD Legacy", "#c92a2a", "#fff5f5")
box("inter", 1380, 420, 190, 80, "EVENT INTERCEPTION\nSQL trigger / CDC", "#c92a2a", "#fff5f5", 14)
box("view", 1170, 540, 400, 60, "DATABASE VIEW LAYER (reportes)", "#c92a2a", "#fff5f5", 14)
box("etl", 1170, 620, 400, 70, "Datos históricos: ETL (batch)\n+ CDC (sincronización sin downtime)", "#c92a2a", "#fff5f5", 14)

# --- Operación -------------------------------------------------------------
box("panel", 1170, 790, 190, 90, "Panel operadores\ntiempo real\nalarmas · reportes", "#5f3dc4", "#e5dbff", 14)
box("side", 1380, 790, 190, 90, "SIDECAR PROXY\nlogging · monitoring", "#5f3dc4", "#e5dbff", 14)
box("audit", 1380, 900, 190, 80, "Audit log\nappend-only · replicado", "#5f3dc4", "#f3f0ff", 14)
text(1160, 905, "quién · qué · cuándo\n· origen", 13, "#5f3dc4")

# --- Flechas ---------------------------------------------------------------
for n, y in ((1, 200), (2, 435), (3, 670)):
    arrow(f"a-lc{n}-bus", f"lc{n}", "bus", [(480, y), (525, y), (525, 205), (570, 205)], "#1971c2")
text(395, 138, "buffer local si cae el bus", 13, "#1971c2")

arrow("a-bus-vote", "bus", "vote", [(820, 250), (820, 290)], "#1971c2")
arrow("a-vote-mca", "vote", "mca", [(690, 360), (690, 400)], "#1971c2")
arrow("a-vote-mcb", "vote", "mcb", [(950, 360), (950, 400)], "#1971c2", dashed=True)
arrow("a-hb", "mca", "mcb", [(810, 445), (830, 445)], "#a61e4d", dashed=True, both=True)
text(840, 498, "heartbeat · failover", 13, "#a61e4d")
arrow("a-mca-str", "mca", "strangler", [(690, 490), (690, 530)], "#2f9e44")
arrow("a-str-cmp", "strangler", "cmp", [(820, 620), (820, 660)], "#2f9e44", "lógica nueva", (830, 630))
arrow("a-str-acl", "strangler", "acl", [(1070, 575), (1105, 575), (1105, 200), (1170, 200)], "#c92a2a",
      "Facade", (1040, 255))
arrow("a-acl-leg", "acl", "leg", [(1370, 240), (1370, 280)], "#c92a2a", both=True)
arrow("a-leg-db", "leg", "legdb", [(1265, 380), (1265, 420)], "#c92a2a")
arrow("a-db-inter", "legdb", "inter", [(1360, 460), (1380, 460)], "#c92a2a")
arrow("a-inter-bus", "inter", "bus", [(1570, 460), (1590, 460), (1590, 152), (900, 152), (900, 160)],
      "#c92a2a", "eventos del legacy → bus", (1180, 132), dashed=True)
arrow("a-leg-cmp", "leg", "cmp", [(1170, 340), (1125, 340), (1125, 715), (1070, 715)], "#c92a2a",
      "decisión legacy", (1000, 395))
arrow("a-cmp-lc3", "cmp", "lc3", [(570, 725), (480, 725)], "#e67700",
      "comandos a R1 · R2 · R3", (300, 750))
arrow("a-cmp-panel", "cmp", "panel", [(1070, 740), (1150, 740), (1150, 835), (1170, 835)], "#e67700",
      "discrepancia / alarma", (950, 765), dashed=True)
arrow("a-panel-side", "panel", "side", [(1360, 835), (1380, 835)], "#5f3dc4", dashed=True)
arrow("a-side-audit", "side", "audit", [(1475, 880), (1475, 900)], "#5f3dc4")

# --- Explicación -----------------------------------------------------------
zone("explain", 1640, 110, 640, 890, "¿CÓMO FUNCIONA?", "#495057", "#f8f9fa")
text(1660, 150, "\n".join([
    "Carga: 3 reactores × 100 sensores × 20 Hz = 6.000 msg/s",
    "",
    "1. Lectura: cada sensor envía al controlador local de su",
    "   reactor. Si pasa el umbral, el controlador enfría SOLO",
    "   (fail-safe), sin esperar red ni Main Controller.",
    "2. Datos: el borde publica al bus (partición por reactor).",
    "   Event Interception / CDC copia lo que pasa en el legacy",
    "   al bus sin modificar su código.",
    "3. Decisión global: el Main Controller A (B en standby)",
    "   recibe datos validados (votación de sensores).",
    "4. Strangler + Facade: decide por reactor si actúa la",
    "   lógica nueva o el legacy (vía ACL, que traduce formato).",
    "5. Parallel Run: ambos deciden; si coinciden se envía el",
    "   comando, si discrepan manda el legacy y se alerta.",
    "6. Trazabilidad: el sidecar registra quién prendió o apagó",
    "   qué en un audit log append-only.",
    "",
    "FAILURE SCENARIOS",
    "• Sensor mudo (> 0.15 s) → se excluye, mediana del resto",
    "• Valor absurdo → outlier, alerta de revisión, no apaga",
    "• Cae MC A → B asume por heartbeat",
    "• Caen A y B → controladores locales en modo seguro",
    "• Cae el bus → buffer local y reenvío",
    "• Falla lib nueva → apagar flag (rollback inmediato)",
    "",
    "MIGRACIÓN (evolutiva, no Big Bang)",
    "0 foto actual → 1 observar (sidecar + CDC) → 2 Facade/ACL",
    "→ 3 Parallel Run R1 → 4 Strangler R1→R2→R3 → 5 retiro legacy",
    "",
    "ESCALABILIDAD (criterios hipotéticos)",
    "• lag de cola > 100 ms por 1 min → + consumidor",
    "• CPU > 70 % por 5 min → escalar horizontal",
    "• p99 decisión crítica > 50 ms → mover lógica al borde",
    "• nuevo reactor → nueva partición + controlador local",
]), 15)

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": E,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}
out = os.path.join(os.path.dirname(__file__), "..", "chernobyl-arquitectura.excalidraw")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
print("ok", os.path.abspath(out), len(E))
