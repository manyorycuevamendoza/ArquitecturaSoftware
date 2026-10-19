# Lab 10 · A tale of Tails — PoC

Simula una API que consulta **10 servicios en paralelo** y compara dos estrategias:

| Modo | Qué hace |
|---|---|
| `baseline` | Cada servicio hace su trabajo; la API espera al más lento. |
| `stealing` (propuesta) | El trabajo de cada servicio se divide en 10 partes (checkpoints) en Redis. Los workers que terminan **roban** las partes pendientes de los lentos. Si una parte no termina en 8 ms (lease), otro worker la toma. |

## Cómo se simula (punto 2 del lab)

- **10 servicios simulados**: 10 procesos `worker.py`, uno por servicio (procesos separados para evitar el GIL).
- **Latencias artificiales**: cada parte del trabajo es un `sleep` de 1–2.5 ms, así que un servicio normal tarda ~10–25 ms.
- **Servicios lentos ocasionales**: en cada ronda, cada servidor tiene un 3% de probabilidad de ponerse lento (GC, CPU throttling). Desde una parte al azar en adelante, cada parte tarda 120–150 ms, y el servicio completo hasta ~1.5 s.
- **Mismo escenario para todos**: los servidores lentos se sortean con una semilla fija, así que ambos modos enfrentan exactamente las mismas rondas lentas.
- **Una ronda a la vez**: antes de cada ronda todos los workers están libres (supuesto de "sin cola previa").

Todos los parámetros están en `config.py`.

## Cómo correrlo

```bash
pip install -r requirements.txt
docker compose up -d                 # Redis en localhost:6379 (o usa un redis-server local)
python run_experiment.py             # 1000 rondas por modo, ~5 min
python run_experiment.py --rounds 200            # prueba rápida
```

Si no hay Redis en `localhost:6379` pero `redis-server` está instalado, el script levanta uno temporal.

Salidas en `results/`:
- `resumen.md`: tabla p50 / p95 / p99 / requests ejecutadas
- `comparacion.png`: CDF y percentiles
- `latencias_<modo>.csv`: latencia de cada petición
- `resumen.json`: los mismos datos en JSON

## Archivos

| Archivo | Rol |
|---|---|
| `config.py` | Parámetros del experimento |
| `worker.py` | Servicio simulado (latencias artificiales + lógica de robo) |
| `redis_scripts.py` | Operaciones atómicas en Redis (tomar parte, robar, registrar checkpoint) |
| `gateway.py` | API: lanza cada petición, mide su latencia y limpia el trabajo sobrante |
| `run_experiment.py` | Levanta los workers por modo, corre todo y genera tabla y gráfico |

## Limitaciones a declarar

- Todo corre en una sola máquina: no hay latencia de red real entre servicios.
- El "trabajo" es un `sleep`. Mide espera, no cómputo, lo cual es válido para tail latency causada por servidores lentos.
- Supone que el trabajo se puede dividir en partes y que cualquier worker puede ejecutar partes de cualquier servicio.
- Las rondas son secuenciales (un cliente). Con muchos usuarios concurrentes no habría workers ociosos y el beneficio sería menor.
