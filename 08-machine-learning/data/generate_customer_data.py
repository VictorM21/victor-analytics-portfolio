"""
Generate Synthetic Customer Data for Churn Prediction
Author: Victor Makanju
Purpose: Create realistic telecom customer data with churn labels
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("Generating synthetic customer data for churn prediction...")

# Number of customers to generate
n_customers = 5000

# Define possible values for categorical features
contract_types = ['Month-to-month', 'One year', 'Two year']
internet_services = ['DSL', 'Fiber optic', 'No']
payment_methods = ['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card']
genders = ['Male', 'Female']
yes_no = ['Yes', 'No']

# Generate data
data = []

for i in range(1, n_customers + 1):
    # Basic customer info
    customer = {
        'customer_id': f'CUST-{i:05d}',
        'gender': random.choice(genders),
        'senior_citizen': np.random.choice([0, 1], p=[0.8, 0.2]),  # 20% seniors
        'partner': random.choice(yes_no),
        'dependents': random.choice(yes_no),
        'tenure': np.random.randint(1, 73),  # 1-72 months
    }
    
    # Service features
    customer['phone_service'] = np.random.choice([0, 1], p=[0.1, 0.9])  # 90% have phone
    customer['multiple_lines'] = random.choice(yes_no) if customer['phone_service'] == 1 else 'No'
    customer['internet_service'] = random.choice(internet_services)
    
    if customer['internet_service'] != 'No':
        customer['online_security'] = random.choice(yes_no)
        customer['online_backup'] = random.choice(yes_no)
        customer['device_protection'] = random.choice(yes_no)
        customer['tech_support'] = random.choice(yes_no)
        customer['streaming_tv'] = random.choice(yes_no)
        customer['streaming_movies'] = random.choice(yes_no)
    else:
        # No internet = no online services
        customer['online_security'] = 'No'
        customer['online_backup'] = 'No'
        customer['device_protection'] = 'No'
        customer['tech_support'] = 'No'
        customer['streaming_tv'] = 'No'
        customer['streaming_movies'] = 'No'
    
    # Contract and billing
    customer['contract'] = random.choice(contract_types)
    customer['paperless_billing'] = random.choice(yes_no)
    customer['payment_method'] = random.choice(payment_methods)
    
    # Calculate charges based on services
    monthly_base = 20  # Base fee
    
    # Add internet costs
    if customer['internet_service'] == 'Fiber optic':
        monthly_base += 30
    elif customer['internet_service'] == 'DSL':
        monthly_base += 20
    
    # Add service costs
    if customer['online_security'] == 'Yes': monthly_base += 5
    if customer['online_backup'] == 'Yes': monthly_base += 5
    if customer['device_protection'] == 'Yes': monthly_base += 5
    if customer['tech_support'] == 'Yes': monthly_base += 5
    if customer['streaming_tv'] == 'Yes': monthly_base += 10
    if customer['streaming_movies'] == 'Yes': monthly_base += 10
    if customer['multiple_lines'] == 'Yes': monthly_base += 10
    
    # Phone service
    if customer['phone_service'] == 1:
        monthly_base += 20
    
    customer['monthly_charges'] = round(monthly_base + np.random.normal(0, 5), 2)
    customer['total_charges'] = round(customer['monthly_charges'] * customer['tenure'], 2)
    
    # Determine churn based on realistic patterns
    churn_probability = 0.1  # Base 10% churn rate
    
    # Increase churn probability for risk factors
    if customer['contract'] == 'Month-to-month':
        churn_probability += 0.15
    if customer['tenure'] < 6:
        churn_probability += 0.1
    if customer['internet_service'] == 'Fiber optic':
        churn_probability += 0.05
    if customer['payment_method'] == 'Electronic check':
        churn_probability += 0.05
    if customer['senior_citizen'] == 1:
        churn_probability -= 0.02  # Seniors slightly more loyal
    if customer['dependents'] == 'Yes':
        churn_probability -= 0.03  # Families more stable
    if customer['partner'] == 'Yes':
        churn_probability -= 0.02
    
    # Cap probability between 0 and 1
    churn_probability = max(0.05, min(0.5, churn_probability))
    
    customer['churn'] = np.random.choice(['Yes', 'No'], p=[churn_probability, 1-churn_probability])
    
    data.append(customer)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('data/customer_churn_data.csv', index=False)

print(f"\n✅ Generated {len(df)} customer records")
print(f"📊 Churn rate: {df['churn'].value_counts(normalize=True)['Yes']:.1%}")
print(f"\n📋 Columns: {', '.join(df.columns)}")

# Show sample
print("\n📝 First 5 rows:")
print(df.head())

# Quick statistics
print("\n📈 Summary statistics:")
print(df[['tenure', 'monthly_charges', 'total_charges']].describe())