import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_data(df_trans: pd.DataFrame, df_users: pd.DataFrame, logical_date: str) -> pd.DataFrame:
    """
    Cleanses, joins, and aggregates transaction and user data.
    """
    logging.info(f"Starting data transformation for logical_date: {logical_date}")
    
    # 1. Filter Transactions (Only Completed)
    df_completed = df_trans[df_trans['status'] == 'Completed'].copy()
    logging.info(f"Filtered completed transactions: {len(df_completed)} records remaining.")
    
    # 2. Join with CRM Users Data
    df_merged = pd.merge(df_completed, df_users, on='user_id', how='left')
    
    # 3. Filter out Pending KYC users (Risk mitigation logic)
    df_clean = df_merged[df_merged['kyc_status'] == 'Verified'].copy()
    logging.info(f"Filtered verified users: {len(df_clean)} records remaining.")
    
    # 4. Feature Engineering: Extract date from timestamp
    df_clean['date'] = pd.to_datetime(df_clean['timestamp']).dt.date
    
    # 5. Aggregation
    # Group by Date, Transaction Type, and User Tier to get total amount and transaction count
    df_aggregated = df_clean.groupby(
        ['date', 'transaction_type', 'user_tier']
    ).agg(
        total_amount=('amount', 'sum'),
        transaction_count=('transaction_id', 'count')
    ).reset_index()
    
    logging.info("Data transformation and aggregation completed successfully.")
    return df_aggregated
