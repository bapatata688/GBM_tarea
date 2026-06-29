import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, text

DDL_TABLA = """
CREATE TABLE IF NOT EXISTS transactions_clean (
    id_transaccion TEXT PRIMARY KEY,
    id_cliente TEXT,
    fecha_hora TIMESTAMP,
    monto_usd NUMERIC,
    tipo_comercio TEXT,
    estado_transaccion TEXT,
    es_monto_inusual BOOLEAN,
    procesado_en TIMESTAMP
)
"""

DDL_VISTA = """
CREATE OR REPLACE VIEW fraud_analysis AS
SELECT * FROM transactions_clean WHERE estado_transaccion = 'aprobada'
"""

UPSERT_DESDE_STAGING = """
INSERT INTO transactions_clean
SELECT * FROM transacciones_staging
ON CONFLICT (id_transaccion) DO NOTHING
"""


def obtener_engine():
    # Formato esperado: postgresql+psycopg2://usuario:clave@host:puerto/bd
    return create_engine(os.environ["SUPABASE_DB_URL"])


def cargar(df, engine=None):
    engine = engine or obtener_engine()
    df = df.copy()
    df["procesado_en"] = datetime.now(timezone.utc)

    with engine.begin() as conexion:
        conexion.execute(text(DDL_TABLA))
        conexion.execute(text(DDL_VISTA))
        df.to_sql("transacciones_staging", conexion, if_exists="replace", index=False)
        
        conexion.execute(text(UPSERT_DESDE_STAGING))
        conexion.execute(text("DROP TABLE transacciones_staging"))
