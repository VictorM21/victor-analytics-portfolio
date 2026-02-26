import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

 Set random seed
np.random.seed(42)
random.seed(42)

print('Generating large e-commerce dataset for cloud warehouses...')

 Generate date range (3 years)
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

 Generate 10,000 customers
customers = []
for i in range(1, 10001):
    customers.append({
        'customer_id': i,
        'customer_name': f'Customer_{i}',
        'email': f'customer{i}@example.com',
        'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                               'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']),
        'state': random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']),
        'country': 'USA',
        'registration_date': random.choice(date_range[:500]).strftime('%Y-%m-%d'),
        'customer_segment': random.choice(['Consumer', 'Corporate', 'Home Office'])
    })
customers_df = pd.DataFrame(customers)

 Generate 500 products
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Food', 'Beauty']
products = []
for i in range(1, 501):
    cat = random.choice(categories)
    if cat == 'Electronics':
        price = round(random.uniform(50, 2000), 2)
    elif cat == 'Clothing':
        price = round(random.uniform(20, 300), 2)
    elif cat == 'Home & Garden':
        price = round(random.uniform(30, 800), 2)
    elif cat == 'Sports':
        price = round(random.uniform(25, 500), 2)
    elif cat == 'Books':
        price = round(random.uniform(10, 100), 2)
    elif cat == 'Toys':
        price = round(random.uniform(15, 200), 2)
    elif cat == 'Food':
        price = round(random.uniform(5, 150), 2)
    elif cat == 'Beauty':
        price = round(random.uniform(10, 250), 2)
    else:
        price = round(random.uniform(20, 100), 2)
    
    products.append({
        'product_id': i,
        'product_name': f'{cat} Product {i}',
        'category': cat,
        'subcategory': f'{cat} - {random.choice(["Premium", "Standard", "Budget"])}',
        'brand': random.choice(['Brand A', 'Brand B', 'Brand C', 'Brand D']),
        'supplier': random.choice(['Supplier X', 'Supplier Y', 'Supplier Z']),
        'unit_price': price,
        'cost': round(price  0.6, 2),
        'weight_kg': round(random.uniform(0.1, 5), 2)
    })
products_df = pd.DataFrame(products)

 Generate 100,000 orders
num_orders = 100000
orders = []

print(f'Generating {num_orders} orders...')

for i in range(num_orders):
    if i % 10000 == 0 and i > 0:
        print(f'  Progress: {i}/{num_orders} orders')
    
    order_date = random.choice(date_range)
    customer = customers_df.iloc[random.randint(0, len(customers_df)-1)]
    
     Create order record - initialize order_total as 0.0 (float)
    orders.append({
        'order_id': i + 1,
        'customer_id': customer['customer_id'],
        'order_date': order_date.strftime('%Y-%m-%d'),
        'order_total': 0.0,   Changed to float
        'payment_method': random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Gift Card']),
        'shipping_method': random.choice(['Standard', 'Express', 'Next Day']),
        'order_status': random.choice(['Completed', 'Shipped', 'Processing', 'Cancelled'])
    })

orders_df = pd.DataFrame(orders)

 Generate order items
order_items = []
print('Generating order items...')

for i in range(num_orders):
    if i % 10000 == 0 and i > 0:
        print(f'  Processing order {i}/{num_orders}')
    
    num_items = random.randint(1, 5)
    order_total = 0.0
    
    for j in range(num_items):
        product = products_df.iloc[random.randint(0, len(products_df)-1)]
        quantity = random.randint(1, 3)
        discount = random.choice([0, 0.05, 0.10, 0.15])
        line_total = product['unit_price']  quantity  (1 - discount)
        order_total += line_total
        
        order_items.append({
            'order_item_id': len(order_items) + 1,
            'order_id': i + 1,
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': product['unit_price'],
            'discount': discount,
            'line_total': round(line_total, 2)
        })
    
     Update order total - using .loc to avoid dtype issues
    orders_df.loc[i, 'order_total'] = round(order_total, 2)

order_items_df = pd.DataFrame(order_items)

 Save to CSV
print('\nSaving files...')
customers_df.to_csv('data/customers.csv', index=False)
products_df.to_csv('data/products.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)
order_items_df.to_csv('data/order_items.csv', index=False)

print('\n✅ Dataset created successfully!')
print(f'Customers: {len(customers_df):,}')
print(f'Products: {len(products_df):,}')
print(f'Orders: {len(orders_df):,}')
print(f'Order Items: {len(order_items_df):,}')
print(f'Total Revenue: ${orders_df["order_total"].sum():,.2f}')