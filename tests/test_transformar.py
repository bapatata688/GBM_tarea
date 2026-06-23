import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from transformar import (
    corregir_montos_rechazados,
    eliminar_duplicados,
    marcar_montos_inusuales,
)


def test_reglas_de_negocio():
    df = pd.DataFrame(
        {
            "id_transaccion": ["T-1", "T-1", "T-2", "T-3", "T-4", "T-5"],
            "monto_usd": [100.0, 100.0, None, 2000.0, 3000.0, 2500.0],
            "tipo_comercio": ["nacional", "nacional", "internacional", "internacional", "internacional", "internacional"],
            "estado_transaccion": ["aprobado", "aprobado", "rechazada", "aprobado", "pendiente", "rechazada"],
        }
    )

  
    df = eliminar_duplicados(df)
    assert len(df) == 5, "debe eliminar el duplicado T-1 (quedan 5 filas de 6)"

  
    df = corregir_montos_rechazados(df)
    monto_rechazada = df.loc[df["id_transaccion"] == "T-2", "monto_usd"].iloc[0]
    assert monto_rechazada == 0.0, "monto nulo en rechazada debe quedar en 0.0"

    df = marcar_montos_inusuales(df)
    inusual = df.set_index("id_transaccion")["es_monto_inusual"]
    
    
    assert inusual["T-3"], "monto > 1500, internacional y aprobado debe marcarse inusual"
    assert not inusual["T-1"], "nacional no debe marcarse inusual"
    assert not inusual["T-2"], "monto 0.0 no debe ser inusual"
    
    
    assert not inusual["T-4"], "monto > 1500 e internacional NO debe ser inusual si está PENDIENTE"
    assert not inusual["T-5"], "monto > 1500 e internacional NO debe ser inusual si está RECHAZADA"

    print("OK: las 4 reglas de negocio se cumplen perfectamente")


if __name__ == "__main__":
    test_reglas_de_negocio()
