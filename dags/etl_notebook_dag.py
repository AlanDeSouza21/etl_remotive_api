from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.sdk import dag
from datetime import datetime
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="remotive_etl_notebook",
    schedule="0 0 * * *",
    start_date=datetime(2026, 6, 26),
    catchup=False,
)
def remotive_etl_notebook_dag():
    # Task 1: dentro da função
    criar_diretorio = BashOperator(
        task_id="criar_diretorio_output",
        bash_command="mkdir -p /opt/airflow/notebooks/out/",
    )

    # Task 2: dentro da função e atribuída a uma variável
    executar_notebook = PapermillOperator(
        # Identificador único da tarefa dentro da DAG
        task_id="executar_main_notebook",

        # Caminho do notebook de entrada (template/source)
        # Este arquivo deve existir no worker que executar a tarefa
        input_nb="/opt/airflow/notebooks/main.ipynb",

        # Caminho do notebook de saída com os outputs da execução
        # "{{ ds }}" é uma macro do Airflow: a data de execução no formato YYYY-MM-DD
        # Ex: main_2026-06-26.ipynb — útil para manter histórico de cada run
        output_nb="/opt/airflow/notebooks/out/main_{{ ds }}.ipynb",

        # [OPCIONAL] Dicionário de parâmetros injetados no notebook em tempo de execução
        # O notebook precisa ter uma célula tagged como "parameters" para recebê-los
        # parameters={"data": "{{ ds }}", "env": "production"},

        # [OPCIONAL] Kernel do Jupyter a ser usado na execução (padrão: o do próprio notebook)
        # Útil quando você tem múltiplos kernels/ambientes no worker
        # kernel_name="python3",

        # [OPCIONAL] Define o diretório de trabalho durante a execução do notebook
        # Por padrão usa o diretório do input_nb
        # cwd="/opt/airflow/notebooks",
    )

    criar_diretorio >> executar_notebook

remotive_etl_notebook_dag()