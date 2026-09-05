# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *

c = Canvas()
c.txt(20, 20, "Problema 1: distribución con Internet intermitente", 26, INK)
c.txt(20, 58, "Ocho puntos de decisión, 36 casos, 24 peores casos. El recorrido completo, de Valeria a Valeria.", 13, MUTE)
c.line(10, 92, 1210, 92)

def bloque(y, h, etiqueta, color=ZONE):
    c.rect(366, y, 830, h, color, dashed=True, rough=0, sw=1)
    c.txt(380, y + 7, etiqueta, 11, color if color != ZONE else MUTE)

# ═══ 1. LIMA ═══
c.txt(20, 112,
"1. Valeria publica el material de la\n"
"   semana. El CMS arma un manifiesto: la\n"
"   lista de archivos con su hash, y lo\n"
"   firma. Todo queda en el servidor HTTPS.", 12, BODY)
bloque(110, 120, "LIMA  ·  PUBLICACIÓN")
c.box(392, 142, 138, 62, ACTOR, "Valeria", None, 14)
c.box(566, 142, 158, 62, SERV, "CMS +\nPublicador", None, 12)
c.box(760, 142, 158, 62, SERV, "Servidor\nHTTPS", None, 12)
c.dbox(958, 134, 132, 78, "BD Lima", "packages / files")
c.arw(530, 173, 566, 173); c.arw(724, 173, 760, 173); c.arw(918, 173, 958, 173)
c.arw(900, 206, 962, 274, "#b45309", dashed=True)
c.txt(680, 232, "Internet intermitente", 10, "#b45309")

# ═══ 2. PD-7 ═══
c.txt(20, 250,
"2. El nodo no baja apenas ve señal.\n"
"   Primero mira si conviene: red, horario\n"
"   de clase y energía. La clase tiene\n"
"   prioridad sobre la sincronización,\n"
"   siempre.", 12, BODY)
bloque(248, 118, "BLOQUE D  ·  ¿Conviene sincronizar ahora?  ·  PD-7  ·  5 casos", LOGIC)
c.box(392, 276, 150, 50, DB, "¿Hay señal?", None, 12)
c.box(558, 276, 150, 50, DB, "¿Hay clase?", None, 12)
c.box(724, 276, 150, 50, DB, "¿Hay energía?", None, 12)
c.box(898, 276, 192, 50, LOGIC, "Planificador de ventana", None, 12)
c.arw(874, 301, 898, 301)
c.txt(392, 334, "SIN SEÑAL  ·  VENTANA IDEAL  ·  SIN ENERGÍA  ·  HAY CLASE  ·  CLASE Y POCA ENERGÍA", 10, MUTE)
c.arw(650, 368, 650, 386)

# ═══ 3. PD-1 + PD-4 ═══
c.txt(20, 390,
"3. Baja el manifiesto remoto, que pesa\n"
"   unos KB, y lo cruza con el local. De\n"
"   ahí salen cuatro casos y ninguno más.\n"
"\n"
"   Si la escuela se atrasó varias semanas\n"
"   no hay nada especial que hacer: el\n"
"   manifiesto describe el estado completo,\n"
"   así que se compara contra el más nuevo\n"
"   y ya está.", 12, BODY)
bloque(386, 180, "BLOQUE A  ·  ¿Qué archivos bajo?  ·  PD-1 + PD-4  ·  9 casos", ACTOR)
c.dbox(392, 412, 140, 74, "Manifiesto\nlocal")
c.dbox(566, 412, 140, 74, "Manifiesto\nremoto")
c.box(750, 420, 190, 58, LOGIC, "Comparador", None, 14)
c.arw(532, 449, 566, 449)
c.arw(706, 449, 750, 449)
chips = [(392, ACTOR, "NUEVO"), (538, WARN, "EDITADO"), (684, OK, "SIN CAMBIO"), (830, BAD, "RETIRADO")]
for x, col, t in chips:
    c.box(x, 500, 136, 40, col, t, None, 12)
c.arw(845, 478, 700, 500)
c.txt(980, 500, "el manifiesto\nes de estado\ncompleto, no\nun delta", 10, BODY)
c.arw(650, 550, 650, 586)

