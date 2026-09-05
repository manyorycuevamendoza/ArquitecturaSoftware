# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *

c = Canvas()
titulo(c, "D. ¿Conviene sincronizar ahora?",
       "PD-7 + PD-4 + PD-8. Catorce casos. Tres preguntas que se responden antes de abrir la transferencia.")

# ══════════ ITERACIÓN 1 ══════════
y = c.header(20, 108, 1, "Tres preguntas, y el orden importa", None)
c.txt(20, y,
"1. Antes de bajar un solo byte el nodo se\n"
"   hace tres preguntas, y el orden\n"
"   importa.\n"
"\n"
"2. Primero: ¿conviene sincronizar ahora?\n"
"   Mira la red, el horario y la energía.\n"
"\n"
"3. Segundo: ¿cuánto me atrasé? Puede ser\n"
"   una semana o pueden ser cuatro.\n"
"\n"
"4. Tercero: ¿me cabe en el disco? La\n"
"   activación atómica necesita dos\n"
"   versiones al mismo tiempo.\n"
"\n"
"5. Si cualquiera da que no, no se abre la\n"
"   transferencia. Esperar cuesta cero;\n"
"   empezar y no terminar desperdicia la\n"
"   ventana.", 12, BODY)

c.box(390, 180, 180, 78, LOGIC, "¿Ahora?", ("PD-7", "red, clase, energía"), 15, 9)
c.box(612, 180, 180, 78, LOGIC, "¿Cuánto?", ("PD-4", "versiones de atraso"), 15, 9)
c.box(834, 180, 180, 78, LOGIC, "¿Me cabe?", ("PD-8", "disco disponible"), 15, 9)
c.box(1046, 186, 145, 66, OK, "Abrir la\ntransferencia", None, 13)
c.arw(570, 219, 612, 219)
c.arw(792, 219, 834, 219)
c.arw(1014, 219, 1046, 219, OK)

c.box(612, 314, 180, 58, WARN, "Esperar", "no se abre nada", 14, 9)
for x in (480, 702, 924):
    c.arw(x, 258, 702, 314, WARN, dashed=True)
c.txt(800, 330, "cualquiera de las tres que dé que no", 10, WARN)

c.line(10, 454, 1200, 454)

# ══════════ ITERACIÓN 2 ══════════
y = c.header(20, 474, 2, "¿Ahora o después? La clase tiene prioridad", None)
c.txt(20, y,
"6. Tres variables: hay señal, es horario\n"
"   de clase, hay energía.\n"
"\n"
"7. Ocho combinaciones nominales. Cuando\n"
"   no hay señal las otras dos dejan de\n"
"   importar, así que cuatro filas\n"
"   colapsan en una. Quedan cinco.\n"
"\n"
"8. La regla que ordena todo no es\n"
"   aprovechar cada ventana de red. Es no\n"
"   estorbar la clase que está pasando.\n"
"\n"
"9. Una sincronización agresiva a mediodía\n"
"   satura el enlace y la LAN. Rosa no\n"
"   puede abrir una guía que ya está en el\n"
"   nodo. El sistema se rompe a sí mismo\n"
"   con su propia tarea de fondo.\n"
"\n"
"10. Y si las 500 escuelas entran a la\n"
"    misma hora, el pico cae entero sobre\n"
"    Lima. Por eso cada escuela espera un\n"
"    rato distinto dentro de la ventana.", 12, BODY)

c.zona(350, 502, 840, 372, "¿SINCRONIZAR AHORA O ESPERAR?  ·  PD-7")

c.box(470, 522, 175, 52, DB, "¿Hay señal?", None, 12)
c.box(663, 522, 175, 52, DB, "¿Horario de clase?", None, 12)
c.box(856, 522, 175, 52, DB, "¿Hay energía?", None, 12)
c.box(633, 604, 245, 58, LOGIC, "Planificador de ventana", None, 14)
c.arw(557, 574, 700, 604)
c.arw(750, 574, 750, 604)
c.arw(943, 574, 810, 604)
c.arw(755, 662, 755, 694)

casos7 = [
    (372,  ZONE, "SIN SEÑAL",            "esperar; la clase sigue\ncorriendo contra el nodo"),
    (537,  OK,   "VENTANA IDEAL",        "sincronizar a fondo,\nincluido lo opcional"),
    (702,  WARN, "SIN ENERGÍA",          "no iniciar; se gasta\nla ventana en vano"),
    (867,  WARN, "HAY CLASE",            "sincronizar con tope\nde ancho de banda"),
    (1032, BAD,  "CLASE Y POCA\nENERGÍA","no sincronizar; todo\nva a servir la LAN"),
]
for x, col, t, acc in casos7:
    c.box(x, 702, 155, 86, col, t, acc, 11, 9)

c.txt(372, 800,
"Nominalmente 2 x 2 x 2 = 8 filas. Cuando no hay señal no se puede transferir sin importar el horario ni\n"
"la energía, así que esas cuatro combinaciones colapsan en una sola. Quedan 5 casos.", 10, MUTE)

c.txt(372, 838,
"Las 500 escuelas no entran a la misma hora: cada una espera un rato aleatorio dentro de la ventana.", 10, BODY)

c.line(10, 900, 1200, 900)

