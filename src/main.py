import sys

from .cargar import cargar
from .transformar import transformar

RUTA_CSV_DEFECTO = "data/transacciones_diarias.csv"


def main(ruta_csv=RUTA_CSV_DEFECTO):
    df = transformar(ruta_csv)
    cargar(df)
    print(f"{len(df)} transacciones procesadas y cargadas en transactions_clean")
    return df


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else RUTA_CSV_DEFECTO)