# ═══ 4. PD-8 ═══
c.txt(20, 588,
"4. Antes de escribir un byte revisa el\n"
"   disco. La activación atómica necesita\n"
"   la versión activa y la nueva al mismo\n"
"   tiempo: mínimo 8 GB por nodo. Si no\n"
"   cabe, libera lo que Lima puede\n"
"   reenviar, nunca la cola.", 12, BODY)
bloque(586, 118, "BLOQUE D  ·  ¿Me cabe en el disco?  ·  PD-8  ·  4 casos", LOGIC)
c.box(392, 614, 178, 50, LOGIC, "Control de espacio", None, 12)
c.txt(600, 614,
"ESPACIO SUFICIENTE   descargar\n"
"LIBERAR Y SEGUIR     borrar antiguas\n"
"DISCO LLENO          solo lo esencial\n"
"DISCO LLENO + COLA   enviar la cola primero", 10, BODY, fam=3)
c.txt(392, 672, "nunca se borra la versión activa, la cola de eventos ni el índice de bloques", 10, MUTE)
c.arw(650, 704, 650, 724)

# ═══ 5. DESCARGA ═══
c.txt(20, 726,
"5. Descarga por bloques con HTTP Range. Si\n"
"   se corta la red guarda el índice, y al\n"
"   volver pide solo los rangos que faltan.", 12, BODY)
bloque(724, 96, "TRANSFERENCIA")
c.box(392, 750, 190, 56, SERV, "Gestor de descargas", "bloques reanudables", 13, 9)
c.dbox(620, 742, 148, 72, "Índice de\nbloques", "persistente")
c.arw(582, 778, 620, 778)
c.txt(800, 758, "si la red se cae la transferencia queda PAUSED,\nno se reinicia desde cero", 10, BODY)
c.arw(650, 820, 650, 840)

# ═══ 6. PD-2 ═══
c.txt(20, 842,
"6. Con los archivos abajo mira tres cosas:\n"
"   hash, firma y si hay versión anterior.\n"
"   Tres preguntas de sí o no dan ocho\n"
"   combinaciones, y están las ocho.\n"
"   Solo dos activan.", 12, BODY)
bloque(840, 132, "BLOQUE B  ·  ¿Puedo confiar en lo que llegó?  ·  PD-2  ·  8 casos", SERV)
c.box(392, 868, 150, 48, DB, "Hash", None, 12)
c.box(558, 868, 150, 48, DB, "Firma", None, 12)
c.box(724, 868, 168, 48, DB, "¿Hay respaldo?", None, 12)
c.box(916, 868, 174, 48, LOGIC, "Validador", None, 13)
c.arw(892, 892, 916, 892)
c.txt(392, 926,
"con respaldo    OK  ·  firma inválida  ·  archivo corrupto  ·  paquete no confiable\n"
"sin respaldo    OK primera carga  ·  las otras tres rechazan y alertan a Lima", 10, BODY, fam=3)
c.arw(650, 972, 650, 992)

# ═══ 7. PD-5 ═══
c.txt(20, 994,
"7. Activar no es copiar encima. Es mover\n"
"   un puntero, que es una sola operación.\n"
"   Si se corta la luz quedó antes o\n"
"   después, nunca en medio.", 12, BODY)
bloque(992, 132, "BLOQUE B  ·  ¿Se activó bien?  ·  PD-5  ·  3 casos", SERV)
c.box(392, 1018, 158, 46, ZONE, "/cache/s11/", None, 12)
c.box(392, 1072, 158, 46, ZONE, "/cache/s12/", None, 12)
c.box(580, 1044, 130, 46, LOGIC, "ACTIVE", None, 13)
c.arw(580, 1052, 550, 1041, MUTE, dashed=True)
c.arw(580, 1082, 550, 1094, OK)
c.txt(740, 1016,
"1. descargar   2. verificar   3. mover el puntero   4. borrar lo viejo\n"
"\n"
"corte al descargar     reanudar desde el ultimo bloque\n"
"corte antes de activar mover el puntero, es idempotente\n"
"corte tras activar     nada, ya esta", 10, BODY, fam=3)
c.arw(650, 1124, 650, 1144)

# ═══ 8. LA CLASE ═══
c.txt(20, 1146,
"8. Rosa enseña y Diego estudia contra la\n"
"   caché local, por WiFi. En ese momento\n"
"   no hace falta Internet: para eso se\n"
"   hizo todo lo anterior.", 12, BODY)
bloque(1144, 104, "LA CLASE OCURRE SIN RED", OK)
c.dbox(392, 1166, 140, 74, "Caché local", "versión activa")
c.box(600, 1174, 140, 58, ACTOR, "Rosa", "enseña", 14, 9)
c.box(770, 1174, 140, 58, ACTOR, "Diego", "estudia", 14, 9)
c.arw(532, 1203, 600, 1203, OK)
c.txt(548, 1184, "WiFi", 9, MUTE)
c.arw(740, 1203, 770, 1203)
c.txt(940, 1180, "aquí no hay\nInternet, y no\nhace falta", 10, OK)
c.arw(650, 1248, 650, 1268)

