"""Corre el experimento completo: baseline vs. work stealing (propuesta).

Uso:
    python run_experiment.py                       # 1000 rondas por modo (~5 min)
    python run_experiment.py --rounds 200          # prueba rápida

Requiere un Redis en --redis-url (por defecto localhost:6379). Si no hay uno corriendo y
`redis-server` está instalado, el script levanta uno temporal en el puerto 6390.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np
import redis

import config as C
import gateway

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
LABEL = {"baseline": "Baseline", "stealing": "Work stealing (propuesta)"}


def ensure_redis(url):
    try:
        redis.Redis.from_url(url).ping()
        return url, None
    except redis.ConnectionError:
        if not shutil.which("redis-server"):
            sys.exit(f"No hay Redis en {url}. Levántalo con:  docker compose up -d")
        proc = subprocess.Popen(["redis-server", "--port", "6390", "--save", "", "--appendonly", "no"],
                                stdout=subprocess.DEVNULL)
        url = "redis://localhost:6390/0"
        for _ in range(50):
            try:
                redis.Redis.from_url(url).ping()
                print("Redis temporal levantado en el puerto 6390")
                return url, proc
            except redis.ConnectionError:
                time.sleep(0.1)
        sys.exit("No se pudo levantar redis-server")


def run_mode(mode, url, rounds, warmup):
    r = redis.Redis.from_url(url, decode_responses=True)
    r.flushdb()
    workers = [subprocess.Popen([sys.executable, os.path.join(HERE, "worker.py"),
                                 "--id", str(i), "--mode", mode, "--redis-url", url])
               for i in range(C.N_SERVICES)]
    time.sleep(1.0)                                          # dar tiempo a que arranquen
    try:
        t = time.time()
        rows = gateway.run(mode, url, rounds, warmup)
        wall = time.time() - t
    finally:
        for w in workers:
            w.terminate()
        for w in workers:
            w.wait()
    stats = {k.split(":")[1]: int(v) for k, v in
             ((k, r.get(k)) for k in r.keys("stat:*"))}
    return rows, stats, wall


def summarize(mode, rows, stats, rounds, warmup):
    lat = np.array([x[1] for x in rows])
    useful = (rounds + warmup) * C.N_SERVICES * C.CHUNKS
    executed = stats.get("executed", 0)
    return {
        "modo": LABEL[mode],
        "rondas": rounds,
        "rondas_con_servidor_lento": int(sum(1 for x in rows if x[2] > 0)),
        "p50_ms": round(float(np.percentile(lat, 50)), 1),
        "p95_ms": round(float(np.percentile(lat, 95)), 1),
        "p99_ms": round(float(np.percentile(lat, 99)), 1),
        "p99_9_ms": round(float(np.percentile(lat, 99.9)), 1),
        "max_ms": round(float(lat.max()), 1),
        "promedio_ms": round(float(lat.mean()), 1),
        "subpeticiones_ejecutadas": executed,
        "subpeticiones_utiles": useful,
        "overhead_pct": round(100 * (executed - useful) / useful, 2),
        "duplicadas": stats.get("dup", 0),
        "robos": stats.get("stolen", 0),
        "leases_vencidos": stats.get("lease", 0),
    }


def write_outputs(results, all_rows):
    os.makedirs(OUT, exist_ok=True)
    for mode, rows in all_rows.items():
        with open(os.path.join(OUT, f"latencias_{mode}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ronda", "latencia_ms", "servidores_lentos"])
            w.writerows([(a, round(b, 3), c) for a, b, c in rows])
    with open(os.path.join(OUT, "resumen.json"), "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    cols = [r["modo"] for r in results]
    lines = ["| Métrica | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    def row(name, key, fmt="{}"):
        lines.append(f"| {name} | " + " | ".join(fmt.format(r[key]) for r in results) + " |")
    row("p50", "p50_ms", "{} ms"); row("p95", "p95_ms", "{} ms"); row("p99", "p99_ms", "{} ms")
    row("p99.9", "p99_9_ms", "{} ms"); row("máximo", "max_ms", "{} ms"); row("promedio", "promedio_ms", "{} ms")
    row("Requests ejecutadas (peticiones del cliente)", "rondas")
    row("Rondas con algún servidor lento", "rondas_con_servidor_lento")
    row("Sub-peticiones ejecutadas (partes)", "subpeticiones_ejecutadas")
    row("Overhead (trabajo extra)", "overhead_pct", "{} %")
    row("Partes duplicadas (desperdicio)", "duplicadas")
    row("Robos de trabajo", "robos"); row("Leases vencidos", "leases_vencidos")
    table = "\n".join(lines)
    with open(os.path.join(OUT, "resumen.md"), "w") as f:
        f.write(f"# Resultados del experimento\n\nParámetros: {C.N_SERVICES} servicios x {C.CHUNKS} partes, "
                f"P(servidor lento)={C.P_SLOW}, parte normal={C.CHUNK_MS} ms, parte lenta={C.SLOW_CHUNK_MS} ms, "
                f"lease={C.LEASE_MS} ms, semilla={C.SEED}.\n\n{table}\n")
    print("\n" + table)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        colors = {"baseline": "#868e96", "stealing": "#1971c2"}
        fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
        for mode, rows in all_rows.items():
            lat = np.sort([x[1] for x in rows])
            y = np.arange(1, len(lat) + 1) / len(lat)
            axes[0].plot(lat, y, label=LABEL[mode], color=colors[mode], lw=2)
        axes[0].set_xscale("log"); axes[0].set_xlabel("latencia por petición (ms, escala log)")
        axes[0].set_ylabel("fracción de peticiones"); axes[0].set_title("Distribución acumulada (CDF)")
        axes[0].grid(alpha=.3, which="both"); axes[0].legend()
        pcts = ["p50_ms", "p95_ms", "p99_ms"]
        x = np.arange(len(pcts)); wbar = 0.8 / len(results)
        for k, (mode, res) in enumerate(zip(all_rows, results)):
            vals = [res[p] for p in pcts]
            bars = axes[1].bar(x + k * wbar, vals, wbar, label=res["modo"], color=colors[mode])
            axes[1].bar_label(bars, fmt="%.0f", fontsize=8)
        axes[1].set_xticks(x + wbar * (len(results) - 1) / 2, ["p50", "p95", "p99"])
        axes[1].set_yscale("log"); axes[1].set_ylabel("ms (escala log)")
        axes[1].set_title("Percentiles"); axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False); axes[1].grid(alpha=.3, axis="y")
        fig.tight_layout(); fig.savefig(os.path.join(OUT, "comparacion.png"), dpi=140)
        print(f"Gráfico: {os.path.join(OUT, 'comparacion.png')}")
    except ImportError:
        print("(matplotlib no instalado: se omite el gráfico)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=C.ROUNDS)
    ap.add_argument("--warmup", type=int, default=C.WARMUP)
    ap.add_argument("--modes", default="baseline,stealing")
    ap.add_argument("--redis-url", default="redis://localhost:6379/0")
    a = ap.parse_args()
    url, proc = ensure_redis(a.redis_url)
    results, all_rows = [], {}
    try:
        for mode in a.modes.split(","):
            print(f"\n=== {LABEL[mode]} ===", flush=True)
            rows, stats, wall = run_mode(mode, url, a.rounds, a.warmup)
            all_rows[mode] = rows
            results.append(summarize(mode, rows, stats, a.rounds, a.warmup))
            print(f"  terminado en {wall:.0f}s", flush=True)
        write_outputs(results, all_rows)
    finally:
        if proc:
            proc.terminate()


if __name__ == "__main__":
    main()
