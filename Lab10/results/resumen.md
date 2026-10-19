# Resultados del experimento

Parámetros: 10 servicios x 10 partes, P(servidor lento)=0.03, parte normal=(1.0, 2.5) ms, parte lenta=(120.0, 150.0) ms, lease=8.0 ms, semilla=42.

| Métrica | Baseline | Work stealing (propuesta) |
|---|---|---|
| p50 | 33.2 ms | 29.4 ms |
| p95 | 1228.3 ms | 33.5 ms |
| p99 | 1383.8 ms | 36.0 ms |
| p99.9 | 1409.4 ms | 37.5 ms |
| máximo | 1415.5 ms | 38.0 ms |
| promedio | 227.6 ms | 29.9 ms |
| Requests ejecutadas (peticiones del cliente) | 1000 | 1000 |
| Rondas con algún servidor lento | 259 | 259 |
| Sub-peticiones ejecutadas (partes) | 102000 | 102286 |
| Overhead (trabajo extra) | 0.0 % | 0.28 % |
| Partes duplicadas (desperdicio) | 0 | 286 |
| Robos de trabajo | 0 | 5404 |
| Leases vencidos | 0 | 286 |
