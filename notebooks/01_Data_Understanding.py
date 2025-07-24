# 01_Data_Acquisition_Understanding.ipynb

import pandas as pd
import os

# Define file paths (assuming this notebook is in the project root)
data_dir = 'data'
sales_file_path = os.path.join(data_dir, 'sales_transactions.csv')
customers_file_path = os.path.join(data_dir, 'customers.csv')

print("--- Loading DataFrames ---")

# Load the datasets
try:
    df_sales = pd.read_csv(sales_file_path)
    df_customers = pd.read_csv(customers_file_path)
    print("DataFrames loaded successfully!")
except FileNotFoundError:
    print(f"Error: Make sure '{data_dir}' directory exists and CSV files are in it.")
    print("Please run 'scripts/data_generator.py' first.")
    exit() # Exit if files are not found

print("\n--- Initial Inspection of Sales Data (df_sales) ---")
print("Shape (rows, columns):", df_sales.shape)
print("\nFirst 5 rows:")
print(df_sales.head())
print("\nData Types:")
print(df_sales.info())
print("\nDescriptive Statistics for numerical columns:")
print(df_sales.describe())
print("\nUnique values in key categorical columns:")
print("Product Categories:", df_sales['product_category'].unique())
print("Sales Regions:", df_sales['sales_region'].unique())
print("Lead Sources:", df_sales['lead_source'].unique())
print("Deal Stages:", df_sales['deal_stage'].unique())


print("\n--- Initial Inspection of Customer Data (df_customers) ---")
print("Shape (rows, columns):", df_customers.shape)
print("\nFirst 5 rows:")
print(df_customers.head())
print("\nData Types:")
print(df_customers.info())
print("\nDescriptive Statistics for numerical columns:")
print(df_customers.describe())
print("\nUnique values in key categorical columns:")
print("Industry:", df_customers['industry'].unique())
print("Company Size:", df_customers['company_size'].unique())
print("Churn Status (0=Active, 1=Churned):", df_customers['churn_status'].value_counts())
print("\nChurn Rate:")
print(f"{df_customers['churn_status'].mean():.2%}")

# Check for customer_id overlap (should be 100% due to generation logic)
print("\n--- Cross-dataset Customer ID check ---")
common_customers = set(df_sales['customer_id']).intersection(set(df_customers['customer_id']))
print(f"Number of common customers in both datasets: {len(common_customers)}")
print(f"Total customers in sales data: {df_sales['customer_id'].nunique()}")
print(f"Total customers in customer data: {df_customers['customer_id'].nunique()}")
if len(common_customers) == df_sales['customer_id'].nunique() and \
   len(common_customers) == df_customers['customer_id'].nunique():
    print("All customer IDs are consistent across both datasets.")
else:
    print("Warning: Customer ID inconsistency detected. Review data generation/loading.")

# Convert date columns to datetime objects (even though we tried during saving, good to confirm)
# This is a crucial step for any time-series analysis or filtering by date.
df_sales['transaction_date'] = pd.to_datetime(df_sales['transaction_date'])
df_customers['customer_since'] = pd.to_datetime(df_customers['customer_since'])
df_customers['last_interaction'] = pd.to_datetime(df_customers['last_interaction'])

print("\n--- Confirmed Date Data Types ---")
print(df_sales['transaction_date'].dtype)
print(df_customers['customer_since'].dtype)
print(df_customers['last_interaction'].dtype)

# Save the loaded and date-converted dataframes to new CSVs if needed, or just proceed
# For this phase, we're just inspecting. We'll save processed data in Phase 2.