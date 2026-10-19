"""Scripts Lua que se ejecutan de forma atómica dentro de Redis.

Cada operación de un worker es UN viaje de ida y vuelta a Redis, y como es atómica
no hay carreras entre workers (dos workers nunca toman la misma parte de la cola).
"""

# Tomar la siguiente parte de MI cola.  KEYS[1]=cola propia  ARGV[1]=ahora(s) ARGV[2]=lease(s, 0=sin lease)
POP_OWN = """
local v = redis.call('LPOP', KEYS[1])
if v then
  redis.call('INCR', 'busy')
  local lease = tonumber(ARGV[2])
  if lease > 0 then redis.call('ZADD', 'inflight', tonumber(ARGV[1]) + lease, v) end
end
return v
"""

# Robar trabajo: 1) de la cola con más partes pendientes (desde el final)
#                2) si no hay, tomar una parte cuyo lease venció (su worker está atascado)
# KEYS = colas de los otros servicios   ARGV[1]=ahora(s) ARGV[2]=lease(s)
STEAL = """
local now, lease = tonumber(ARGV[1]), tonumber(ARGV[2])
local best, blen = nil, 0
for _, k in ipairs(KEYS) do
  local l = redis.call('LLEN', k)
  if l > blen then best, blen = k, l end
end
if best then
  local v = redis.call('RPOP', best)
  redis.call('INCR', 'busy'); redis.call('INCR', 'stat:stolen')
  redis.call('ZADD', 'inflight', now + lease, v)
  return v
end
local exp = redis.call('ZRANGEBYSCORE', 'inflight', '-inf', now, 'LIMIT', 0, 1)
if #exp > 0 then
  redis.call('ZREM', 'inflight', exp[1])
  redis.call('INCR', 'busy'); redis.call('INCR', 'stat:lease')
  redis.call('ZADD', 'inflight', now + lease, exp[1])
  return exp[1]
end
return nil
"""

# Registrar una parte terminada (checkpoint).
# KEYS[1]=done:<ronda> KEYS[2]=cnts:<ronda> KEYS[3]=cnt:<ronda> KEYS[4]=fin:<ronda>
# ARGV[1]=id de la parte  ARGV[2]=servicio  ARGV[3]=total de partes
RECORD = """
redis.call('INCR', 'stat:executed')
redis.call('ZREM', 'inflight', ARGV[1])
redis.call('DECR', 'busy')
if redis.call('HSETNX', KEYS[1], ARGV[1], 1) == 0 then
  redis.call('INCR', 'stat:dup')          -- ya la había terminado otro worker: trabajo duplicado
  return 0
end
redis.call('HINCRBY', KEYS[2], ARGV[2], 1)
if redis.call('INCR', KEYS[3]) == tonumber(ARGV[3]) then
  redis.call('LPUSH', KEYS[4], 1)         -- ronda completa: despierta a la API
end
return 1
"""
