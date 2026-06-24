-- Detecta clientes cuya transacción actual es al menos 5 veces mayor
-- que su transacción inmediatamente anterior.
-- Regla de negocio 4: se parte de fraud_analysis, vista que ya filtra
-- estado_transaccion = 'aprobada', así que pendientes y rechazadas
-- quedan excluidas estructuralmente, no por un WHERE adicional aquí.

WITH transacciones_ordenadas AS (
    SELECT
        id_cliente,
        id_transaccion,
        fecha_hora,
        monto_usd,
        LAG(monto_usd) OVER (
            PARTITION BY id_cliente
            ORDER BY fecha_hora
        ) AS monto_anterior
    FROM fraud_analysis
)
SELECT
    id_cliente,
    id_transaccion,
    fecha_hora,
    monto_anterior,
    monto_usd,
    ROUND(monto_usd / monto_anterior, 2) AS factor_incremento
FROM transacciones_ordenadas
WHERE monto_anterior > 0
  AND monto_usd >= monto_anterior * 5
ORDER BY factor_incremento DESC;
