# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *

c = Canvas()
titulo(c, "C. Lo que se hizo sin red vuelve una sola vez",
       "PD-3 + PD-6. Siete casos. Protege los datos que solo existen en la escuela.")

# ══════════ ITERACIÓN 1 ══════════
y = c.header(20, 108, 1, "El riesgo del reintento", None)
c.txt(20, y,
"1. Diego termina una actividad un martes.\n"
"   No hay Internet.\n"
"\n"
"2. El avance se guarda en una cola local,\n"
"   dentro del nodo.\n"
"\n"
"3. El jueves vuelve la señal y la cola\n"
"   sale hacia Lima.\n"
"\n"
"4. Si el envío se corta a mitad de camino,\n"
"   el nodo reintenta. Ahí está el riesgo:\n"
"   que el mismo avance quede registrado\n"
"   dos veces.\n"
"\n"
"5. El avance de Diego no existe en ningún\n"
"   otro lado del mundo.", 12, BODY)

c.box(390, 192, 145, 64, ACTOR, "Diego", "termina una actividad", 14)
c.dbox(590, 182, 158, 88, "Cola local", ("outbox_events", "PENDING_SYNC"))
c.box(980, 192, 178, 64, SERV, "API de Lima", "recibe la cola", 14)
c.arw(535, 224, 590, 224)
c.arw(748, 224, 980, 224)
c.txt(790, 200, "cuando vuelve la red", 10, MUTE)
c.arw(1000, 262, 750, 288, WARN, dashed=True)
c.txt(760, 288, "si no llega la confirmación, el nodo reintenta", 10, WARN)

c.line(10, 424, 1200, 424)

# ══════════ ITERACIÓN 2 ══════════
y = c.header(20, 444, 2, "El identificador que no cambia nunca", None)
c.txt(20, y,
"6. Cada evento nace con un identificador\n"
"   propio y ya no lo cambia nunca.\n"
"\n"
"7. El identificador junta tres cosas: qué\n"
"   escuela, un contador local que solo\n"
"   sube, y el hash del contenido.\n"
"\n"
"8. Se arma al crear el evento, no al\n"
"   enviarlo. Esa es la diferencia que\n"
"   sostiene todo lo demás.\n"
"\n"
"9. Cuando llega a Lima la pregunta es una\n"
"   sola: ¿ya tengo un evento con este\n"
"   identificador?\n"
"\n"
"10. Si no lo tengo, lo proceso y lo\n"
"    guardo. Si ya lo tengo, respondo OK\n"
"    otra vez y no lo vuelvo a procesar.\n"
"\n"
"11. Lima aplica el evento y guarda el\n"
"    identificador en la misma\n"
"    transacción. Si guardara después y se\n"
"    cayera en el medio, el reintento lo\n"
"    duplicaría igual.", 12, BODY)

c.zona(350, 496, 840, 366, "IDEMPOTENCIA DEL RETORNO  ·  PD-3")

c.txt(378, 522,
"event_id  =  school_id  +  seq  +  hash(contenido)\n"
"\n"
"PE-AYA-041   -   0417   -   1f045c4e79d4\n"
"  escuela      contador      hash del\n"
"                local        contenido\n"
"\n"
"se arma al CREAR el evento, no al enviarlo", 10, BODY, fam=3)

c.box(760, 540, 240, 60, LOGIC, "¿Ya tengo este event_id?", None, 13)
c.dbox(1030, 532, 140, 78, "sync_events", "event_id (PK)")
c.arw(1000, 570, 1030, 571)
c.arw(880, 600, 880, 640)

casos3 = [
    (372, OK,   "Evento nuevo",   "no tengo ese event_id",       "procesar y guardar el id\nen la misma transacción"),
    (632, WARN, "Reintento",      "ya lo tengo, no confirmó",    "no reprocesar,\nresponder OK otra vez"),
    (892, BAD,  "Duplicado real", "ya lo tengo y ya confirmó",   "no reprocesar,\nregistrar como anomalía"),
]
for x, col, t, comb, acc in casos3:
    c.box(x, 648, 240, 88, col, t, (comb, acc), 13, 9)
    c.arw(880, 640, x + 120, 648)

