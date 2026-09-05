# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *

c = Canvas()
titulo(c, "B. ¿Puedo confiar en lo que llegó?",
       "PD-2 + PD-5. Once casos. Las dos decisiones que protegen la versión que Rosa está usando.")

# ══════════ ITERACIÓN 1 ══════════
y = c.header(20, 108, 1, "La pregunta que hay que responder", None)
c.txt(20, y,
"1. El nodo terminó de bajar los archivos\n"
"   de la semana nueva.\n"
"\n"
"2. Antes de mostrarle nada a Rosa tiene\n"
"   que responder una pregunta: ¿esto\n"
"   llegó igual a como salió de Lima?\n"
"\n"
"3. Si la respuesta es no, la regla no se\n"
"   negocia: no se activa nada y la\n"
"   escuela sigue con lo que ya tenía.", 12, BODY)

c.box(400, 178, 165, 70, DB, "Archivos\ndescargados", "todavía nadie los vio", 13)
c.box(630, 172, 200, 82, LOGIC, "¿Puedo confiar?", "hash, firma, respaldo", 15)
c.box(900, 140, 175, 64, OK, "Se activa", "Rosa ve lo nuevo", 13)
c.box(900, 222, 175, 64, WARN, "No se activa", "Rosa sigue con lo viejo", 13)
c.arw(565, 213, 630, 213)
c.arw(830, 200, 900, 176, OK)
c.arw(830, 226, 900, 250, WARN)

c.line(10, 348, 1200, 348)

# ══════════ ITERACIÓN 2 ══════════
y = c.header(20, 368, 2, "Los tres controles y sus ocho combinaciones", None)
c.txt(20, y,
"4. Hay tres cosas que mirar, y son\n"
"   independientes entre sí.\n"
"\n"
"5. El hash de cada archivo dice si el\n"
"   contenido llegó completo.\n"
"\n"
"6. La firma del manifiesto dice si el\n"
"   paquete salió de Lima y no de otro\n"
"   lado.\n"
"\n"
"7. Que exista una versión anterior en\n"
"   READY dice si hay a qué volver.\n"
"\n"
"8. Tres preguntas de sí o no dan ocho\n"
"   combinaciones. Están las ocho,\n"
"   ninguna se inventó y ninguna falta.\n"
"\n"
"9. Solo dos activan. Las otras seis\n"
"   rechazan, y en cuatro de ellas la\n"
"   escuela conserva lo que ya tenía.\n"
"\n"
"10. Las cuatro de abajo son las graves:\n"
"    no hay versión anterior, así que la\n"
"    escuela se queda sin material. Esas\n"
"    cuatro disparan alerta a Lima.", 12, BODY)

c.zona(350, 396, 840, 452, "VALIDACIÓN DEL PAQUETE  ·  PD-2")

c.box(470, 414, 180, 54, DB,  "Hash del archivo", None, 12)
c.box(663, 414, 180, 54, DB,  "Firma del manifiesto", None, 12)
c.box(856, 414, 180, 54, DB,  "¿Hay versión READY?", None, 12)

c.box(633, 502, 240, 60, LOGIC, "Validador de integridad", None, 14)
c.arw(560, 468, 700, 502)
c.arw(753, 468, 753, 502)
c.arw(946, 468, 806, 502)
c.arw(753, 562, 753, 588)

cols = [372, 566, 760, 954]
cw = 180
heads = ["hash ok   firma ok", "hash ok   firma NO",
         "hash NO   firma ok", "hash NO   firma NO"]
for x, h in zip(cols, heads):
    c.txt(x, 594, h, 10, MUTE, "center", cw, fam=3)

c.txt(372, 616, "CON versión anterior en READY   ·   hay a qué volver", 11, OK)
fila1 = [
    (OK,   "OK con respaldo",     "activar la\nversión nueva"),
    (WARN, "Firma inválida",      "rechazar,\nconservar la anterior"),
    (WARN, "Archivo corrupto",    "rechazar el archivo,\nreintentar el bloque"),
    (WARN, "Paquete no confiable","rechazar todo,\nconservar la anterior"),
]
for x, (col, t, s) in zip(cols, fila1):
    c.box(x, 636, cw, 78, col, t, s, 12, 9)

