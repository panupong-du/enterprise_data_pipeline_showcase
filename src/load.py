import pandas as pd
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

def load_raw_transactions(df: pd.DataFrame, project_id: str, dataset_id: str, key_path: str, logical_date: str):
    """
    Loads raw transaction DataFrame into BigQuery stg_raw_transactions table.
    Uses Idempotent logic: DELETE existing data for the logical_date, then APPEND.
    """
    table_id = "stg_raw_transactions"
    logging.info(f"Preparing to load raw data to {project_id}.{dataset_id}.{table_id} for date {logical_date}")
    
    try:
        client = get_bq_client(project_id, key_path)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        
        # Delete existing data for the logical date (Idempotency)
        delete_query = f"DELETE FROM `{table_ref}` WHERE CAST(DATE(timestamp) AS STRING) = '{logical_date}'"
        logging.info(f"Executing idempotent delete query: {delete_query}")
        try:
            delete_job = client.query(delete_query)
            delete_job.result()
        except Exception as e:
            logging.warning(f"Delete query failed (table might not exist yet or empty): {e}")

        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND", 
        )
        
        logging.info("Uploading raw transactions to BigQuery...")
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  
        logging.info(f"Successfully loaded {job.output_rows} rows into {table_ref}.")
        
    except Exception as e:
        logging.error(f"Failed to load raw transactions to BigQuery: {e}")
        raise

def load_dim_crm_users(df: pd.DataFrame, project_id: str, dataset_id: str, key_path: str):
    """
    Loads CRM user profiles into BigQuery dim_crm_users table.
    Uses WRITE_TRUNCATE since it's a dimension table (full replace).
    """
    table_id = "dim_crm_users"
    logging.info(f"Preparing to load dimension data to {project_id}.{dataset_id}.{table_id}")
    
    try:
        client = get_bq_client(project_id, key_path)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE", 
        )
        
        logging.info("Uploading CRM users to BigQuery...")
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  
        logging.info(f"Successfully loaded {job.output_rows} rows into {table_ref}.")
        
    except Exception as e:
        logging.error(f"Failed to load CRM users to BigQuery: {e}")
        raise