# ══════════ ITERACIÓN 3 ══════════
y = c.header(20, 920, 3, "¿Cuánto me atrasé? ¿Y me cabe?", None)
c.txt(20, y,
"11. El manifiesto no dice qué cambió esta\n"
"    semana. Dice qué debe tener la\n"
"    escuela hoy.\n"
"\n"
"12. Con eso, saltarse tres semanas deja de\n"
"    ser un caso especial: es el mismo\n"
"    algoritmo de comparar dos listas del\n"
"    diagrama A.\n"
"\n"
"13. La escuela que quedó en la semana 9\n"
"    lee el manifiesto de la 12 y baja\n"
"    185 MB, no 369. La guía viaja una\n"
"    sola vez, en su versión final.\n"
"\n"
"14. Diego no pierde el material de las\n"
"    semanas sin señal: sigue vigente en\n"
"    ese manifiesto.\n"
"\n"
"15. Después viene el disco. La activación\n"
"    atómica necesita la versión activa y\n"
"    la nueva al mismo tiempo. Por eso el\n"
"    mínimo por nodo no es 4 GB sino 8.\n"
"\n"
"16. Si no cabe, se libera en orden:\n"
"    primero multimedia vieja, después\n"
"    versiones antiguas completas. Nunca\n"
"    la versión activa ni la cola.\n"
"\n"
"17. La regla que ordena el borrado es que\n"
"    lo que solo existe en la escuela vale\n"
"    más que lo que Lima puede reenviar.", 12, BODY)

# ── PD-4 ──
c.zona(350, 976, 840, 232, "¿CUÁNTO ME ATRASÉ?  ·  PD-4")
casos4 = [
    (372,  OK,   "AL DÍA",          "no hay nada nuevo",       "no se transfiere nada"),
    (537,  OK,   "ATRASO NORMAL",   "una versión, alcanza",    "bajar la diferencia\ny activar"),
    (702,  WARN, "VENTANA CORTA",   "una versión, no alcanza", "lo esencial primero,\nquedar PAUSED"),
    (867,  OK,   "SALTO DE\nVERSIONES", "varias, alcanza",     "comparar contra la\nmás nueva, activar directo"),
    (1032, WARN, "SALTO CON\nVENTANA CORTA", "varias, no alcanza", "por prioridad; sigue\ncon su versión anterior"),
]
for x, col, t, comb, acc in casos4:
    c.box(x, 1004, 155, 94, col, t, (comb, acc), 11, 9)

c.txt(372, 1116,
"ESCUELA EN s9, PENDIENTES s10 s11 s12\n"
"delta encadenado   369 MB   49 min\n"
"estado completo    185 MB   25 min    50% menos", 10, BODY, fam=3)

c.txt(760, 1120,
"La guía viaja una sola vez, en su versión final: las versiones v2 y v3 que s12 ya\n"
"reemplazó nunca se descargan. Y la ficha publicada en s10 sí baja, porque sigue\n"
"vigente en el manifiesto de s12. Diego no pierde nada.", 10, BODY)

# ── PD-8 ──
c.zona(350, 1230, 840, 254, "¿ME CABE EN EL DISCO?  ·  PD-8")
casos8 = [
    (372, OK,   "ESPACIO SUFICIENTE",  "cabe la versión nueva",   "descargar normalmente"),
    (578, WARN, "LIBERAR Y SEGUIR",    "no cabe, hay antiguas",   "borrar antiguas,\nnunca la activa"),
    (784, BAD,  "DISCO LLENO",         "no cabe, cola vacía",     "solo lo esencial,\nalertar al administrador"),
    (990, BAD,  "DISCO LLENO\nCON COLA","no cabe, cola pendiente","enviar la cola primero,\njamás borrarla"),
]
for x, col, t, comb, acc in casos8:
    c.box(x, 1258, 190, 94, col, t, (comb, acc), 11, 9)

c.txt(372, 1370,
"JERARQUIA DE BORRADO\n"
"1. multimedia opcional de versiones antiguas\n"
"2. versiones antiguas completas, menos la activa\n"
"3. NUNCA: version activa, cola de eventos, indice", 10, BODY, fam=3)

c.txt(790, 1370,
"MINIMO POR NODO\n"
"version activa     3.0 GB\n"
"version nueva      3.0 GB\n"
"cola e indices     0.5 GB\n"
"SO y margen        1.5 GB\n"
"                   8.0 GB", 10, BODY, fam=3)

c.txt(372, 1444,
"Lo que solo existe en la escuela vale más que lo que Lima puede volver a mandar.", 10, INK)

# leyenda
c.rect(372, 1508, 470, 132, MUTE, rough=0, sw=1)
c.txt(386, 1518, "PEORES CASOS QUE ATAJA ESTE DIAGRAMA", 11, INK)
c.txt(386, 1540,
"P1   la ventana de conexión no alcanza nunca\n"
"P11  manifiesto como delta encadenado\n"
"P12  el manifiesto describe solo su semana\n"
"P13  descargar las versiones en orden s10, s11, s12\n"
"P14  atraso permanente invisible\n"
"P20  sincronizar sin límite durante la clase\n"
"P21  todas las escuelas sincronizan a la misma hora\n"
"P23  nodo dimensionado a 4 GB\n"
"P24  disco al 100%: no se puede registrar ni el fallo", 10, BODY)

n = c.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "D-cuando-sincronizar.excalidraw"))
print("D:", n, "elementos")
