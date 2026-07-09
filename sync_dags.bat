@echo off
echo Syncing DAG files to Airflow containers...
docker cp dags/. enterprise_data_pipeline_showcase-airflow-scheduler-1:/opt/airflow/dags/
docker cp dags/. enterprise_data_pipeline_showcase-airflow-webserver-1:/opt/airflow/dags/
docker cp dags/. enterprise_data_pipeline_showcase-airflow-worker-1:/opt/airflow/dags/
echo Sync complete! 
echo Please wait a few seconds and refresh the Airflow UI.
pause
