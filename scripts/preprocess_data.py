import pandas as pd
import os
from datetime import datetime

def preprocess_data(raw_data_dir, processed_data_dir):
    """
    Loads raw sales and customer data, merges them, engineers new features,
    and saves the cleaned, processed data.
    """
    try:
        # Load the raw datasets
        sales_file = os.path.join(raw_data_dir, 'sales_transactions.csv')
        customers_file = os.path.join(raw_data_dir, 'customers.csv')
        df_sales = pd.read_csv(sales_file)
        df_customers = pd.read_csv(customers_file)
        print("Raw data loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error loading raw data: {e}. Please ensure data is in the 'data/raw/' directory.")
        return None

    # Merge the DataFrames
    df_merged = pd.merge(df_sales, df_customers, on='customer_id', how='inner')
    print("DataFrames merged successfully!")

    # Convert date columns to datetime objects
    df_merged['transaction_date'] = pd.to_datetime(df_merged['transaction_date'])
    df_merged['customer_since'] = pd.to_datetime(df_merged['customer_since'])
    df_merged['last_interaction'] = pd.to_datetime(df_merged['last_interaction'])
    print("Date columns converted to datetime objects.")

    # Aggregate transaction data for each customer
    today = datetime.now()
    df_customer_summary = df_merged.groupby('customer_id').agg(
        total_revenue=('total_price', 'sum'),
        average_order_value=('total_price', 'mean'),
        transaction_count=('transaction_id', 'count'),
        first_purchase_date=('transaction_date', 'min'),
        last_purchase_date=('transaction_date', 'max'),
        customer_since=('customer_since', 'first'),
        last_interaction=('last_interaction', 'max')
    ).reset_index()
    print("Transaction data aggregated to a customer level.")

    # Calculate final recency and tenure features
    df_customer_summary['customer_tenure_months'] = ((today - df_customer_summary['customer_since']).dt.days // 30)
    df_customer_summary['days_since_last_purchase'] = (today - df_customer_summary['last_purchase_date']).dt.days
    df_customer_summary['days_since_last_interaction'] = (today - df_customer_summary['last_interaction']).dt.days

    # Merge with original customer data for final attributes
    df_processed = pd.merge(df_customer_summary, df_customers.drop(columns=['customer_since', 'last_interaction']), on='customer_id', how='left')
    
    # Save the processed DataFrame
    os.makedirs(processed_data_dir, exist_ok=True)
    processed_file = os.path.join(processed_data_dir, 'cleaned_merged_data.csv')
    df_processed.to_csv(processed_file, index=False)
    print(f"Processed data saved to: {processed_file}")
    
    return df_processed

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    raw_data_path = os.path.join(script_dir, '..', 'data', 'raw')
    processed_data_path = os.path.join(script_dir, '..', 'data', 'processed')
    
    preprocess_data(raw_data_path, processed_data_path)