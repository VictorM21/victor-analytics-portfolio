"""
ETL Pipeline for Data Warehouse Loading
Author: Victor Makanju
Purpose: Demonstrate ETL process for star schema
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

 Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataWarehouseETL:
    """
    ETL pipeline for loading data warehouse
    """
    
    def __init__(self, source_connection, target_connection):
        self.source = source_connection
        self.target = target_connection
        self.logger = logging.getLogger(__name__)
        
    def extract(self, table_name, query=None):
        """
        Extract data from source system
        """
        self.logger.info(f"Extracting data from {table_name}")
        
        if query:
            df = pd.read_sql(query, self.source)
        else:
            df = pd.read_sql(f"SELECT  FROM {table_name}", self.source)
            
        self.logger.info(f"Extracted {len(df)} rows from {table_name}")
        return df
    
    def transform_customer(self, df):
        """
        Transform customer data for Type 2 SCD
        """
        self.logger.info("Transforming customer data")
        
         Add surrogate key if not present
        if 'customer_key' not in df.columns:
            df['customer_key'] = range(1, len(df) + 1)
        
         Handle SCD Type 2 columns
        df['valid_from'] = pd.to_datetime(df.get('registration_date', datetime.now()))
        df['valid_to'] = pd.to_datetime('9999-12-31')
        df['is_current'] = True
        
         Clean and standardize
        df['email'] = df['email'].str.lower().str.strip()
        df['customer_name'] = df['customer_name'].str.title()
        
         Add audit columns
        df['created_date'] = datetime.now()
        
        return df
    
    def transform_product(self, df):
        """
        Transform product data for Type 1 SCD
        """
        self.logger.info("Transforming product data")
        
         Add surrogate key
        if 'product_key' not in df.columns:
            df['product_key'] = range(1, len(df) + 1)
        
         Calculate derived fields
        df['margin_percent'] = ((df['unit_price'] - df['unit_cost']) / df['unit_price']  100).round(2)
        
         Categorize price points
        df['price_tier'] = pd.cut(
            df['unit_price'],
            bins=[0, 50, 200, 500, 10000],
            labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
        )
        
        return df
    
    def transform_sales(self, df_orders, df_order_items, df_products):
        """
        Transform sales data to fact table format
        """
        self.logger.info("Transforming sales data")
        
         Merge orders with order items
        fact_sales = df_order_items.merge(
            df_orders[['order_id', 'customer_id', 'order_date', 'store_id']],
            on='order_id',
            how='left'
        )
        
         Add product information
        fact_sales = fact_sales.merge(
            df_products[['product_id', 'unit_cost']],
            on='product_id',
            how='left'
        )
        
         Calculate measures
        fact_sales['sales_amount'] = fact_sales['quantity']  fact_sales['unit_price']  (1 - fact_sales['discount'])
        fact_sales['cost_amount'] = fact_sales['quantity']  fact_sales['unit_cost']
        fact_sales['profit_amount'] = fact_sales['sales_amount'] - fact_sales['cost_amount']
        fact_sales['margin_percent'] = (fact_sales['profit_amount'] / fact_sales['sales_amount']  100).round(2)
        
         Add date key (YYYYMMDD format)
        fact_sales['date_key'] = pd.to_datetime(fact_sales['order_date']).dt.strftime('%Y%m%d').astype(int)
        
        self.logger.info(f"Created fact table with {len(fact_sales)} rows")
        return fact_sales
    
    def load(self, df, table_name, if_exists='append'):
        """
        Load transformed data into warehouse
        """
        self.logger.info(f"Loading {len(df)} rows into {table_name}")
        
        df.to_sql(
            table_name,
            self.target,
            if_exists=if_exists,
            index=False,
            method='multi',
            chunksize=10000
        )
        
        self.logger.info(f"Successfully loaded data into {table_name}")
    
    def run_full_pipeline(self):
        """
        Execute complete ETL pipeline
        """
        self.logger.info("="  50)
        self.logger.info("STARTING ETL PIPELINE")
        self.logger.info("="  50)
        
        try:
             Extract
            customers = self.extract('source_customers')
            products = self.extract('source_products')
            orders = self.extract('source_orders')
            order_items = self.extract('source_order_items')
            
             Transform
            dim_customers = self.transform_customer(customers)
            dim_products = self.transform_product(products)
            fact_sales = self.transform_sales(orders, order_items, products)
            
             Load
            self.load(dim_customers, 'dim_customer', if_exists='replace')
            self.load(dim_products, 'dim_product', if_exists='replace')
            self.load(fact_sales, 'fact_sales', if_exists='replace')
            
            self.logger.info("="  50)
            self.logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
            self.logger.info("="  50)
            
            return {
                'customers_loaded': len(dim_customers),
                'products_loaded': len(dim_products),
                'fact_rows_loaded': len(fact_sales)
            }
            
        except Exception as e:
            self.logger.error(f"ETL pipeline failed: {str(e)}")
            raise

 Example usage
if __name__ == "__main__":
     This is a mock example - in production, use actual database connections
    import sqlite3
    
     Create in-memory SQLite databases for demonstration
    source_conn = sqlite3.connect(':memory:')
    target_conn = sqlite3.connect(':memory:')
    
     Initialize ETL
    etl = DataWarehouseETL(source_conn, target_conn)
    
    print("ETL pipeline ready for execution")
    print("Run etl.run_full_pipeline() to execute")