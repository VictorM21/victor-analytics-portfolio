&nbsp;E-Commerce Data Warehouse: Star Schema Design



&nbsp;📊 Overview

This document outlines a star schema design for an e-commerce analytics data warehouse. The design follows Kimball's dimensional modeling principles for optimal query performance and business user understanding.



&nbsp;🎯 Business Process

Subject Area: Online Sales Transactions

Granularity: Individual line item per order

Process: Customer purchases products through the e-commerce platform



&nbsp;📐 Schema Diagram

&nbsp;                               +------------------+

&nbsp;                               |   DIM\_CUSTOMER   |

&nbsp;                               +------------------+

&nbsp;                                      |

&nbsp;                                      |

+------------------+ +------------------+ +------------------+

| DIM\_PRODUCT |-----| FACT\_SALES |-----| DIM\_DATE |

+------------------+ +------------------+ +------------------+

| |

| |

| +------------------+

|----| DIM\_STORE |

| +------------------+

|

| +------------------+

|----| DIM\_PROMOTION |

+------------------+

&nbsp;📋 Dimension Tables



&nbsp;1. DIM\_CUSTOMER (Type 2 Slowly Changing Dimension)

Tracks customer information with history for changes



| Column Name | Data Type | Description | Example |

|-------------|-----------|-------------|---------|

| customer\_key | INTEGER (PK) | Surrogate key | 10001 |

| customer\_id | VARCHAR(50) | Natural key from source | CUST-12345 |

| customer\_name | VARCHAR(100) | Full name | John Smith |

| email | VARCHAR(100) | Email address | john@email.com |

| phone | VARCHAR(20) | Contact number | 555-123-4567 |

| address\_line1 | VARCHAR(200) | Street address | 123 Main St |

| city | VARCHAR(50) | City | New York |

| state | VARCHAR(50) | State | NY |

| postal\_code | VARCHAR(20) | ZIP/Postal code | 10001 |

| country | VARCHAR(50) | Country | USA |

| customer\_segment | VARCHAR(50) | Segment | Premium |

| registration\_date | DATE | First registration | 2024-01-15 |

| valid\_from | DATE | SCD start date | 2024-01-15 |

| valid\_to | DATE | SCD end date | 9999-12-31 |

| is\_current | BOOLEAN | Current record flag | TRUE |

| created\_date | TIMESTAMP | Record creation | 2024-01-15 10:30:00 |



&nbsp;2. DIM\_PRODUCT

Product catalog information



| Column Name | Data Type | Description | Example |

|-------------|-----------|-------------|---------|

| product\_key | INTEGER (PK) | Surrogate key | 5001 |

| product\_id | VARCHAR(50) | Natural key from source | PROD-ELEC-001 |

| product\_name | VARCHAR(200) | Product name | iPhone 15 Pro |

| description | TEXT | Product description | 6.1-inch display... |

| category | VARCHAR(100) | Product category | Electronics |

| subcategory | VARCHAR(100) | Product subcategory | Smartphones |

| brand | VARCHAR(100) | Brand name | Apple |

| supplier | VARCHAR(100) | Supplier name | Foxconn |

| unit\_price | DECIMAL(10,2) | Current selling price | 999.99 |

| unit\_cost | DECIMAL(10,2) | Current cost | 699.99 |

| weight\_kg | DECIMAL(5,2) | Weight in kg | 0.25 |

| is\_active | BOOLEAN | Product active flag | TRUE |

| launched\_date | DATE | Product launch date | 2023-09-22 |



&nbsp;3. DIM\_DATE (Date Dimension)

Comprehensive date attributes for time-based analysis



| Column Name | Data Type | Description | Example |

|-------------|-----------|-------------|---------|

| date\_key | INTEGER (PK) | Surrogate key (YYYYMMDD) | 20240226 |

| full\_date | DATE | Calendar date | 2024-02-26 |

| year | INTEGER | Year | 2024 |

| quarter | INTEGER | Quarter (1-4) | 1 |

| month | INTEGER | Month (1-12) | 2 |

| month\_name | VARCHAR(20) | Month name | February |

| week | INTEGER | Week of year | 9 |

| day\_of\_month | INTEGER | Day of month | 26 |

| day\_of\_week | INTEGER | Day of week (1-7) | 2 |

| day\_name | VARCHAR(20) | Day name | Monday |

| is\_weekend | BOOLEAN | Weekend flag | FALSE |

| is\_holiday | BOOLEAN | Holiday flag | FALSE |

| fiscal\_year | INTEGER | Fiscal year | 2024 |

| fiscal\_quarter | INTEGER | Fiscal quarter | 3 |



&nbsp;4. DIM\_STORE

Store/branch information



| Column Name | Data Type | Description | Example |

|-------------|-----------|-------------|---------|

| store\_key | INTEGER (PK) | Surrogate key | 101 |

| store\_id | VARCHAR(50) | Natural key | STORE-NY-001 |

| store\_name | VARCHAR(100) | Store name | Manhattan Flagship |

| store\_type | VARCHAR(50) | Type | Flagship |

| address | VARCHAR(200) | Street address | 767 5th Ave |

| city | VARCHAR(50) | City | New York |

| state | VARCHAR(50) | State | NY |

| postal\_code | VARCHAR(20) | ZIP | 10153 |

| country | VARCHAR(50) | Country | USA |

| region | VARCHAR(50) | Sales region | Northeast |

| phone | VARCHAR(20) | Contact | 212-555-0123 |

| manager | VARCHAR(100) | Store manager | Jane Doe |

| opened\_date | DATE | Opening date | 2020-06-15 |

