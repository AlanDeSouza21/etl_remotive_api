from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.sdk import dag
from datetime import datetime

@dag(
    dag_id="remotive_etl_notebook",
    schedule="0 0 * * *",
    start_date=datetime(2026, 6, 26),
    catchup=False,
)
def remotive_etl_notebook_dag():
    PapermillOperator(
        task_id="executar_main_notebook",
        input_nb="/opt/airflow/notebooks/main.ipynb",
        output_nb="/opt/airflow/notebooks/out/main_{{ ds }}.ipynb",
    )

remotive_etl_notebook_dag()