# ═══ 9. PD-3 + PD-6 ═══
c.txt(20, 1270,
"9. Lo que hicieron sin red queda en una\n"
"   cola. Cuando vuelve la señal sale hacia\n"
"   Lima con un identificador que se\n"
"   congeló al crearse.\n"
"\n"
"   Si el envío se reintenta, Lima lo\n"
"   reconoce y no lo procesa dos veces.", 12, BODY)
bloque(1268, 150, "BLOQUE C  ·  El retorno vuelve una sola vez  ·  PD-3 + PD-6  ·  7 casos", DB)
c.dbox(392, 1294, 148, 78, "Cola local", "outbox_events")
c.box(588, 1300, 210, 56, LOGIC, "¿Ya tengo este id?", None, 13)
c.arw(540, 1333, 588, 1330)
c.txt(824, 1290,
"event_id = school_id + seq + hash(contenido)\n"
"se congela al CREAR, nunca al enviar\n"
"\n"
"evento nuevo     procesar y guardar el id\n"
"reintento        no reprocesar, responder OK\n"
"duplicado real   registrar como anomalia", 10, BODY, fam=3)
c.txt(392, 1382, "created_at lo pone el nodo  ·  received_at lo pone Lima y ordena la auditoría", 10, BODY)
c.arw(650, 1418, 650, 1438)

# ═══ 10. CIERRE ═══
c.txt(20, 1440,
"10. Valeria ve el avance de cada escuela y\n"
"    cuántas semanas de atraso lleva cada\n"
"    una. El círculo se cierra.", 12, BODY)
bloque(1438, 96, "LIMA  ·  EL CÍRCULO SE CIERRA")
c.box(392, 1464, 190, 52, SERV, "Panel de Valeria", None, 13)
c.dbox(620, 1456, 148, 70, "sync_events", "auditoría")
c.arw(582, 1490, 620, 1491)
c.txt(800, 1470, "semanas de atraso por escuela, versiones READY, bytes reanudados", 10, BODY)

# ═══ TABLA RESUMEN ═══
c.line(10, 1560, 1210, 1560)
c.txt(20, 1580, "Los 36 casos", 18, INK)
c.txt(372, 1580,
"PD    PREGUNTA                                   CASOS  DIAGRAMA\n"
"PD-1  Que archivos transferir                       4       A\n"
"PD-2  El archivo llego bien                         8       B\n"
"PD-3  Este evento ya lo procese                     3       C\n"
"PD-4  La escuela salto varias versiones             5       D\n"
"PD-5  Se corta la luz durante la activacion         3       B\n"
"PD-6  El reloj del nodo esta desincronizado         4       C\n"
"PD-7  Sincronizar ahora o esperar                   5       D\n"
"PD-8  El disco del nodo se lleno                    4       D\n"
"                                            TOTAL  36", 11, BODY, fam=3)

c.txt(20, 1620,
"Cada bloque se abre en\n"
"su propio lienzo, con el\n"
"guion completo y las\n"
"tres iteraciones:\n"
"\n"
"A-que-bajar\n"
"B-integridad-y-activacion\n"
"C-retorno-idempotente\n"
"D-cuando-sincronizar", 11, MUTE)

c.txt(372, 1780, "Los 24 peores casos que ataja el Problema 1", 14, INK)
c.txt(372, 1812,
"P1   la ventana de conexion no alcanza\n"
"P2   se pierde el indice de bloques\n"
"P3   activacion parcial de la version\n"
"P4   firma o hash invalido sin respaldo\n"
"P5   RETIRADO olvidado en la cache\n"
"P6   el timestamp se toma al enviar\n"
"P7   Lima aplica pero no guarda el id\n"
"P8   la cola crece sin limite\n"
"P9   colision de hash\n"
"P10  se asume conexion durante la clase\n"
"P11  manifiesto como delta encadenado\n"
"P12  el manifiesto describe solo su semana", 10, BODY, fam=3)
c.txt(760, 1812,
"P13  descargar las versiones en orden\n"
"P14  atraso permanente invisible\n"
"P15  activar copiando archivos encima\n"
"P16  mover el puntero antes de verificar\n"
"P17  borrar la anterior antes de activar\n"
"P18  salto de reloj por NTP\n"
"P19  ordenar la auditoria por hora del nodo\n"
"P20  sincronizar sin limite durante la clase\n"
"P21  todas las escuelas a la misma hora\n"
"P22  borrar la cola para liberar espacio\n"
"P23  nodo dimensionado a 4 GB\n"
"P24  disco al 100%: falla silenciosa", 10, BODY, fam=3)

n = c.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "E-problema1-completo.excalidraw"))
print("E:", n, "elementos")