c.txt(372, 752,
"Aplicar el evento y guardar el event_id ocurren en la misma transacción. Si Lima aplicara primero y\n"
"guardara después, un corte en el medio haría que el reintento lo procesara otra vez.", 10, BODY)

c.txt(372, 800,
"Nominalmente 2 x 3 = 6 filas. Cuando no tengo el event_id la segunda variable no aplica:\n"
"esas filas colapsan en una sola. Quedan 3 casos.", 10, MUTE)

c.line(10, 880, 1200, 880)

# ══════════ ITERACIÓN 3 ══════════
y = c.header(20, 900, 3, "El reloj del nodo puede mentir", None)
c.txt(20, y,
"12. El nodo puede tener el reloj mal. Un\n"
"    corte largo de energía y arranca en\n"
"    una fecha por defecto.\n"
"\n"
"13. Eso no rompe la idempotencia, porque\n"
"    el identificador ya se congeló cuando\n"
"    se creó el evento.\n"
"\n"
"14. Lo que sí rompe es la auditoría: el\n"
"    orden de los eventos deja de ser\n"
"    confiable.\n"
"\n"
"15. Por eso se guardan dos tiempos\n"
"    distintos. created_at lo pone el nodo\n"
"    y cuenta cuándo pasó en la escuela.\n"
"    received_at lo pone Lima y sirve para\n"
"    ordenar.\n"
"\n"
"16. Los reportes ordenan por received_at,\n"
"    nunca por la hora del nodo.\n"
"\n"
"17. Si el timestamp se tomara al enviar,\n"
"    cada reintento generaría un\n"
"    identificador distinto y el duplicado\n"
"    se colaría. Por eso el contador local\n"
"    reemplaza al reloj dentro del id.", 12, BODY)

c.zona(350, 976, 840, 380, "DOS RELOJES, DOS TRABAJOS  ·  PD-6")

c.box(390, 1008, 210, 74, ACTOR, "created_at", ("lo pone el nodo", "cuándo pasó en la escuela"), 14, 9)
c.box(630, 1008, 210, 74, SERV, "received_at", ("lo pone Lima", "ordena la auditoría"), 14, 9)
c.txt(872, 1014,
"los reportes ordenan\n"
"por received_at,\n"
"nunca por created_at", 10, BODY, fam=3)

c.txt(500, 1112, "PRIMER ENVÍO", 10, MUTE, "center", 240, fam=3)
c.txt(760, 1112, "REINTENTO", 10, MUTE, "center", 240, fam=3)

c.txt(372, 1160, "reloj\nsincronizado", 10, OK, "center", 118)
c.box(500, 1136, 240, 76, OK, "Normal", "ningún riesgo", 13, 9)
c.box(760, 1136, 240, 76, OK, "Reintento limpio", "mismo event_id, se ignora", 13, 9)

c.txt(372, 1252, "reloj\ndesviado", 10, WARN, "center", 118)
c.box(500, 1228, 240, 76, WARN, "Reloj desviado", "la hora queda mal en la auditoría", 13, 9)
c.box(760, 1228, 240, 76, WARN, "Desviado en reintento", "el id no cambia: se congeló al crear", 13, 9)

c.txt(1020, 1150,
"El reloj desviado\n"
"nunca rompe la\n"
"idempotencia.\n"
"Solo ensucia la\n"
"auditoría, y para\n"
"eso está el\n"
"received_at.", 10, BODY)

# leyenda
c.rect(372, 1380, 450, 118, MUTE, rough=0, sw=1)
c.txt(386, 1390, "PEORES CASOS QUE ATAJA ESTE DIAGRAMA", 11, INK)
c.txt(386, 1412,
"P6   el timestamp se toma al enviar y no al crear\n"
"P7   Lima aplica el evento pero no guarda el event_id\n"
"P8   la cola crece sin límite hasta llenar el disco\n"
"P18  salto de reloj por NTP entre crear y reenviar\n"
"P19  ordenar la auditoría por la hora del nodo\n"
"P22  borrar la cola para liberar espacio", 10, BODY)

n = c.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "C-retorno-idempotente.excalidraw"))
print("C:", n, "elementos")
