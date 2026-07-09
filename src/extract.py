import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_transactions(file_path: str, logical_date: str) -> pd.DataFrame:
    """Extracts transaction data from a CSV file."""
    logging.info(f"Extracting transactions from {file_path}")
    try:
        df = pd.read_csv(file_path)
        
        # Filter by logical_date
        df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')
        df_filtered = df[df['date'] == logical_date].copy()
        df_filtered = df_filtered.drop(columns=['date'])
        
        logging.info(f"Successfully extracted {len(df_filtered)} transaction records for {logical_date}.")
        return df_filtered
    except Exception as e:
        logging.error(f"Error reading transactions CSV: {e}")
        raise

def extract_crm_profiles() -> pd.DataFrame:
    """
    Simulates extracting user profiles from a CRM API.
    In a real scenario, this would use the `requests` library to fetch JSON from an endpoint.
    """
    logging.info("Extracting user profiles from CRM (Mock API)...")
    
    # Mocking a JSON response from an API
    mock_api_data = [
        {"user_id": "U001", "user_tier": "Standard", "kyc_status": "Verified"},
        {"user_id": "U002", "user_tier": "Premium", "kyc_status": "Verified"},
        {"user_id": "U003", "user_tier": "Standard", "kyc_status": "Pending"},
        {"user_id": "U004", "user_tier": "VIP", "kyc_status": "Verified"},
        {"user_id": "U005", "user_tier": "Standard", "kyc_status": "Verified"},
        {"user_id": "U006", "user_tier": "Premium", "kyc_status": "Verified"},
        {"user_id": "U007", "user_tier": "VIP", "kyc_status": "Pending"},
    ]
    
    df = pd.DataFrame(mock_api_data)
    logging.info(f"Successfully extracted {len(df)} CRM user profiles.")
    return df
