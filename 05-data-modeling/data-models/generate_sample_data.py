"""
Sample Data Generator for Data Warehouse
Generates realistic dimension and fact data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

 Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

 Create output directory
output_dir = 'sample_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Generating sample data for data warehouse...")

 ============================================
 Generate DIM_DATE
 ============================================
print("Generating date dimension...")

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = []

current_date = start_date
while current_date <= end_date:
    date_range.append(current_date)
    current_date += timedelta(days=1)

dim_date = []
for date in date_range:
    dim_date.append({
        'date_key': int(date.strftime('%Y%m%d')),
        'full_date': date.strftime('%Y-%m-%d'),
        'year': date.year,
        'quarter': (date.month - 1) // 3 + 1,
        'month': date.month,
        'month_name': date.strftime('%B'),
        'week': date.isocalendar()[1],
        'day_of_month': date.day,
        'day_of_week': date.isoweekday(),
        'day_name': date.strftime('%A'),
        'is_weekend': date.weekday() >= 5,
        'is_holiday': False,   Would need holiday calendar
        'fiscal_year': date.year,
        'fiscal_quarter': (date.month - 1) // 3 + 1
    })

df_date = pd.DataFrame(dim_date)
df_date.to_csv(f'{output_dir}/dim_date.csv', index=False)
print(f"  Created {len(df_date)} date records")

 ============================================
 Generate DIM_CUSTOMER
 ============================================
print("Generating customer dimension...")

first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 
               'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
          'San Antonio', 'San Diego', 'Dallas', 'San Jose']
states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']
segments = ['Consumer', 'Corporate', 'Home Office']

num_customers = 10000
customers = []

for i in range(1, num_customers + 1):
    first = random.choice(first_names)
    last = random.choice(last_names)
    city_idx = random.randint(0, len(cities) - 1)
    reg_date = start_date + timedelta(days=random.randint(0, 365))
    
    customers.append({
        'customer_key': i,
        'customer_id': f'CUST-{i:06d}',
        'customer_name': f'{first} {last}',
        'email': f'{first.lower()}.{last.lower()}@email.com',
        'phone': f'555-{random.randint(100,999)}-{random.randint(1000,9999)}',
        'address_line1': f'{random.randint(100,9999)} Main St',
        'city': cities[city_idx],
        'state': states[city_idx],
        'postal_code': f'{random.randint(10000,99999)}',
        'country': 'USA',
        'customer_segment': random.choice(segments),
        'registration_date': reg_date.strftime('%Y-%m-%d'),
        'valid_from': reg_date.strftime('%Y-%m-%d'),
        'valid_to': '9999-12-31',
        'is_current': True,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

df_customer = pd.DataFrame(customers)
df_customer.to_csv(f'{output_dir}/dim_customer.csv', index=False)
print(f"  Created {len(df_customer)} customer records")

 ============================================
 Generate DIM_PRODUCT
 ============================================
print("Generating product dimension...")

categories = {
    'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Accessories'],
    'Clothing': ['Mens', 'Womens', 'Kids', 'Footwear'],
    'Home & Garden': ['Furniture', 'Kitchen', 'Garden', 'Decor'],
    'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Equipment'],
    'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children'],
    'Beauty': ['Skincare', 'Makeup', 'Haircare', 'Fragrance']
}

num_products = 500
products = []

for i in range(1, num_products + 1):
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])
    
     Price based on category
    if category == 'Electronics':
        price = round(random.uniform(50, 2000), 2)
    elif category == 'Clothing':
        price = round(random.uniform(20, 300), 2)
    elif category == 'Home & Garden':
        price = round(random.uniform(30, 800), 2)
    elif category == 'Sports':
        price = round(random.uniform(25, 500), 2)
    elif category == 'Books':
        price = round(random.uniform(10, 100), 2)
    else:   Beauty
        price = round(random.uniform(15, 250), 2)
    
    cost = round(price  random.uniform(0.4, 0.7), 2)
    
    products.append({
        'product_key': i,
        'product_id': f'PROD-{category[:3].upper()}-{i:04d}',
        'product_name': f'{category} {subcategory} Product {i}',
        'description': f'High-quality {category.lower()} product',
        'category': category,
        'subcategory': subcategory,
        'brand': random.choice(['Brand A', 'Brand B', 'Brand C', 'Brand D']),
        'supplier': random.choice(['Supplier X', 'Supplier Y', 'Supplier Z']),
        'unit_price': price,
        'unit_cost': cost,
        'weight_kg': round(random.uniform(0.1, 5), 2),
        'is_active': random.random() > 0.05,   95% active
        'launched_date': (start_date + timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d'),
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

df_product = pd.DataFrame(products)
df_product.to_csv(f'{output_dir}/dim_product.csv', index=False)
print(f"  Created {len(df_product)} product records")

 ============================================
 Generate DIM_STORE
 ============================================
print("Generating store dimension...")

store_locations = [
    ('New York', 'NY', 'Northeast'),
    ('Los Angeles', 'CA', 'West'),
    ('Chicago', 'IL', 'Midwest'),
    ('Houston', 'TX', 'South'),
    ('Phoenix', 'AZ', 'West'),
    ('Philadelphia', 'PA', 'Northeast'),
    ('San Antonio', 'TX', 'South'),
    ('San Diego', 'CA', 'West'),
    ('Dallas', 'TX', 'South'),
    ('San Jose', 'CA', 'West')
]

stores = []
for i, (city, state, region) in enumerate(store_locations, 1):
    stores.append({
        'store_key': i,
        'store_id': f'STORE-{state}-{i:03d}',
        'store_name': f'{city} {region} Store',
        'store_type': random.choice(['Flagship', 'Regular', 'Outlet']),
        'address': f'{random.randint(100,9999)} {["Main","Broadway","Oak","Maple"][i%4]} St',
        'city': city,
        'state': state,
        'postal_code': f'{random.randint(10000,99999)}',
        'country': 'USA',
        'region': region,
        'phone': f'800-555-{1000+i:04d}',
        'manager': f'Manager {