import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate date range (2 years of data)
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Define categories and products
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys']
regions = ['North', 'South', 'East', 'West', 'Central']
customer_segments = ['Consumer', 'Corporate', 'Home Office']
payment_methods = ['Credit Card', 'PayPal', 'Debit Card', 'Gift Card']
shipping_methods = ['Standard', 'Express', 'Next Day']

# Create product catalog
products = []
for cat in categories:
    for i in range(1, 11):  # 10 products per category
        price = 0
        if cat == 'Electronics':
            price = round(random.uniform(50, 1000), 2)
        elif cat == 'Clothing':
            price = round(random.uniform(20, 200), 2)
        elif cat == 'Home & Garden':
            price = round(random.uniform(30, 500), 2)
        elif cat == 'Sports':
            price = round(random.uniform(25, 300), 2)
        elif cat == 'Books':
            price = round(random.uniform(10, 80), 2)
        elif cat == 'Toys':
            price = round(random.uniform(15, 150), 2)
        
        products.append({
            'product_id': f'PROD_{cat[:3].upper()}_{i:03d}',
            'product_name': f'{cat} Product {i}',
            'category': cat,
            'subcategory': f'{cat} - Type {chr(64+i)}',
            'unit_price': price,
            'cost': round(price * 0.6, 2)  # 40% margin
        })

products_df = pd.DataFrame(products)

# Generate sales transactions
num_transactions = 5000
sales_data = []

for i in range(num_transactions):
    # Random date
    order_date = random.choice(date_range)
    
    # Random product
    product = products_df.iloc[random.randint(0, len(products_df)-1)]
    
    # Random quantity (1-5)
    quantity = random.randint(1, 5)
    
    # Calculate sales and profit
    sales = product['unit_price'] * quantity
    cost = product['cost'] * quantity
    profit = sales - cost
    
    # Random discount (0%, 5%, 10%, 15%, 20%)
    discount_pct = random.choice([0, 0.05, 0.10, 0.15, 0.20])
    discount = sales * discount_pct
    final_sales = sales - discount
    
    # Create transaction
    transaction = {
        'order_id': f'ORD-{20240000 + i}',
        'order_date': order_date.strftime('%Y-%m-%d'),
        'customer_id': f'CUST-{random.randint(1000, 9999)}',
        'customer_name': f'Customer {random.randint(1000, 9999)}',
        'customer_segment': random.choice(customer_segments),
        'region': random.choice(regions),
        'product_id': product['product_id'],
        'product_name': product['product_name'],
        'category': product['category'],
        'subcategory': product['subcategory'],
        'unit_price': product['unit_price'],
        'quantity': quantity,
        'discount_pct': discount_pct,
        'discount_amount': round(discount, 2),
        'sales_amount': round(final_sales, 2),
        'cost_amount': round(cost, 2),
        'profit_amount': round(final_sales - cost, 2),
        'payment_method': random.choice(payment_methods),
        'shipping_method': random.choice(shipping_methods),
        'shipping_cost': round(random.uniform(5, 30), 2),
        'order_priority': random.choice(['High', 'Medium', 'Low']),
        'year': order_date.year,
        'quarter': f'Q{(order_date.month-1)//3 + 1}',
        'month': order_date.strftime('%B'),
        'month_num': order_date.month,
        'day_of_week': order_date.strftime('%A')
    }
    sales_data.append(transaction)

# Create DataFrame
df = pd.DataFrame(sales_data)

# Sort by date
df = df.sort_values('order_date')

# Save to CSV
df.to_csv('data/sales_data.csv', index=False)
print(f'Generated {len(df)} sales records')
print('Sample data:')
print(df.head())
print('\nSummary:')
print(f'Total Sales: ')
print(f'Total Profit: ')
print(f'Average Order Value: ')
