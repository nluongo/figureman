import os
import time
import yaml
from datetime import datetime
from airflow import DAG
from airflow.decorators import task, sensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.base import PokeReturnValue
from date_handler import compare_dates, seconds_since_last_updated, get_modification_date

with open('../../config.yaml') as config_f:
	try:
		config_dict = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

download_dir = config_dict['bofa_scraper']['download_dir']
scraper_bin = config_dict['bofa_scraper']['python_bin']
firefly_dir = config_dict['firefly']['statement_dir']

time_started = time.time()

with DAG(dag_id='ImportToFirefly', 
        start_date=datetime(2023, 12, 6),
        catchup=False) as dag:
    #compare_dates_task = PythonOperator(task_id='compare_dates', python_callable=compare_dates)
    import_task = BashOperator(task_id='firefly_import', bash_command='firefly_import.sh') 

    @task
    def scrape_call():
        import os
        os.system("gnome-terminal -e 'bash -c \"download_statements; bash\" '")

    # Statement downloads will be happening in the background
    @task.sensor(poke_interval=10, timeout=600, mode='poke')
    def done_scraping() -> PokeReturnValue:
        time_last_update = seconds_since_last_updated(download_dir)

        # Check that we've scraped anything before saying we're done
        started_scraping = False
        if get_modification_date(download_dir) > time_started:
            started_scraping = True

        condition_met = False
        if started_scraping and time_last_update > 60:
            condition_met = True

        return PokeReturnValue(is_done=condition_met)

    scrape_task = scrape_call()
    done_scraping_task = done_scraping()
    scrape_task >> done_scraping_task >> import_task
