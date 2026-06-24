from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from src.main import main as transformar_y_cargar

with DAG(
    dag_id="dag_transacciones_fraude",
    description="Limpieza, carga y análisis diario de transacciones de tarjetas",
    schedule="30 23 * * *",  # 11:30 PM todos los días
    start_date=datetime(2026, 6, 1),
    catchup=False,
    default_args={"retries": 2},
) as dag:

    tarea_transformar_y_cargar = PythonOperator(
        task_id="transformar_y_cargar",
        python_callable=transformar_y_cargar,
    )

    tarea_analizar_anomalias = PostgresOperator(
        task_id="analizar_anomalias",
        postgres_conn_id="supabase_postgres",
        sql="sql/analisis_anomalias.sql",
    )

    # trigger_rule por defecto es "all_success": si la transformación/carga
    # falla, el análisis SQL no se ejecuta sobre datos a medio cargar.
    tarea_transformar_y_cargar >> tarea_analizar_anomalias
