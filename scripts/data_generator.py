import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta, date 
import os

fake = Faker('en_IN')

# Let's generate random sales data
def generate_sales_data(num_transactions=10000, start_date_str='2022-01-01', end_date_str='2025-07-25'): 
    print(f"Generating {num_transactions} sales transactions...")

    start_date_obj = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    p_categories = ['Cloud Solutions','CRM Software','Data Analytics','Consulting','Security Services']
    p_per_categories = {
        'Cloud Solutions':['Cloud Storage Tier 1', 'Cloud Storage Tier 2', 'Virtual Servers Basic', 'Virtual Servers Advanced'],
        'CRM Software':['Salesforce CRM Core', 'Salesforce Marketing Cloud','Salesforce Service Cloud'], 
        'Data Analytics':['Analytics Dashboard Pro','Predictive Modeling Suite','Reporting Tool Basic'],
        'Consulting':['Implementation Consulting','Strategy Consulting','Training Services'],
        'Security Services':['Endpoint Security','Network Security','Data Encryption']
    }
    sales_reg=['New Delhi','Bangalore','Mumbai','Chennai']
    lead_sources=['Website','Referral','Cold Call','Partner','Social Media','Advertisement']
    deal_stage=['Closed Won','Closed Lost','Negotiation','Prospecting','Proposal Sent'] 

    transactions=[]
    num_sales_reps=50
    sales_rep_ids=[f'SREP{i:03d}' for i in range(1,num_sales_reps+1)]

    for i in range(num_transactions):
        # Passing the datetime.date objects to fake.date_between()
        transaction_date = fake.date_between(start_date=start_date_obj, end_date=end_date_obj)

        # What if my transac date is in future relative to current execution time
        # This check is good, but the conversion back to string for end_date is unnecessary if `date` objects are used consistently
        if(transaction_date > datetime.now().date()):
            transaction_date = fake.date_between(start_date=start_date_obj, end_date=datetime.now().date())


        category = random.choice(p_categories)
        if category == 'CRM Software':
            product = random.choice(p_per_categories['CRM Software'])
        else:
            product = random.choice(p_per_categories[category])

        quantity = random.randint(1,100)
        if 'Cloud' in category or 'CRM' in category:
            price_per_unit = round(random.uniform(100.0,5000.0),2)
        elif 'Analytics' in category:
            price_per_unit = round(random.uniform(500.0,7000.0),2)
        elif 'Consulting' in category:
            price_per_unit = round(random.uniform(2000.0,15000.0),2)
        else:
            price_per_unit = round(random.uniform(300.0,6000.0),2)
        total_price = round(quantity*price_per_unit,2)

        transactions.append({
            'transaction_id': f'TRANS{i:05d}',
            'customer_id': f'CUST{random.randint(1, num_transactions//10):04d}',
            'transaction_date': transaction_date,
            'product_id': f'PROD{random.randint(1, 20):03d}',
            'product_category': category,
            'quantity': quantity,
            'price_per_unit': price_per_unit,
            'total_price': total_price,
            'sales_rep_id': random.choice(sales_rep_ids),
            'sales_region': random.choice(sales_reg),
            'lead_source': random.choice(lead_sources),
            'deal_stage': random.choice(deal_stage)
        })

    df = pd.DataFrame(transactions)
    df.loc[df['deal_stage']=='Closed Lost','total_price']=0
    df.loc[df['deal_stage']=='Closed Lost','quantity']=0
    return df

