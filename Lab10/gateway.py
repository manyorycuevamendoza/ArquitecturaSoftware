"""API Gateway: simula al cliente enviando peticiones y mide la latencia de cada una.

Cada "ronda" es UNA petición del cliente:
  1. se sortea qué servidores estarán lentos (mismo plan para todos los modos gracias a SEED);
  2. se encola el trabajo de los 10 servicios (10 partes cada uno) de forma atómica;
  3. se espera a que las 100 partes estén terminadas  -> latencia percibida por el usuario;
  4. se cancela el trabajo sobrante y se espera a que todos los workers queden libres,
     para que la siguiente ronda empiece sin cola previa (supuesto del diseño).
"""
import random
import time

import redis

import config as C


def run(mode, url, rounds=C.ROUNDS, warmup=C.WARMUP, progress=True):
    r = redis.Redis.from_url(url, decode_responses=True)
    plan_rng = random.Random(C.SEED)
    total = C.N_SERVICES * C.CHUNKS
    rows = []          # (ronda, latencia_ms, servidores_lentos)

    for i in range(warmup + rounds):
        plan = {s: plan_rng.randrange(C.CHUNKS) for s in range(C.N_SERVICES)
                if plan_rng.random() < C.P_SLOW}

        p = r.pipeline(transaction=True)
        if plan:
            p.hset(f"plan:{i}", mapping=plan)
        for s in range(C.N_SERVICES):
            p.rpush(f"q:{s}", *[f"{i}:{s}:{k}" for k in range(C.CHUNKS)])
        t0 = time.perf_counter()
        p.execute()                                        # fan-out de los 10 servicios

        if r.blpop(f"fin:{i}", timeout=C.ROUND_TIMEOUT_S) is None:
            raise RuntimeError(f"ronda {i} no terminó en {C.ROUND_TIMEOUT_S}s (¿workers caídos?)")
        lat_ms = (time.perf_counter() - t0) * 1000

        # limpiar trabajo sobrante y esperar a que todos los workers terminen
        p = r.pipeline()
        p.delete(*[f"q:{s}" for s in range(C.N_SERVICES)])
        p.execute()
        while int(r.get("busy") or 0) > 0:
            time.sleep(0.001)
        r.delete(f"plan:{i}", f"done:{i}", f"cnts:{i}", f"cnt:{i}", f"fin:{i}", "inflight")

        if i >= warmup:
            rows.append((i - warmup, lat_ms, len(plan)))
        if progress and i >= warmup and (i + 1 - warmup) % 100 == 0:
            print(f"  [{mode}] {i + 1 - warmup}/{rounds} rondas", flush=True)
    return rows
