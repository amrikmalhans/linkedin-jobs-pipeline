import sys
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

sys.path.append("/opt/airflow/etl/extract")
from etl.extract.scraper import scrapeWebpage


@dag(
    default_args={
        "owner": "airflow",
    },
    schedule_interval="@daily",
    start_date=days_ago(2),
    tags=["example"],
    dag_id="linkedin_etl_dag",
)
def linkedin_etl_dag():
    @task
    def extract():
        return scrapeWebpage()

    extract_task = extract()


linkedin_etl_dag = linkedin_etl_dag()
