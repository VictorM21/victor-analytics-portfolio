-- ======================================================
-- DIM_DATE (Date Dimension)
-- ======================================================

CREATE TABLE dim_date (
    -- Surrogate key (YYYYMMDD format)
    date_key INT PRIMARY KEY,
    
    -- Date attributes
    full_date DATE NOT NULL UNIQUE,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    
    -- Flag attributes
    is_weekend BOOLEAN DEFAULT FALSE,
    is_holiday BOOLEAN DEFAULT FALSE,
    holiday_name VARCHAR(100),
    
    -- Fiscal attributes (if different from calendar)
    fiscal_year INT,
    fiscal_quarter INT,
    fiscal_period INT,
    
    -- Constraints
    CONSTRAINT chk_month CHECK (month BETWEEN 1 AND 12),
    CONSTRAINT chk_quarter CHECK (quarter BETWEEN 1 AND 4),
    CONSTRAINT chk_day_of_week CHECK (day_of_week BETWEEN 1 AND 7)
);

-- Create indexes
CREATE INDEX idx_date_year ON dim_date(year);
CREATE INDEX idx_date_month ON dim_date(year, month);
CREATE INDEX idx_date_week ON dim_date(year, week);

-- Comments
COMMENT ON TABLE dim_date IS 'Date dimension for time-based analysis';
COMMENT ON COLUMN dim_date.date_key IS 'Surrogate key in YYYYMMDD format';
COMMENT ON COLUMN dim_date.full_date IS 'Calendar date';
COMMENT ON COLUMN dim_date.is_weekend IS 'TRUE for Saturday and Sunday';

-- Populate date dimension (example for 5 years)
-- Run this as a separate script or use a date generator