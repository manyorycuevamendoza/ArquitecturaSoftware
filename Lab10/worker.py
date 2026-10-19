"""Worker = una instancia de un servicio simulado.

El worker i atiende el servicio S(i): toma partes de su cola `q:i`, "trabaja" (sleep con
latencia artificial) y registra un checkpoint en Redis por cada parte terminada.

Latencias artificiales:
  * normal: cada parte tarda CHUNK_MS (1-2.5 ms) -> el servicio completo ~10-25 ms
  * lento:  si el plan de la ronda marca a este servidor como lento, a partir de la parte
            número `onset` cada parte tarda SLOW_CHUNK_MS (120-150 ms) -> hasta ~1.5 s.
            La lentitud es del SERVIDOR (GC, CPU throttling...), no de la petición:
            si otro worker toma esas partes, las hace a velocidad normal.

Modos:
  baseline  solo procesa su propia cola.
  stealing  procesa su cola; si está ocioso, roba partes de la cola más larga o partes con lease vencido.

Uso: python worker.py --id 3 --mode stealing [--redis-url redis://localhost:6379/0]
"""
import argparse
import random
import time

import redis

import config as C
import redis_scripts as S


class Worker:
    def __init__(self, wid, mode, url):
        self.wid, self.mode = wid, mode
        self.r = redis.Redis.from_url(url, decode_responses=True)
        self.rng = random.Random(C.SEED * 1000 + wid)
        self.own = f"q:{wid}"
        self.others = [f"q:{i}" for i in range(C.N_SERVICES) if i != wid]
        self.pop_own = self.r.register_script(S.POP_OWN)
        self.steal = self.r.register_script(S.STEAL)
        self.record_s = self.r.register_script(S.RECORD)
        self.lease_s = C.LEASE_MS / 1000 if mode == "stealing" else 0
        self.done_in_round = {}   # ronda -> partes procesadas por este worker (para el onset)
        self.onset = {}           # ronda -> parte desde la que este servidor está lento (o None)

    # ---------- latencia artificial ----------
    def chunk_duration(self, rnd):
        if rnd not in self.onset:
            v = self.r.hget(f"plan:{rnd}", self.wid)
            self.onset = {k: o for k, o in self.onset.items() if k > rnd - 5}   # limpiar memoria
            self.onset[rnd] = int(v) if v is not None else None
            self.done_in_round = {rnd: 0}
        n = self.done_in_round.get(rnd, 0)
        self.done_in_round[rnd] = n + 1
        onset = self.onset[rnd]
        lo, hi = C.SLOW_CHUNK_MS if (onset is not None and n >= onset) else C.CHUNK_MS
        return self.rng.uniform(lo, hi) / 1000

    def work_and_record(self, chunk_id):
        rnd, svc, _ = chunk_id.split(":")
        time.sleep(self.chunk_duration(int(rnd)))           # <- "trabajo" simulado
        self.record_s(keys=[f"done:{rnd}", f"cnts:{rnd}", f"cnt:{rnd}", f"fin:{rnd}"],
                      args=[chunk_id, svc, C.N_SERVICES * C.CHUNKS])

    # ---------- bucle principal ----------
    def run(self):
        idle = C.IDLE_SLEEP_MS / 1000
        while True:
            if self.mode == "baseline":
                item = self.r.blpop(self.own, timeout=1)       # espera bloqueante en su cola
                if item:
                    self.r.incr("busy")
                    self.work_and_record(item[1])
                continue

            now = time.time()
            item = self.pop_own(keys=[self.own], args=[now, self.lease_s])
            if item:
                self.work_and_record(item)
                continue

            item = self.steal(keys=self.others, args=[now, self.lease_s])   # ocioso -> robar
            if item:
                self.work_and_record(item)
                continue
            time.sleep(idle)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=int, required=True)
    ap.add_argument("--mode", choices=["baseline", "stealing"], required=True)
    ap.add_argument("--redis-url", default="redis://localhost:6379/0")
    a = ap.parse_args()
    Worker(a.id, a.mode, a.redis_url).run()
