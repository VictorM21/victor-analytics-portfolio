-- ======================================================
-- DIM_PRODUCT (Type 1 Slowly Changing Dimension)
-- ======================================================

CREATE TABLE dim_product (
    -- Surrogate key
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Natural key from source
    product_id VARCHAR(50) NOT NULL UNIQUE,
    
    -- Product attributes
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    supplier VARCHAR(100),
    unit_price DECIMAL(10,2),
    unit_cost DECIMAL(10,2),
    weight_kg DECIMAL(5,2),
    
    -- Status flags
    is_active BOOLEAN DEFAULT TRUE,
    launched_date DATE,
    discontinued_date DATE,
    
    -- Audit columns
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP,
    
    -- Check constraints
    CONSTRAINT chk_product_price CHECK (unit_price >= 0),
    CONSTRAINT chk_product_cost CHECK (unit_cost >= 0)
);

-- Create indexes
CREATE INDEX idx_product_category ON dim_product(category);
CREATE INDEX idx_product_brand ON dim_product(brand);
CREATE INDEX idx_product_active ON dim_product(is_active);

-- Comments
COMMENT ON TABLE dim_product IS 'Product dimension (Type 1 SCD - overwrites changes)';
COMMENT ON COLUMN dim_product.product_key IS 'Surrogate key for product dimension';
COMMENT ON COLUMN dim_product.product_id IS 'Natural key from source system';
COMMENT ON COLUMN dim_product.unit_price IS 'Current selling price';
COMMENT ON COLUMN dim_product.unit_cost IS 'Current cost from supplier';