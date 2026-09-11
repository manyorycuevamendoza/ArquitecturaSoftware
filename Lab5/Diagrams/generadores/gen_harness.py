# -*- coding: utf-8 -*-
"""Harness de Genius-x: diagrama básico de la solución propuesta por el equipo,
con las correcciones marcadas con estrella. El aprendizaje no es un módulo
aparte: es un lazo cerrado LLM → ingeniero → BD3 → BD2 → LLM."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *

LLMC = "#9c36b5"   # morado uva: el modelo

c = Canvas()
titulo(c, "Genius-x — Harness del LLM",
       "El LLM propone, el harness decide. El estado se responde sin pasar por el modelo, "
       "y lo que el LLM aprende vuelve por las bases, no por la conversación.")
c.txt(1230, 30, "★ = agregado o corregido\nsobre el diseño original", 12, MUTE)

# ── zonas ───────────────────────────────────────────────
c.zona(220, 100, 940, 710, "HARNESS — todo lo que rodea al LLM")
c.zona(1180, 100, 450, 710, "DATOS Y QUIÉN LOS GOBIERNA")

# ── usuarios ────────────────────────────────────────────
c.box(20, 170, 160, 70, ACTOR, "Ing. Soporte", "pregunta el estado\nde una incidencia", 13, 10)
c.box(20, 275, 160, 70, ACTOR, "Ing. Desarrollo", "queries, troubleshooting,\nacciones sobre datos", 13, 10)
c.box(20, 380, 160, 70, ACTOR, "Cliente (empresa)", "reporta incidencias\ny entrega su data", 13, 10)
c.arw(180, 200, 245, 225)
c.arw(180, 310, 245, 262)
c.arw(180, 400, 245, 290)

# ── entrada y router ────────────────────────────────────
c.box(245, 190, 175, 100, LOGIC, "Entrada Genius",
      ("quién pregunta y sobre\nqué incidente", "customer · support ·\nengineering ★"), 14, 10)
c.box(450, 190, 180, 100, LOGIC, "¿Qué tipo de\npregunta es? ★",
      "estado · frecuente ·\nconocimiento · acción", 14, 10)
c.arw(420, 240, 450, 240)

# ── los cuatro caminos ──────────────────────────────────
c.box(680, 120, 200, 76, SERV, "Estado de la incidencia",
      "sin pasar por el LLM,\ncon sello de hora ★", 13, 10)
c.box(680, 228, 200, 80, SERV, "Respuestas aprobadas ★",
      "misma pregunta,\nmisma respuesta", 13, 10)
c.box(680, 340, 200, 80, SERV, "Fila con prioridad ★",
      "customer (1 día) antes\nque engineering (3 días)", 13, 10)
c.arw(630, 222, 680, 158)
c.arw(630, 240, 680, 265)
c.arw(630, 262, 680, 372)

# ── modelo, portero y aprobación ────────────────────────
c.box(940, 340, 200, 96, LLMC, "LLM local",
      ("versión fija, no inventa ★", "varias réplicas ★",
       "responde con lo aprobado en BD2 ★"), 15, 10)
c.arw(880, 380, 940, 380)

c.box(940, 490, 200, 96, BAD, "Portero de acciones ★",
      ("leer  →  pasa directo", "cambiar  →  necesita aprobación"), 14, 10)
c.arw(1040, 436, 1040, 490, BAD)
c.txt(1052, 446, "propone,\nno ejecuta", 10, BAD)

c.box(940, 620, 200, 76, ACTOR, "Incident Manager ★",
      ("aprueba lo que cambia datos", "y qué respuesta se guarda"), 13, 10)
c.arw(1040, 620, 1040, 586, ACTOR)

# ── el lazo de aprendizaje, dentro del mismo flujo ──────
c.txt(470, 596, "EL CICLO DE APRENDIZAJE ★", 12, INK)
c.box(470, 620, 185, 76, SERV, "Respuesta al ingeniero",
      "con evidencia y hora ★", 13, 10)
c.box(690, 620, 185, 76, SERV, "El ingeniero califica ★",
      "correcta / incorrecta\n+ motivo", 13, 10)
c.arw(985, 436, 650, 630, LLMC)
c.arw(655, 658, 690, 658)
c.arw(875, 658, 940, 658)
c.arw(1140, 655, 1420, 505, ACTOR)

# ── notas de riesgo ─────────────────────────────────────
c.txt(245, 470, "Si el LLM se satura en el pico de\n"
                "la primera semana, el estado y\n"
                "las respuestas aprobadas siguen\n"
                "saliendo. ★", 11, WARN)
c.txt(245, 548, "Lo que el cliente escribe en el\n"
                "ticket es DATO, nunca una orden\n"
                "para el sistema. ★", 11, BAD)
c.txt(245, 622, "El LLM no tiene permiso para\n"
                "borrar: el permiso lo pone la\n"
                "persona que aprueba. ★", 11, BAD)

# ── bitácora ────────────────────────────────────────────
c.box(245, 730, 895, 58, MUTE,
      "Bitácora ★ — quién pidió, qué se respondió, quién aprobó",
      "nadie la puede editar ni borrar", 14, 10)

# ── MCP y bases ─────────────────────────────────────────
c.box(1200, 235, 150, 90, SERV, "MCP ×2 ★", "única puerta\na las bases", 14, 10)
c.arw(880, 158, 1200, 255)
c.arw(880, 268, 1200, 272)
c.arw(1140, 368, 1200, 300)
c.arw(1200, 318, 1145, 392, DB)
c.arw(1140, 520, 1205, 325, BAD)

c.dbox(1400, 115, 190, 86, "BD1 — Estado actual",
       "se actualiza al cambiar,\nno cada 5 min ★")
c.dbox(1400, 262, 190, 86, "BD2 — Conocimiento",
       "histórico, troubleshooting\ny respuestas aprobadas")
c.dbox(1400, 430, 190, 86, "BD3 — Candidatos ★",
       "data del cliente y respuestas\ncalificadas, aún sin aprobar")
c.arw(1350, 262, 1400, 170)
c.arw(1350, 295, 1400, 300)

c.arw(1495, 201, 1495, 262, WARN, dashed=True)
c.txt(1400, 358, "BD2 respalda a BD1, pero el relevo\ntiene que ser automático ★", 10, WARN, "center", 190)

c.box(1195, 430, 150, 86, ACTOR, "Data Science",
      "cura y pasa a BD2\nsolo lo aprobado ★", 13, 10)
c.arw(1400, 473, 1350, 473)
c.arw(1290, 430, 1398, 352, ACTOR)

c.txt(245, 826,
      "El lazo se cierra por las bases, no por la conversación: el LLM responde, el ingeniero califica, lo calificado\n"
      "cae en BD3 como candidato y solo lo que se aprueba pasa a BD2, que es de donde el LLM vuelve a leer. Sin ese\n"
      "filtro, una respuesta inventada con buen score se guardaría como verdad y el LLM la repetiría con más confianza. ★",
      12, BAD)

HERE = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(os.path.dirname(HERE), "harness-genius.excalidraw")
print(c.save(out), "elementos →", out)