c.txt(372, 730, "SIN versión anterior   ·   la escuela se queda sin material", 11, BAD)
fila2 = [
    (OK,  "OK primera carga",    "activar, es la\nprimera versión"),
    (BAD, "Firma inválida",      "rechazar y\nalertar a Lima"),
    (BAD, "Archivo corrupto",    "rechazar y\nalertar a Lima"),
    (BAD, "Paquete no confiable","rechazar y escalar\na soporte regional"),
]
for x, (col, t, s) in zip(cols, fila2):
    c.box(x, 750, cw, 78, col, t, s, 12, 9)

c.line(10, 880, 1200, 880)

# ══════════ ITERACIÓN 3 ══════════
y = c.header(20, 900, 3, "Se corta la luz justo al activar", None)
c.txt(20, y,
"11. Ya sabemos que los archivos son\n"
"    confiables. Falta activarlos, y ahí\n"
"    puede irse la luz.\n"
"\n"
"12. Activar no es copiar los archivos\n"
"    nuevos encima de los viejos. Es\n"
"    mover un puntero.\n"
"\n"
"13. Cada versión vive en su propio\n"
"    directorio. El puntero ACTIVE apunta\n"
"    a una sola.\n"
"\n"
"14. Moverlo es una única operación del\n"
"    sistema de archivos. No existe un\n"
"    instante en que apunte a media\n"
"    versión.\n"
"\n"
"15. Al reiniciar tras el corte solo hay\n"
"    tres estados posibles, y en los tres\n"
"    la escuela está sirviendo una versión\n"
"    completa y verificada.\n"
"\n"
"16. Hay una cuarta combinación: puntero\n"
"    movido con archivos sin verificar. Es\n"
"    imposible si el orden es correcto. Si\n"
"    alguna vez ocurre, el orden está mal.\n"
"\n"
"17. Por eso el orden no se negocia:\n"
"    descargar, verificar, activar, y\n"
"    recién al final borrar lo viejo.", 12, BODY)

c.zona(350, 976, 840, 366, "ACTIVACIÓN ATÓMICA  ·  PD-5")

c.box(392, 1008, 178, 52, ZONE, "/cache/s11/", "versión anterior", 13, 9)
c.box(392, 1082, 178, 52, ZONE, "/cache/s12/", "nueva, ya verificada", 13, 9)
c.box(630, 1044, 148, 52, LOGIC, "ACTIVE", "el puntero", 14, 9)
c.arw(630, 1058, 570, 1034, MUTE, dashed=True)
c.txt(575, 1014, "antes", 9, MUTE)
c.arw(630, 1082, 570, 1108, OK)
c.txt(575, 1112, "después", 9, OK)

c.txt(830, 1006,
"ORDEN OBLIGATORIO\n"
"1. descargar a /cache/<version>/\n"
"2. verificar hash y firma\n"
"3. mover el puntero ACTIVE\n"
"4. borrar la version anterior", 10, BODY, fam=3)

c.arw(704, 1096, 704, 1170)

cols3 = [372, 573, 774, 975]
casos5 = [
    (WARN, "Corte al descargar",     "archivos NO  ·  puntero NO", "reanudar desde el\núltimo bloque validado"),
    (WARN, "Corte antes de activar", "archivos SI  ·  puntero NO", "mover el puntero,\nla operación es idempotente"),
    (OK,   "Corte tras activar",     "archivos SI  ·  puntero SI", "nada que hacer,\nya está activa"),
    (BAD,  "IMPOSIBLE",              "archivos NO  ·  puntero SI", "si ocurre, se invirtieron\nlos pasos 2 y 3"),
]
for x, (col, t, comb, acc) in zip(cols3, casos5):
    c.box(x, 1170, 185, 88, col, t, (comb, acc), 12, 9, dashed=(t == "IMPOSIBLE"))

c.txt(372, 1272,
"En los tres casos posibles la escuela siempre está sirviendo una versión completa y verificada.\n"
"No existe un estado observable a medias. La cuarta fila es la que demuestra que el orden está bien.",
10, BODY)

# leyenda
c.rect(372, 1356, 430, 118, MUTE, rough=0, sw=1)
c.txt(386, 1366, "PEORES CASOS QUE ATAJA ESTE DIAGRAMA", 11, INK)
c.txt(386, 1388,
"P2   se pierde el índice de bloques validados\n"
"P3   activación parcial de la versión\n"
"P4   firma o hash inválido y sin respaldo\n"
"P9   colisión de hash\n"
"P15  activar copiando archivos encima\n"
"P16  mover el puntero antes de verificar\n"
"P17  borrar la versión anterior antes de activar", 10, BODY)

n = c.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "B-integridad-y-activacion.excalidraw"))
print("B:", n, "elementos")
