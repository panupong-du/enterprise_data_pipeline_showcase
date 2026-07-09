import logging
from src.extract import extract_transactions, extract_crm_profiles
from src.load import load_raw_transactions, load_dim_crm_users
from src.transform_sql import run_sql_transform
import glob
import argparse
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Run Enterprise ELT Pipeline")
    parser.add_argument("--date", type=str, required=True, help="Logical date in YYYY-MM-DD format")
    args = parser.parse_args()
    
    logical_date = args.date
    logging.info(f"--- Starting Enterprise ELT Pipeline for logical_date: {logical_date} ---")
    
    # Configuration
    CSV_FILE_PATH = "data/raw_transactions.csv"
    SQL_FILE_PATH = "sql/transform_daily_summary.sql"
    
    # GCP Configuration
    PROJECT_ID = "data-portfolio-project-501110"  
    DATASET_ID = "enterprise_data"
    
    # Automatically find the JSON key file in the root directory
    json_keys = glob.glob("*.json")
    if not json_keys:
        logging.error("No JSON Service Account key found in the root directory!")
        return
    KEY_PATH = json_keys[0]
    
    try:
        # Phase 1: Extract
        logging.info("=== PHASE 1: EXTRACT ===")
        df_transactions = extract_transactions(CSV_FILE_PATH, logical_date)
        if df_transactions.empty:
            logging.warning(f"No transaction data found for {logical_date}. Exiting pipeline.")
            return

        df_users = extract_crm_profiles()
        
        # Phase 2: Load Raw Data
        logging.info("=== PHASE 2: LOAD RAW DATA ===")
        load_raw_transactions(df_transactions, PROJECT_ID, DATASET_ID, KEY_PATH, logical_date)
        load_dim_crm_users(df_users, PROJECT_ID, DATASET_ID, KEY_PATH)
        
        # Phase 3: Transform (SQL in BigQuery)
        logging.info("=== PHASE 3: TRANSFORM (SQL) ===")
        run_sql_transform(PROJECT_ID, DATASET_ID, KEY_PATH, logical_date, SQL_FILE_PATH)
        
        logging.info("--- ELT Pipeline Execution Completed Successfully! ---")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
