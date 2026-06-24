import pandas as pd

MONTO_MINIMO_INUSUAL = 1500
TIPO_COMERCIO_INUSUAL = "internacional"
ESTADO_RECHAZADA = "rechazada"


def leer_csv(ruta):
    return pd.read_csv(ruta, parse_dates=["fecha_hora"])


def eliminar_duplicados(df):
    # Regla 1: id_transaccion es el identificador único de deduplicación
    return df.drop_duplicates(subset="id_transaccion", keep="first")


def corregir_montos_rechazados(df):
    # Regla 2: monto nulo en una transacción rechazada equivale a 0.0
    mascara = df["monto_usd"].isna() & (df["estado_transaccion"] == ESTADO_RECHAZADA)
    df.loc[mascara, "monto_usd"] = 0.0
    return df


def marcar_montos_inusuales(df):
    # Regla 3: inusual solo si monto > 1500 USD y el comercio es internacional
    df["es_monto_inusual"] = (df["monto_usd"] > MONTO_MINIMO_INUSUAL) & (
        df["tipo_comercio"] == TIPO_COMERCIO_INUSUAL
    )
    return df


def transformar(ruta_csv):
    df = leer_csv(ruta_csv)
    df = eliminar_duplicados(df)
    df = corregir_montos_rechazados(df)
    df = marcar_montos_inusuales(df)
    return df
