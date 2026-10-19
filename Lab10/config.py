"""Parámetros del experimento (Lab 10 - A tale of Tails).

Todos los tiempos están en milisegundos salvo que se indique lo contrario.
"""

N_SERVICES = 10            # servicios consultados en paralelo por cada petición del cliente
CHUNKS = 10                # partes (checkpoints) en que se divide el trabajo de cada servicio

# Latencias artificiales
CHUNK_MS = (1.0, 2.5)      # duración normal de una parte -> un servicio normal tarda ~10-25 ms
SLOW_CHUNK_MS = (120.0, 150.0)  # duración de una parte cuando el servidor está lento -> hasta ~1.5 s
P_SLOW = 0.03              # probabilidad de que un servidor se ponga lento en una ronda
                           # (con 10 servicios: 1 - 0.97^10 ≈ 26% de las rondas tienen al menos uno lento)

# Mecanismo de mitigación (work stealing)
LEASE_MS = 8.0             # work stealing: si una parte no termina en 8 ms, otro worker puede tomarla
IDLE_SLEEP_MS = 0.5        # espera de un worker ocioso antes de volver a buscar trabajo

# Experimento
ROUNDS = 1000              # peticiones del cliente medidas por modo
WARMUP = 20                # rondas iniciales descartadas
SEED = 42                  # misma semilla => ambos modos sufren exactamente los mismos servidores lentos
ROUND_TIMEOUT_S = 30
