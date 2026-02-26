-- ======================================================
-- FACT_SALES (Sales Fact Table)
-- ======================================================

CREATE TABLE fact_sales (
    -- Surrogate key
    sales_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign keys to dimensions
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL,
    promotion_key INT,
    
    -- Degenerate dimensions
    order_id VARCHAR(50) NOT NULL,
    line_item_id INT NOT NULL,
    
    -- Measures
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    sales_amount DECIMAL(10,2) NOT NULL,
    cost_amount DECIMAL(10,2) NOT NULL,
    profit_amount DECIMAL(10,2) NOT NULL,
    margin_percent DECIMAL(5,2),
    
    -- Timestamp for time-of-day analysis
    order_timestamp TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_fact_date FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    CONSTRAINT fk_fact_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_fact_product FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    CONSTRAINT fk_fact_store FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    CONSTRAINT fk_fact_promotion FOREIGN KEY (promotion_key) REFERENCES dim_promotion(promotion_key),
    
    -- Business constraints
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_sales_amount CHECK (sales_amount >= 0),
    CONSTRAINT chk_discount CHECK (discount_amount >= 0),
    CONSTRAINT uk_order_line UNIQUE (order_id, line_item_id)
);

-- Create indexes for performance
CREATE INDEX idx_fact_date ON fact_sales(date_key);
CREATE INDEX idx_fact_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_product ON fact_sales(product_key);
CREATE INDEX idx_fact_store ON fact_sales(store_key);
CREATE INDEX idx_fact_order ON fact_sales(order_id);

-- For partitioned tables (if using Snowflake/BigQuery)
-- PARTITION BY RANGE (date_key)
-- CLUSTER BY customer_key, product_key

-- Comments
COMMENT ON TABLE fact_sales IS 'Sales fact table at line item granularity';
COMMENT ON COLUMN fact_sales.sales_key IS 'Surrogate key for fact table';
COMMENT ON COLUMN fact_sales.sales_amount IS 'Final amount after discount';
COMMENT ON COLUMN fact_sales.profit_amount IS 'Sales amount minus cost amount';