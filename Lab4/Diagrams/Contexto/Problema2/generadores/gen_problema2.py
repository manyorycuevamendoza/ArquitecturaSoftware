# -*- coding: utf-8 -*-
"""Problema 2: el gasto excesivo de tokens.

Un solo lienzo, en el mismo lenguaje visual que Problema1/problema1.excalidraw:
sin marcos de zona, títulos sueltos de tamaño variable, escenas escalonadas y
flechas largas que serpentean de una a otra. El guion vive junto a su escena, no
en una columna aparte.

Se dibuja desde ../../00-contexto-diagrama.md (PD-9 a PD-12) y desde
../../01-decision-ai-gateway.md (las 16 filas, los 9 casos vivos).
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "Problema1", "generadores")))
from _lib import *  # noqa: F403

c = Canvas()
FLOW = "#846358"   # el hilo que une las escenas, como en el Problema 1


def curva(x1, y1, x2, y2, bulge=0.22, color=FLOW, dashed=False):
    """Flecha de tres puntos: el hilo entre escenas nunca es una recta."""
    dx, dy = x2 - x1, y2 - y1
    mx, my = x1 + dx / 2 - dy * bulge, y1 + dy / 2 + dx * bulge
    return c._add({"type": "arrow", "x": x1, "y": y1,
                   "width": abs(dx), "height": abs(dy), "strokeColor": color,
                   "strokeWidth": 2, "strokeStyle": "dashed" if dashed else "solid",
                   "roughness": 1, "roundness": {"type": 2},
                   "points": [[0, 0], [mx - x1, my - y1], [dx, dy]],
                   "lastCommittedPoint": None, "startBinding": None,
                   "endBinding": None, "startArrowhead": None,
                   "endArrowhead": "arrow"})


def rotulo(x, y, s, size=25, color=INK):
    c.txt(x, y, s, size, color)


def chips(x, y, w, h, items, gap=12, tsize=11):
    for i, (col, t, s) in enumerate(items):
        c.box(x + i * (w + gap), y, w, h, col, t, s, tsize, 9)


c.txt(60, 40, "Problema 2: el gasto excesivo de tokens", 26, INK)
c.txt(60, 80, "Cuatro puntos de decisión, 18 casos. La llamada al modelo es lo último "
              "que queda, y casi nunca se llega a ella.", 13, MUTE)

# ══════════════════════════════════════════════════════════════════════
# 1 · LA DOCENTE ENTRA
# ══════════════════════════════════════════════════════════════════════
rotulo(300, 128, "LA DOCENTE ENTRA", 17)

c.box(120, 168, 170, 66, ACTOR, "Rosa", "docente de 4to grado", 15, 9)
c.arw(290, 201, 336, 201)
c.txt(296, 183, "entra", 10, MUTE)
c.box(340, 160, 190, 80, SERV, "Login", ("identidad · escuela", "cuota del mes"), 15, 9)
c.arw(530, 200, 576, 200)
c.dbox(580, 158, 160, 86, "users", ("token_quota · role", "school_id"))

c.txt(120, 286, "Un pedido anónimo no se puede presupuestar ni auditar.", 10, BAD)

c.txt(120, 336,
      "1. El primer gasto se evita antes de escribir la\n"
      "   primera palabra: Rosa entra con su cuenta.\n"
      "\n"
      "2. El login trae quién pide, de qué escuela y\n"
      "   cuánta cuota le queda.", 12, BODY)

curva(748, 196, 856, 250)

# ══════════════════════════════════════════════════════════════════════
# 2 · ¿SE PUEDE ARMAR EL PROMPT?
# ══════════════════════════════════════════════════════════════════════
rotulo(900, 150, "¿SE PUEDE ARMAR EL PROMPT?", 20)
c.txt(900, 178, "PD-9 · Clarification Gate · 5 casos · este paso cuesta 0 tokens externos", 11, MUTE)

c.box(860, 212, 185, 72, SERV, "Formulario",
      ("solicitud intermedia", "objetivo · grado · formato"), 14, 9)
c.arw(1045, 248, 1091, 248)

c.txt(1095, 196, "orden de evaluación", 10, MUTE)
c.box(1095, 214, 215, 44, DB, "1. ¿Plantilla vigente?", None, 12)
c.box(1095, 266, 215, 44, DB, "2. ¿Tiene cuota?", None, 12)
c.box(1095, 318, 215, 44, DB, "3. ¿Campos completos?", None, 12)

c.box(1350, 242, 205, 76, LOGIC, "Clarification Gate",
      ("no invoca al modelo", "0 tokens externos"), 14, 9)
c.arw(1310, 236, 1350, 264)
c.arw(1310, 288, 1350, 280)
c.arw(1310, 340, 1350, 296)
c.dbox(1352, 352, 200, 82, "prompt_templates", ("required_fields", "budget · version"))
c.arw(1452, 352, 1452, 322)
c.txt(1562, 262, "el Gate lee de la plantilla\nqué campos exige;\nno los inventa", 10, BODY)

chips(860, 448, 178, 92, [
    (BAD,  "SIN PLANTILLA",             ("no se puede construir", "el prompt; avisa a Valeria")),
    (WARN, "FALTAN CAMPOS",             ("máximo tres preguntas", "concretas, 0 tokens")),
    (WARN, "FALTAN CAMPOS\nY SIN CUOTA", ("se avisa la cuota antes", "de pedir nada")),
    (OK,   "LISTO PARA\nGENERAR",       ("se arma el prompt", "canónico y sigue")),
    (BAD,  "CUOTA AGOTADA",             ("queda lista y en espera", "de cuota; no se invoca")),
], gap=10)

c.txt(860, 556, "P25: preguntar usando el modelo   ·   P30: avisar de la cuota al final", 10, BAD)

c.txt(860, 596,
      "3. Sin plantilla vigente no se sabe siquiera qué campos son\n"
      "   obligatorios: esa pregunta va primera.\n"
      "\n"
      "4. La cuota se revisa antes de preguntar; enterarse al final es\n"
      "   perder el tiempo.", 12, BODY)

curva(1790, 300, 1900, 220)

# ══════════════════════════════════════════════════════════════════════
# 3 · ¿QUÉ ENTRA AL PROMPT?
# ══════════════════════════════════════════════════════════════════════
rotulo(1990, 118, "¿QUÉ ENTRA AL PROMPT?", 20)
c.txt(1990, 146, "PD-11 · el archivo intermedio es la frontera de costo · 4 casos", 11, MUTE)

c.box(1930, 190, 190, 64, SERV, "Normalizador", "quita ruido y repetición", 14, 9)
c.arw(2120, 222, 2160, 222)
c.box(2164, 190, 200, 64, LOGIC, "Context Builder", "elige qué contexto entra", 14, 9)
c.arw(2364, 222, 2404, 222)
c.dbox(2408, 182, 195, 84, "context_chunks", ("tags · token_count", "COM-4-INF-02 · COM-4-RUB-01"))

c.txt(2640, 190, "Lo que entra aquí se paga.\n"
                 "Lo que se queda fuera es\n"
                 "gratis para siempre.", 11, BODY)

chips(1930, 300, 215, 88, [
    (BAD,  "RUIDO",          ("se elimina", "«hola, mil gracias»")),
    (BAD,  "REDUNDANTE",     ("se elimina: ya viaja", "como campo del formulario")),
    (OK,   "ACOTABLE",       ("entran solo los fragmentos", "etiquetados, no el temario")),
    (OK,   "IMPRESCINDIBLE", ("entra literal y cuenta", "contra el presupuesto")),
])

c.txt(1930, 412,
"CONCEPTO                          LIBRE  GATEWAY\n"
"saludos y cortesias                  80        0\n"
"grado y curso ya en el formulario   120        0\n"
"temario completo de Comunicacion  1,100      352\n"
"objetivo pedagogico y limites       400      280\n"
"instrucciones de formato            300      210\n"
"TOTAL                             2,000      842   -58%",
      10, BODY, fam=3)

c.txt(2430, 412,
      "El 55% del ahorro sale de un\n"
      "solo caso: ACOTABLE.\n"
      "\n"
      "Limpiar saludos aporta el\n"
      "10%: con eso no se llega.", 10, BODY)

c.txt(1930, 528, "P28: adjuntar el temario completo «por si acaso»   ·   "
                 "P29: arrastrar toda la conversación anterior", 10, BAD)

c.txt(1930, 568,
      "5. Cada dato responde tres preguntas: ¿hace falta?, ¿ya viaja por\n"
      "   otro campo?, ¿se puede acotar a un fragmento?\n"
      "\n"
      "6. De 2,000 a 842 tokens. El 58% no sale de limpiar el texto:\n"
      "   sale de no mandar el temario entero.", 12, BODY)

curva(2860, 320, 2960, 400)

# ══════════════════════════════════════════════════════════════════════
# 4 · ¿YA EXISTE ESTA RESPUESTA?
# ══════════════════════════════════════════════════════════════════════
rotulo(2980, 296, "¿Ya existe esta respuesta?", 25)
c.txt(2980, 330, "PD-10 · la caché se consulta ANTES del presupuesto · 5 casos", 11, MUTE)

c.txt(2940, 372,
"huella = hash(prompt_id + version + valores de campos\n"
"              + chunkIds + modelo + curriculum_version)", 10, BODY, fam=3)

c.box(2940, 428, 195, 44, DB, "¿Existe la huella?", None, 12)
c.box(3145, 428, 220, 44, DB, "¿Versión curricular vigente?", None, 11)
c.box(3375, 428, 150, 44, DB, "¿Hay red?", None, 12)
c.box(3560, 420, 215, 60, LOGIC, "Caché de resultados", "vive en el nodo local", 14, 9)
c.arw(3525, 450, 3560, 450)

chips(2940, 512, 185, 96, [
    (OK,    "ACIERTO DE CACHÉ",      ("devuelve el generationId", "0 tokens · funciona sin red")),
    (WARN,  "HUELLA VIEJA",          ("no se devuelve; se regenera", "contra la versión vigente")),
    (BAD,   "HUELLA VIEJA\nSIN RED", ("PENDING_NETWORK; nunca", "se entrega el resultado viejo")),
    (LOGIC, "SIN CACHÉ\nCON RED",    ("pasa al presupuesto:", "es candidata a costar")),
    (WARN,  "SIN CACHÉ\nSIN RED",    ("PENDING_NETWORK con", "la cuota reservada")),
], gap=10)

c.txt(2940, 636,
      "La caché es lo único que produce material con IA durante un corte.", 10, OK)
c.txt(2940, 692, "P26: entregar el resultado de 2026 porque no hay red   ·   "
                 "P27: huella sin la versión curricular", 10, BAD)

c.txt(2940, 732,
      "7. Ocho combinaciones, cuatro colapsan: sin huella no hay versión que\n"
      "   comparar, y con huella vigente el resultado sirve con red o sin ella.", 12, BODY)

curva(3800, 470, 3930, 400)

# ══════════════════════════════════════════════════════════════════════
# 5 · ¿CABE EN EL PRESUPUESTO?
# ══════════════════════════════════════════════════════════════════════
rotulo(4010, 232, "¿Cabe en el presupuesto?", 25)
c.txt(4010, 266, "PD-12 · Budget Guard · el último control antes de salir a Internet · 4 casos", 11, MUTE)

c.box(3960, 308, 196, 44, DB, "¿Cabe la entrada?", None, 12)
c.box(4166, 308, 210, 44, DB, "¿Se puede recortar?", None, 12)
c.box(4386, 308, 190, 44, DB, "¿Cabe la salida?", None, 12)
c.box(4610, 300, 235, 60, LOGIC, "Budget Guard",
      "maxInputTokens 700 · maxOutputTokens 450", 14, 8)
c.arw(4576, 330, 4610, 330)

chips(3960, 392, 215, 96, [
    (OK,   "DENTRO DE\nPRESUPUESTO",     ("invocar una vez, con tope", "de entrada y de salida")),
    (WARN, "SALIDA EXCEDIDA",            ("recortar el formato pedido", "y volver a estimar")),
    (WARN, "ENTRADA EXCEDIDA\nREDUCIBLE", ("quitar los fragmentos", "menos pertinentes")),
    (BAD,  "BLOQUEO",                    ("no se invoca; se le explica", "a Rosa qué recortar")),
])

c.txt(3960, 504,
      "El bloqueo no es un error: es el sistema funcionando. Se recorta el contexto,\n"
      "nunca el objetivo.", 10, BODY)
c.txt(3960, 552,
      "SALIDA EXCEDIDA es el caso que más se olvida: se controla el prompt y se\n"
      "ignora la respuesta, que suele ser la parte cara.", 10, WARN)
c.txt(3960, 600, "P31: controlar solo los tokens de entrada", 10, BAD)

c.txt(3960, 640,
      "8. La estimación mira las dos direcciones: lo que entra y lo que sale.\n"
      "\n"
      "9. Tras un bloqueo el sistema no reintenta solo: devuelve el control\n"
      "   a Rosa.", 12, BODY)

curva(4870, 340, 4990, 300)

# ══════════════════════════════════════════════════════════════════════
# 6 · LA LLAMADA
# ══════════════════════════════════════════════════════════════════════
rotulo(5040, 168, "LA LLAMADA", 37)
c.txt(5044, 220, "el único paso de todo el recorrido que cuesta dinero", 12, MUTE)

c.box(5020, 268, 180, 62, LOGIC, "AI Gateway", "en Lima", 14, 9)
c.arw(5200, 299, 5244, 299)
c.box(5248, 268, 190, 62, SERV, "Proveedor de IA", "una sola invocación", 13, 9)
c.arw(5438, 299, 5482, 299)
c.dbox(5486, 260, 200, 84, "ai_generations", ("input · output · costo", "cache_hit · modelo"))

c.txt(5020, 372,
"0 TOKENS    validar · aclarar · normalizar · seleccionar\n"
"            presupuestar · encolar · reutilizar\n"
"FACTURADO   generar: una vez, con tope de entrada y de salida", 10, BODY, fam=3)

c.txt(5020, 440, "P32: no registrar las llamadas fallidas", 10, BAD)

c.txt(5020, 480,
      "10. Se llega aquí cuando ya se descartó\n"
      "    preguntar, acotar, reutilizar y bloquear.", 12, BODY)

# ══════════════════════════════════════════════════════════════════════
# 7 · SIN RED, LA SOLICITUD ESPERA
# ══════════════════════════════════════════════════════════════════════
rotulo(4290, 792, "Sin red, la solicitud espera", 25)

c.box(4700, 790, 225, 66, WARN, "Cola PENDING_NETWORK", "con la cuota reservada", 12, 9)
curva(5016, 334, 4870, 786, bulge=0.10, color=WARN, dashed=True)
c.txt(4952, 690, "sin red", 10, WARN)
curva(4788, 788, 4998, 336, bulge=-0.10, color=WARN)
c.txt(4676, 690, "al volver la red", 10, MUTE)

c.txt(4970, 786,
      "Al drenar la cola se recalcula la huella contra la versión vigente y se vuelve\n"
      "a pasar por campos, caché y presupuesto: lo encolado no es un permiso de gasto.", 11, BODY)

c.txt(4700, 880, "Sin reserva de cuota, veinte solicitudes en cola rompen\n"
                 "el presupuesto mensual en un minuto.", 10, BAD)

c.txt(4700, 930,
      "11. Este caso no aparece si se desarrolla con Internet:\n"
      "    se descubre en la escuela, no en el laboratorio.", 12, BODY)

curva(5664, 348, 5900, 716)

# ══════════════════════════════════════════════════════════════════════
# 8 · ¿SE LOGRÓ EL 40%?
# ══════════════════════════════════════════════════════════════════════
rotulo(5940, 704, "¿Se logró el 40%?", 25)
c.txt(5940, 738, "la medición contra una línea base comparable", 11, MUTE)

c.dbox(5900, 778, 190, 86, "token_baselines", ("baseline · gateway", "reduction_pct"))
c.arw(6090, 821, 6128, 821)
c.box(6132, 788, 200, 66, SERV, "Reporte de reducción", "por curso y escuela", 13, 9)
c.arw(6332, 821, 6370, 821)
c.box(6374, 788, 170, 66, ACTOR, "Valeria", "aprueba o no", 14, 9)

c.txt(5900, 892,
"reduccion = (tokens_base - tokens_gateway) / tokens_base x 100\n"
"\n"
"una solicitud tipica    2,000  ->      842     -58%\n"
"30 tareas del piloto   60,000  ->  <=36,000    meta -40%", 10, BODY, fam=3)

c.txt(5900, 982,
      "La línea base fija tarea, modelo y versión curricular: si cambia una,\n"
      "el 40% deja de significar algo.", 10, BODY)
c.txt(5900, 1026, "P33: medir contra una línea base no comparable   ·   "
                  "P34: el prompt vive en el chat del docente", 10, BAD)

c.txt(5900, 1066,
      "12. La meta se aprueba solo sobre tareas comparables.\n"
      "\n"
      "13. Un número que no se puede reproducir no es una medición.", 12, BODY)

c.txt(6180, 1140, "LIMA · EL CÍRCULO SE CIERRA", 17, MUTE)

# ══════════════════════════════════════════════════════════════════════
# EL CRUCE COMPLETO — el mismo recorrido, visto de una sola vez
# ══════════════════════════════════════════════════════════════════════
rotulo(900, 800, "El cruce completo del Gateway", 20)
c.txt(900, 830, "2 × 2 × 2 × 2 = 16 filas. Están las 16; las ocho con A = no colapsan en una.", 11, MUTE)

c.txt(900, 866,
"campos  cache  presup.  red    CASO\n"
"\n"
"  no      -       -      -     FALTA DATO\n"
"  si     si      si     si     REUSO\n"
"  si     si      si     no     REUSO OFFLINE\n"
"  si     si      no     si     REUSO SIN CUOTA\n"
"  si     si      no     no     REUSO SIN CUOTA NI RED\n"
"  si     no      si     si     GENERAR    <- el unico que cuesta\n"
"  si     no      si     no     PENDIENTE DE RED\n"
"  si     no      no     si     PRESUPUESTO EXCEDIDO\n"
"  si     no      no     no     BLOQUEO SIN RED", 10, BODY, fam=3)

c.txt(900, 1030,
      "REUSO SIN CUOTA fija el orden: la caché va antes que el Budget Guard.", 10, BODY)
c.txt(900, 1062,
      "El acierto de caché sin red supone que la caché vive en el nodo local:\n"
      "supuesto declarado, no dado por el enunciado.", 10, WARN)

n = c.save(os.path.join(os.path.dirname(HERE), "problema2.excalidraw"))
print("problema2:", n, "elementos")
