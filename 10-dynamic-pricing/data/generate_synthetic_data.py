"""
Synthetic Data Generator for Electronics Dynamic Pricing
Author: Victor Makanju

This script generates realistic e-commerce sales data for electronics products
using Negative Binomial distribution to model over-dispersed sales patterns.

Key Features:
- 50 products across 5 categories (Laptops, Smartphones, Headphones, Tablets, Accessories)
- 2 years of daily sales (2024-2025)
- Realistic price elasticity curves
- Weekend and holiday seasonality
- Competitor price fluctuations
- Product lifecycle decay
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# =============================================
# CONFIGURATION
# =============================================

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
NUM_PRODUCTS = 50

# Product categories with their price ranges and elasticity
PRODUCT_CATEGORIES = {
    'Laptops': {'base_price_range': (500, 2500), 'elasticity': -1.8, 'decay_rate': 0.001},
    'Smartphones': {'base_price_range': (400, 1200), 'elasticity': -1.5, 'decay_rate': 0.002},
    'Headphones': {'base_price_range': (50, 350), 'elasticity': -1.2, 'decay_rate': 0.0005},
    'Tablets': {'base_price_range': (200, 800), 'elasticity': -1.4, 'decay_rate': 0.0015},
    'Accessories': {'base_price_range': (10, 100), 'elasticity': -0.8, 'decay_rate': 0.0002}
}

# Holidays with demand multipliers
HOLIDAYS = {
    '2024-11-29': 2.5,  # Black Friday 2024
    '2024-12-02': 2.0,  # Cyber Monday 2024
    '2024-12-25': 1.8,  # Christmas 2024
    '2025-11-28': 2.5,  # Black Friday 2025
    '2025-12-01': 2.0,  # Cyber Monday 2025
    '2025-12-25': 1.8,  # Christmas 2025
}

# =============================================
# PRODUCT GENERATION
# =============================================

def generate_products():
    """Create 50 realistic electronics products"""
    products = []
    
    for i in range(1, NUM_PRODUCTS + 1):
        # Assign category with weighted distribution (more laptops/phones)
        category = random.choices(
            list(PRODUCT_CATEGORIES.keys()),
            weights=[0.3, 0.3, 0.15, 0.15, 0.1]
        )[0]
        
        cat_config = PRODUCT_CATEGORIES[category]
        
        # Generate base price from category range
        base_price = round(random.uniform(*cat_config['base_price_range']), 2)
        
        # Cost is typically 40-60% of price
        cost = round(base_price * random.uniform(0.4, 0.6), 2)
        
        # Release date (staggered over past 3 years)
        days_ago = random.randint(30, 1000)
        release_date = (END_DATE - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        products.append({
            'product_id': f'P{i:04d}',
            'product_name': f"{category} {random.choice(['Pro', 'Air', 'Max', 'Elite', 'Basic'])} {random.randint(1, 100)}",
            'category': category,
            'base_price': base_price,
            'cost': cost,
            'elasticity': cat_config['elasticity'],
            'decay_rate': cat_config['decay_rate'],
            'release_date': release_date,
            'brand': random.choice(['TechBrand', 'ElectroMax', 'GadgetPro', 'InnoTech', 'SmartLife'])
        })
    
    return pd.DataFrame(products)

# =============================================
# SALES GENERATION
# =============================================

def calculate_expected_sales(base_demand, price, base_price, elasticity, 
                            day_of_week, is_holiday, holiday_multiplier,
                            days_since_release, decay_rate, competitor_price):
    """
    Calculate expected sales using Negative Binomial parameters
    
    This is the "ground truth" demand function that our model will try to learn.
    """
    
    # 1. Price elasticity effect
    price_ratio = price / base_price
    price_effect = price_ratio ** elasticity  # Negative elasticity reduces demand
    
    # 2. Day of week effect (weekends = higher demand)
    dow_effect = 1.5 if day_of_week >= 5 else 1.0  # Saturday/Sunday = 1.5x
    
    # 3. Holiday effect
    holiday_effect = holiday_multiplier if is_holiday else 1.0
    
    # 4. Product lifecycle effect (older products sell less)
    lifecycle_effect = np.exp(-decay_rate * days_since_release)
    
    # 5. Competitor effect (if competitor is cheaper, we lose sales)
    if competitor_price < price:
        competitor_effect = 1 - min(0.5, (price - competitor_price) / price)
    else:
        competitor_effect = 1.0
    
    # Combine all effects (multiplicative model)
    expected_sales = (base_demand * price_effect * dow_effect * 
                     holiday_effect * lifecycle_effect * competitor_effect)
    
    return max(0.1, expected_sales)  # Never go below 0.1 expected sales

def generate_sales(products_df):
    """Generate 2 years of daily sales data"""
    
    all_sales = []
    date_range = pd.date_range(START_DATE, END_DATE)
    
    print(f"📊 Generating sales for {len(date_range)} days...")
    
    for idx, date in enumerate(date_range):
        if idx % 100 == 0:
            print(f"   Progress: {idx}/{len(date_range)} days")
        
        year = date.year
        month = date.month
        day_of_week = date.dayofweek  # 0=Monday, 6=Sunday
        date_str = date.strftime('%Y-%m-%d')
        
        # Check if holiday
        is_holiday = date_str in HOLIDAYS
        holiday_multiplier = HOLIDAYS.get(date_str, 1.0)
        
        # December boost (holiday shopping)
        if month == 12 and not is_holiday:
            holiday_multiplier = 1.4
        
        for _, product in products_df.iterrows():
            # Calculate product age
            release_date = datetime.strptime(product['release_date'], '%Y-%m-%d')
            days_since_release = (date - release_date).days
            if days_since_release < 0:
                continue  # Product not yet released
            
            # Base price (can be adjusted for promotions)
            base_price = product['base_price']
            
            # Simulate competitor price (random fluctuation around our price)
            competitor_price = base_price * random.uniform(0.85, 1.15)
            
            # Our actual price (could be varied for training data)
            # For training, we'll use a range of prices to learn elasticity
            price_multiplier = random.choice([0.9, 0.95, 1.0, 1.05, 1.1])
            our_price = round(base_price * price_multiplier, 2)
            
            # Base demand for this product category
            category_base_demand = {
                'Laptops': 5,
                'Smartphones': 8,
                'Headphones': 12,
                'Tablets': 6,
                'Accessories': 20
            }[product['category']]
            
            # Calculate expected sales
            expected = calculate_expected_sales(
                base_demand=category_base_demand,
                price=our_price,
                base_price=base_price,
                elasticity=product['elasticity'],
                day_of_week=day_of_week,
                is_holiday=is_holiday,
                holiday_multiplier=holiday_multiplier,
                days_since_release=days_since_release,
                decay_rate=product['decay_rate'],
                competitor_price=competitor_price
            )
            
            # Generate actual sales using Negative Binomial (over-dispersed count)
            # Size parameter controls over-dispersion (smaller = more over-dispersed)
            size_param = 2.0  # Adjust this to control variance
            p = size_param / (size_param + expected)
            # Ensure p is between 0 and 1
            p = max(0.01, min(0.99, p))
            actual_sales = np.random.negative_binomial(n=size_param, p=p)
            
            # Revenue and profit
            revenue = round(actual_sales * our_price, 2)
            profit = round(actual_sales * (our_price - product['cost']), 2)
            
            all_sales.append({
                'date': date_str,
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'category': product['category'],
                'brand': product['brand'],
                'days_since_release': days_since_release,
                'our_price': our_price,
                'competitor_price': round(competitor_price, 2),
                'price_diff': round(our_price - competitor_price, 2),
                'units_sold': int(actual_sales),
                'revenue': revenue,
                'cost': product['cost'],
                'profit': profit,
                'is_holiday': is_holiday,
                'holiday_multiplier': round(holiday_multiplier, 2),
                'day_of_week': date.strftime('%A'),
                'month': month,
                'year': year,
                'quarter': f"Q{(month-1)//3 + 1}"
            })
    
    return pd.DataFrame(all_sales)

# =============================================
# MAIN EXECUTION
# =============================================

def main():
    print("="*60)
    print("🚀 GENERATING SYNTHETIC ELECTRONICS SALES DATA")
    print("="*60)
    
    # Generate products
    print("\n📱 Generating product catalog...")
    products_df = generate_products()
    print(f"   ✅ Created {len(products_df)} products across 5 categories")
    
    # Save products
    os.makedirs('data/raw', exist_ok=True)
    products_df.to_csv('data/raw/products.csv', index=False)
    print(f"   ✅ Saved to data/raw/products.csv")
    
    # Generate sales
    print("\n💰 Generating sales data...")
    sales_df = generate_sales(products_df)
    print(f"   ✅ Generated {len(sales_df):,} sales records")
    
    # Save sales
    sales_df.to_csv('data/raw/sales_history.csv', index=False)
    print(f"   ✅ Saved to data/raw/sales_history.csv")
    
    # Summary statistics
    print("\n📊 DATA SUMMARY")
    print("-" * 40)
    print(f"Date range: {sales_df['date'].min()} to {sales_df['date'].max()}")
    print(f"Total revenue: ${sales_df['revenue'].sum():,.2f}")
    print(f"Total profit: ${sales_df['profit'].sum():,.2f}")
    print(f"Average units sold per day: {sales_df['units_sold'].mean():.1f}")
    print(f"Products with sales: {sales_df['product_id'].nunique()}")
    
    # Show sample
    print("\n📋 Sample data (first 5 rows):")
    print(sales_df[['date', 'product_id', 'our_price', 'competitor_price', 
                   'units_sold', 'profit']].head())
    
    print("\n" + "="*60)
    print("✅ DATA GENERATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()