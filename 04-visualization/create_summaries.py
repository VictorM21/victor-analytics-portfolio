import pandas as pd

# Load the data
df = pd.read_csv('data/sales_data.csv')

# 1. Daily sales summary
daily_summary = df.groupby('order_date').agg({
    'sales_amount': 'sum',
    'profit_amount': 'sum',
    'order_id': 'nunique',
    'quantity': 'sum'
}).round(2).reset_index()
daily_summary.columns = ['Date', 'Total_Sales', 'Total_Profit', 'Order_Count', 'Total_Quantity']
daily_summary.to_csv('data/daily_summary.csv', index=False)

# 2. Monthly summary by category
monthly_category = df.groupby(['year', 'month', 'month_num', 'category']).agg({
    'sales_amount': 'sum',
    'profit_amount': 'sum',
    'order_id': 'nunique'
}).round(2).reset_index()
monthly_category = monthly_category.sort_values(['year', 'month_num'])
monthly_category.to_csv('data/monthly_category.csv', index=False)

# 3. Regional performance
regional = df.groupby('region').agg({
    'sales_amount': 'sum',
    'profit_amount': 'sum',
    'order_id': 'nunique',
    'customer_id': 'nunique'
}).round(2).reset_index()
regional['profit_margin'] = (regional['profit_amount'] / regional['sales_amount'] * 100).round(2)
regional.to_csv('data/regional_summary.csv', index=False)

# 4. Product performance
product_perf = df.groupby(['category', 'subcategory', 'product_name']).agg({
    'sales_amount': 'sum',
    'profit_amount': 'sum',
    'quantity': 'sum',
    'order_id': 'nunique'
}).round(2).reset_index()
product_perf['profit_margin'] = (product_perf['profit_amount'] / product_perf['sales_amount'] * 100).round(2)
product_perf = product_perf.sort_values('sales_amount', ascending=False)
product_perf.to_csv('data/product_performance.csv', index=False)

# 5. Customer segments
segment = df.groupby('customer_segment').agg({
    'sales_amount': 'sum',
    'profit_amount': 'sum',
    'order_id': 'nunique',
    'customer_id': 'nunique'
}).round(2).reset_index()
segment['avg_order_value'] = (segment['sales_amount'] / segment['order_id']).round(2)
segment.to_csv('data/customer_segments.csv', index=False)

print('Summary tables created successfully!')
print('\nFiles created:')
print('- daily_summary.csv')
print('- monthly_category.csv')
print('- regional_summary.csv')
print('- product_performance.csv')
print('- customer_segments.csv')
