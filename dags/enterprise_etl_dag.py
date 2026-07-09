from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'enterprise_data_pipeline',
    default_args=default_args,
    description='Enterprise ETL Pipeline for Portfolio',
    schedule='0 8 * * *', # รันเวลา 8:00 น. (UTC) ของทุกวัน
    catchup=False,
    tags=['elt', 'portfolio', 'bigquery'],
) as dag:

    extract_task = BashOperator(
        task_id='extract_task',
        bash_command='echo "Starting Data Extraction for date: {{ ds }}..." && sleep 2 && echo "Data Extraction Completed."',
    )

    load_raw_task = BashOperator(
        task_id='load_raw_task',
        bash_command='echo "Starting Data Load (Raw) to BigQuery for date: {{ ds }}..." && sleep 2 && echo "Raw Data Load Completed."',
    )

    transform_sql_task = BashOperator(
        task_id='transform_sql_task',
        bash_command='echo "Starting SQL Transformation in BigQuery for date: {{ ds }}..." && sleep 2 && echo "SQL Transformation Completed."',
    )

    extract_task >> load_raw_task >> transform_sql_task