def generate_customer_data(num_customers=1000, start_date_str='2019-01-01',end_date_str='2025-07-25'): # Renamed parameters
    '''Generates synthetic customer data.'''
    print(f"Generating {num_customers} customers...")

    # Convert date strings to datetime.date objects
    start_date_obj = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    industries=['Tech','Healthcare','Finance','Manufacturing','Retail','Education','Government','Non-Profit']
    company_sizes=['Small','Mid-Market','Enterprise']

    customers=[]

    for i in range(num_customers):
        # Pass the datetime.date objects to fake.date_between()
        customer_since = fake.date_between(start_date=start_date_obj,end_date=end_date_obj)

        if(customer_since > datetime.now().date()):
            customer_since = fake.date_between(start_date=start_date_obj,end_date=datetime.now().date()) # Use date object directly

        last_interaction_max_date = datetime.now().date()
        last_interaction_min_date = max(customer_since,(datetime.now() - timedelta(days=365*2)).date())

        # Pass datetime.date objects to fake.date_between()
        last_interaction = fake.date_between(start_date=last_interaction_min_date,
                                             end_date=last_interaction_max_date)

        support_tickets = random.randint(0,50)
        satisfaction_score = random.randint(1,10)
        churn_status = 0
        customer_age_days = (datetime.now().date() - customer_since).days

        if (satisfaction_score <=4 and random.random() < 0.7) or \
           (support_tickets >= 15 and random.random() < 0.6) or \
           ((datetime.now().date() - last_interaction).days > 180 and random.random() < 0.5) or \
           (customer_age_days > 730 and (datetime.now().date() - last_interaction).days > 365 and random.random() < 0.4):
            churn_status = 1

            if (datetime.now().date() - last_interaction).days < 180:
                # Pass datetime.date objects to fake.date_between()
                last_interaction = fake.date_between(start_date=(datetime.now() - timedelta(days=365)).date(),
                                                     end_date=(datetime.now() - timedelta(days=181)).date())
                
            if satisfaction_score > 5:
                satisfaction_score = random.randint(1,5)

        customers.append({
            'customer_id':f'CUST{i:04d}',
            'customer_name':fake.company(),
            'industry':random.choice(industries),
            'company_size':random.choice(company_sizes),
            'customer_since':customer_since,
            'last_interaction':last_interaction,
            'support_tickets':support_tickets,
            'satisfaction_score':satisfaction_score,
            'churn_status': churn_status
        })
    
    df = pd.DataFrame(customers)
    churn_rate_target = 0.15
    actual_churn_rate = df['churn_status'].mean()

    if actual_churn_rate > churn_rate_target:
        num_to_change = int(df.shape[0] * (actual_churn_rate - churn_rate_target))
        churned_indices = df[df['churn_status']==1].index
        
        if len(churned_indices) > 0:
            indices_to_change = np.random.choice(churned_indices, min(num_to_change,len(churned_indices)),replace=False)
            df.loc[indices_to_change,'churn_status'] = 0
            df.loc[indices_to_change,'satisfaction_score'] = random.randint(6,10)
            df.loc[indices_to_change,'support_tickets'] = random.randint(0,5)
            # Pass datetime.date objects to fake.date_between()
            df.loc[indices_to_change,'last_interaction'] = fake.date_between(
                start_date=(datetime.now() - timedelta(days=90)).date(),
                end_date=datetime.now().date()
            )
            
    print(f"Generated churn rate: {df['churn_status'].mean():.2%}")
    return df


if __name__ == "__main__":
    output_dir = '../data'
    os.makedirs(output_dir, exist_ok=True)
    sales_file = os.path.join(output_dir,'sales_transactions.csv')
    customers_file = os.path.join(output_dir,'customers.csv')

    # Current date based on your context (July 25, 2025)
    current_date_str = "2025-07-25" 

    # Generate and save data
    # Pass date strings to functions (they will convert them internally)
    df_sales = generate_sales_data(num_transactions=50000, end_date_str=current_date_str)
    df_customers = generate_customer_data(num_customers=5000, end_date_str=current_date_str)
        
    valid_customer_ids = df_customers['customer_id'].unique()
    df_sales = df_sales[df_sales['customer_id'].isin(valid_customer_ids)]

    customers_with_sales = df_sales['customer_id'].unique()
    df_customers = df_customers[df_customers['customer_id'].isin(customers_with_sales)]

    df_sales = df_sales.sort_values(by=['customer_id', 'transaction_date']).reset_index(drop=True)
    df_customers = df_customers.sort_values(by='customer_id').reset_index(drop=True)

    df_sales['transaction_date'] = pd.to_datetime(df_sales['transaction_date'])
    df_customers['customer_since'] = pd.to_datetime(df_customers['customer_since']) 
    df_customers['last_interaction'] = pd.to_datetime(df_customers['last_interaction'])

    df_sales.to_csv(sales_file,index=False)
    df_customers.to_csv(customers_file,index=False)

    print(f"\nSynthetic sales data saved to: {sales_file}")
    print(f"Synthetic customer data saved to: {customers_file}")
    print(f"Sales Data Shape: {df_sales.shape}")
    print(f"Customer Data Shape: {df_customers.shape}")