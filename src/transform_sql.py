import logging
from google.cloud import bigquery
from google.oauth2 import service_account
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_bq_client(project_id: str, key_path: str) -> bigquery.Client:
    if not os.path.exists(key_path):
        logging.error(f"Service account key file not found at {key_path}")
        raise FileNotFoundError(f"Missing JSON key file at {key_path}")
    credentials = service_account.Credentials.from_service_account_file(key_path)
    return bigquery.Client(credentials=credentials, project=project_id)

def run_sql_transform(project_id: str, dataset_id: str, key_path: str, logical_date: str, sql_file_path: str):
    """
    Executes a SQL file on BigQuery to perform ELT transformation.
    """
    logging.info(f"Starting SQL transformation for date {logical_date} using {sql_file_path}")
    
    try:
        if not os.path.exists(sql_file_path):
            raise FileNotFoundError(f"SQL file not found at {sql_file_path}")
            
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_query = f.read()
            
        # Format the SQL query with runtime parameters
        formatted_sql = sql_query.format(
            project=project_id,
            dataset=dataset_id,
            logical_date=logical_date
        )
        
        logging.info("Executing the following SQL query on BigQuery:\n" + formatted_sql)
        
        client = get_bq_client(project_id, key_path)
        query_job = client.query(formatted_sql)
        
        # Wait for the job to complete
        query_job.result()
        logging.info("SQL transformation completed successfully.")
        
    except Exception as e:
        logging.error(f"Failed to execute SQL transformation: {e}")
        raise