| is\_active | BOOLEAN | Active flag | TRUE |



&nbsp;5. DIM\_PROMOTION

Marketing promotion information



| Column Name | Data Type | Description | Example |

|-------------|-----------|-------------|---------|

| promotion\_key | INTEGER (PK) | Surrogate key | 2001 |

| promotion\_id | VARCHAR(50) | Natural key | PROMO-SUMMER-24 |

| promotion\_name | VARCHAR(200) | Promotion name | Summer Sale 2024 |

| promotion\_type | VARCHAR(50) | Type | Percentage Off |

| discount\_pct | DECIMAL(5,2) | Discount percentage | 15.00 |

| start\_date | DATE | Promotion start | 2024-06-01 |

| end\_date | DATE | Promotion end | 2024-08-31 |

| min\_purchase | DECIMAL(10,2) | Minimum purchase | 50.00 |

| applies\_to | VARCHAR(50) | All/Category/Product | Electronics |



&nbsp;📊 Fact Table: FACT\_SALES



| Column Name | Data Type | Description | Example |

|-------------|-----------|-------------|---------|

| sales\_key | INTEGER (PK) | Surrogate key | 10000001 |

| date\_key | INTEGER (FK) | Reference to DIM\_DATE | 20240226 |

| customer\_key | INTEGER (FK) | Reference to DIM\_CUSTOMER | 10001 |

| product\_key | INTEGER (FK) | Reference to DIM\_PRODUCT | 5001 |

| store\_key | INTEGER (FK) | Reference to DIM\_STORE | 101 |

| promotion\_key | INTEGER (FK) | Reference to DIM\_PROMOTION | 2001 |

| order\_id | VARCHAR(50) | Order number (degenerate dim) | ORD-2024-12345 |

| line\_item\_id | INTEGER | Line item number | 1 |

| quantity | INTEGER | Units sold | 2 |

| unit\_price | DECIMAL(10,2) | Price at time of sale | 999.99 |

| discount\_amount | DECIMAL(10,2) | Discount applied | 150.00 |

| sales\_amount | DECIMAL(10,2) | Final amount after discount | 1849.98 |

| cost\_amount | DECIMAL(10,2) | Cost of goods sold | 1399.98 |

| profit\_amount | DECIMAL(10,2) | Profit = sales - cost | 450.00 |

| margin\_percent | DECIMAL(5,2) | Profit margin % | 24.32 |

| order\_timestamp | TIMESTAMP | Date + time | 2024-02-26 14:30:00 |



&nbsp;🔄 Slowly Changing Dimensions (SCD) Strategy



| Dimension | SCD Type | Rationale |

|-----------|----------|-----------|

| DIM\_CUSTOMER | Type 2 | Track customer address/segment changes for historical accuracy |

| DIM\_PRODUCT | Type 1 | Overwrite price/cost changes (assume corrections) |

| DIM\_STORE | Type 1 | Store info rarely changes |

| DIM\_PROMOTION | Type 1 | Historical promotions not modified |



&nbsp;📈 Sample Business Queries



&nbsp;Query 1: Monthly Sales by Category

```sql

SELECT 

&nbsp;   d.year,

&nbsp;   d.month\_name,

&nbsp;   p.category,

&nbsp;   SUM(f.sales\_amount) AS total\_sales,

&nbsp;   SUM(f.quantity) AS units\_sold,

&nbsp;   COUNT(DISTINCT f.order\_id) AS orders

FROM FACT\_SALES f

JOIN DIM\_DATE d ON f.date\_key = d.date\_key

JOIN DIM\_PRODUCT p ON f.product\_key = p.product\_key

WHERE d.year = 2024

GROUP BY d.year, d.month\_name, p.category

ORDER BY d.month, total\_sales DESC;



Query 2: Customer Lifetime Value by Segment

sql



SELECT 

&nbsp;   c.customer\_segment,

&nbsp;   COUNT(DISTINCT c.customer\_key) AS customer\_count,

&nbsp;   SUM(f.sales\_amount) AS total\_revenue,

&nbsp;   SUM(f.profit\_amount) AS total\_profit,

&nbsp;   AVG(f.sales\_amount) AS avg\_order\_value,

&nbsp;   SUM(f.sales\_amount) / COUNT(DISTINCT c.customer\_key) AS ltv

FROM FACT\_SALES f

JOIN DIM\_CUSTOMER c ON f.customer\_key = c.customer\_key

WHERE c.is\_current = TRUE

GROUP BY c.customer\_segment

ORDER BY ltv DESC;



Partitioning Strategy

Partition FACT\_SALES by date\_key (monthly partitions)



Partition large dimensions by category (e.g., DIM\_PRODUCT by category)



Indexing Recommendations

sql

-- Clustered index on date\_key for time-based queries

CREATE CLUSTERED INDEX idx\_fact\_date ON FACT\_SALES(date\_key);



-- Non-clustered indexes for foreign keys

CREATE INDEX idx\_fact\_customer ON FACT\_SALES(customer\_key);

CREATE INDEX idx\_fact\_product ON FACT\_SALES(product\_key);

CREATE INDEX idx\_fact\_store ON FACT\_SALES(store\_key);

Best Practices Applied

Surrogate Keys: All dimensions use integer surrogate keys for better join performance



Conformed Dimensions: Date dimension reused across multiple fact tables



Consistent Naming: Clear, descriptive column names with prefixes



Audit Columns: Created\_date, modified\_date for data lineage



Degenerate Dimensions: Order\_id stored in fact table



SCD Management: Type 2 for tracking customer history



Referential Integrity: Foreign key relationships documented

