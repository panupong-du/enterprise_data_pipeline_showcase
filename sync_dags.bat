@echo off
echo Syncing DAG files to Airflow containers...
docker cp dags/. data_engineering_hub-airflow-scheduler-1:/opt/airflow/dags/
docker cp dags/. data_engineering_hub-airflow-webserver-1:/opt/airflow/dags/
docker cp dags/. data_engineering_hub-airflow-worker-1:/opt/airflow/dags/
echo Sync complete! 
echo Please wait a few seconds and refresh the Airflow UI.
pause
