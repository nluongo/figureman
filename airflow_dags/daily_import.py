from airflow import DAG
from datetime import datetime

with DAG(dag_id='DailyImport', 
        start_date=datetime(2023, 12, 6),
        catchup=False,
        schedule_interval='@daily') as dag:

    from firefly_import import import_task

    import_task
