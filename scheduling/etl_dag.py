from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# Airflow DAG ще се изпълнява от понеделник до петък в 9:30 AM
with DAG(
        dag_id="invoices_etl_pipeline",
        start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
        schedule="30 9 * * 1-5",  # Cron формат: 30 минути, 9 часа, всеки ден, всеки месец, от понеделник до петък
        catchup=False,
        tags=["etl", "telecom", "invoices"],
) as dag:
    # Задача за изпълнение на Python скрипта main.py
    # `bash_command` изпълнява командата python main.py
    run_etl_script = BashOperator(
        task_id="run_etl_script",
        bash_command="python main.py",
        cwd="/path/to/your/project/folder",  # Замени с пътя до директорията на твоя проект
    )