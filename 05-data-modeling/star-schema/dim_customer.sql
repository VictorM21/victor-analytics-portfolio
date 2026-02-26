-- ======================================================
-- DIM_CUSTOMER (Type 2 Slowly Changing Dimension)
-- ======================================================

CREATE TABLE dim_customer (
    -- Surrogate key
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Natural key from source
    customer_id VARCHAR(50) NOT NULL,
    
    -- Customer attributes
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address_line1 VARCHAR(200),
    address_line2 VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50) DEFAULT 'USA',
    customer_segment VARCHAR(50),
    registration_date DATE,
    
    -- SCD Type 2 tracking columns
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    
    -- Audit columns
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP,
    
    -- Business rules
    CONSTRAINT uk_customer_id_valid_from UNIQUE (customer_id, valid_from)
);

-- Create indexes for performance
CREATE INDEX idx_customer_email ON dim_customer(email);
CREATE INDEX idx_customer_segment ON dim_customer(customer_segment);
CREATE INDEX idx_customer_current ON dim_customer(is_current);

-- Comment on table and columns
COMMENT ON TABLE dim_customer IS 'Customer dimension with Type 2 SCD for tracking historical changes';
COMMENT ON COLUMN dim_customer.customer_key IS 'Surrogate key for customer dimension';
COMMENT ON COLUMN dim_customer.customer_id IS 'Natural key from source system';
COMMENT ON COLUMN dim_customer.valid_from IS 'Date when this version became active';
COMMENT ON COLUMN dim_customer.valid_to IS 'Date when this version expired (9999-12-31 for current)';
COMMENT ON COLUMN dim_customer.is_current IS 'Flag indicating if this is the current version';