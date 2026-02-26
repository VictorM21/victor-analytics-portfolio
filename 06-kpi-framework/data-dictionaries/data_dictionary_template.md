 Data Dictionary Template

 📋 Purpose
This template provides a standardized format for documenting data tables, columns, and business definitions. Use this template to create consistent documentation for all data assets in your data warehouse.

---

 [TABLE_NAME] Data Dictionary

 📊 Table Overview

| Attribute | Description |
|-----------|-------------|
| Table Name | `[schema_name.table_name]` |
| Display Name | [User-friendly table name] |
| Description | [Brief description of what this table contains and its business purpose] |
| Primary Key | `[column_name(s)]` |
| Foreign Keys | `[column_name]` → `[schema.referenced_table]` |
| Row Count | [Approximate number of rows, e.g., ~1.2M] |
| Update Frequency | [Daily, Hourly, Real-time, Batch, etc.] |
| Retention Period | [How long data is kept, e.g., 3 years] |
| Source System | [Source application, database, or external provider] |
| Business Owner | [Team or person responsible] |
| Data Steward | [Team or person managing data quality] |
| Criticality | [High/Medium/Low - business impact if unavailable] |

---

 🔑 Key Business Rules

| Rule ID | Description | Validation |
|---------|-------------|------------|
| BR-001 | [e.g., Order total must equal sum of line items] | Automated |
| BR-002 | [e.g., Order date cannot be in the future] | Automated |
| BR-003 | [e.g., Customer must exist before order can be placed] | Application-level |
| BR-004 | [e.g., Cancelled orders cannot be refunded twice] | Business process |

---

 📝 Column Definitions

| Column Name | Data Type | Required | Description | Example | Business Rules |
|-------------|-----------|----------|-------------|---------|----------------|
| `order_id` | VARCHAR(50) | Yes | Unique identifier for each order. Format: ORD-YYYY- where YYYY is year and  is sequential number | ORD-2024-123456 | Must be unique across all orders |
| `customer_id` | VARCHAR(50) | Yes | Foreign key to customers table. References `customers.customer_id` | CUST-67890 | Must exist in customers table |
| `order_date` | DATE | Yes | Date when order was placed in UTC | 2024-02-26 | Cannot be future date; must be >= customer registration date |
| `order_time` | TIME | No | Time when order was placed in UTC | 14:30:00 | Populated for real-time orders only |
| `order_timestamp` | TIMESTAMP | Yes | Full timestamp of order (date + time) | 2024-02-26 14:30:00 | Automatically generated |
| `order_total` | DECIMAL(10,2) | Yes | Total order amount after all discounts but before tax and shipping. Must equal sum of line items. | 125.99 | Must be ≥ 0; rounded to 2 decimals |
| `subtotal` | DECIMAL(10,2) | Yes | Order amount before discounts | 150.00 | Must be ≥ order_total |
| `discount_total` | DECIMAL(10,2) | Yes | Total discount applied to order | 24.01 | Must be ≥ 0 |
| `tax_amount` | DECIMAL(10,2) | Yes | Total tax applied | 10.50 | Calculated based on shipping address |
| `shipping_amount` | DECIMAL(10,2) | Yes | Shipping cost charged to customer | 5.99 | Based on shipping method |
| `grand_total` | DECIMAL(10,2) | Yes | Final amount including tax and shipping | 142.48 | = order_total + tax_amount + shipping_amount |
| `order_status` | VARCHAR(20) | Yes | Current status in order lifecycle | completed | Values: pending, processing, shipped, delivered, cancelled, returned, refunded |
| `payment_method` | VARCHAR(30) | No | Primary payment method used | credit_card | Values: credit_card, paypal, bank_transfer, gift_card, apple_pay, google_pay |
| `payment_status` | VARCHAR(20) | Yes | Status of payment processing | paid | Values: pending, authorized, paid, failed, refunded |
| `shipping_method` | VARCHAR(30) | No | Shipping service selected by customer | standard | Values: standard (3-5 days), express (2 days), next_day (1 day), same_day |
| `shipping_address_id` | VARCHAR(50) | No | Reference to shipping address | ADDR-78901 | Must exist in addresses table |
| `billing_address_id` | VARCHAR(50) | No | Reference to billing address | ADDR-78902 | Must exist in addresses table |
| `promotion_id` | VARCHAR(50) | No | Applied promotion code | SUMMER24 | May be NULL if no promotion |
| `channel` | VARCHAR(30) | No | Sales channel where order originated | website | Values: website, mobile_app, instore, marketplace, phone |
| `device_type` | VARCHAR(20) | No | Device used for online orders | desktop | Values: desktop, mobile, tablet, other |
| `is_first_order` | BOOLEAN | Yes | Flag indicating if this is customer's first order | TRUE | Calculated based on customer order history |
| `is_gift` | BOOLEAN | Yes | Whether order is marked as gift | FALSE | Default FALSE |
| `gift_message` | TEXT | No | Gift message if applicable | "Happy Birthday!" | Only populated when is_gift = TRUE |
| `notes` | TEXT | No | Internal order notes | "Customer requested signature" | For internal use only |
| `created_at` | TIMESTAMP | Yes | When record was created in source system | 2024-02-26 14:30:00 | Auto-populated by system |
| `created_by` | VARCHAR(50) | Yes | User or system that created the record | system | Could be user_id or 'system' |
| `updated_at` | TIMESTAMP | Yes | When record was last updated | 2024-02-27 09:15:00 | Auto-updated on any change |
| `updated_by` | VARCHAR(50) | Yes | User or system that last updated the record | john.doe@company.com | Tracks last modifier |
| `source_file` | VARCHAR(200) | No | Source file name if loaded from external file | orders_20240226.csv | For audit purposes |
| `load_timestamp` | TIMESTAMP | Yes | When record was loaded into warehouse | 2024-02-27 03:00:00 | For ETL tracking |

---

 🔗 Table Relationships

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    ORDER_ITEMS }o--|| PRODUCTS : includes
    ORDERS }o--|| ADDRESSES : ships_to
    ORDERS }o--|| PROMOTIONS : applies

Relationship Details

Relationship	From Table	To Table	Cardinality	Join Key			Description
places		customers	orders		One-to-Many	customer_id		A customer can place many orders
contains	orders		order_items	One-to-Many	order_id		An order contains one or more items
includes	order_items	products	Many-to-One	product_id		Each order item is for one product
ships_to	orders		addresses	Many-to-One	shipping_address_id	Orders ship to one address
applies		orders		promotions	Many-to-One	promotion_id		Orders may use one promotion

📊 Sample Data

order_id		customer_id	order_date	order_total	status		payment_method	channel
ORD-2024-123456	CUST-67890	2024-02-26	125.99		delivered	credit_card	website
ORD-2024-123457	CUST-12345	2024-02-26	79.50		shipped		paypal		mobile_app
ORD-2024-123458	CUST-45678	2024-02-25	245.00		processing	bank_transfer	website
ORD-2024-123459	CUST-78901	2024-02-25	32.99		delivered	gift_card	instore
ORD-2024-123460	CUST-23456	2024-02-24	599.99		cancelled	credit_card	website

🔍 Common Queries SQL
Get daily revenue for the last 30 days
SELECT 
    DATE(order_date) AS day,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(order_total) AS revenue,
    AVG(order_total) AS avg_order_value
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
    AND order_status IN ('delivered', 'shipped')
GROUP BY DATE(order_date)
ORDER BY day DESC;

Get revenue by channel for current month
SELECT 
    channel,
    COUNT(*) AS orders,
    SUM(order_total) AS revenue,
    ROUND(100.0 * SUM(order_total) / SUM(SUM(order_total)) OVER (), 2) AS revenue_pct
FROM orders
WHERE DATE_TRUNC('month', order_date) = DATE_TRUNC('month', CURRENT_DATE)
    AND order_status NOT IN ('cancelled')
GROUP BY channel
ORDER BY revenue DESC;

📈 Data Quality Metrics

Metric					Target	Current	Status			Notes
Completeness - payment_method		> 98%	97.5%	⚠️	2.5% missing payment methods
Completeness - shipping_method		> 95%	99.2%	✅	Good coverage
Uniqueness - order_id			100%	100%	✅	No duplicates found
Validity - order_total ≥ 0			100%	99.9%	⚠️	0.1% have negative values (credits?)
Freshness - max order_date			< 24h	2h	✅	Data is current
Referential integrity - customer_id	100%	99.8%	⚠️	0.2% orphaned orders

⚠️ Known Data Quality Issues

Issue ID		Description				Impact	                             Root Cause	                          Resolution Status		    	 	    Target Fix Date
DQ-001	~2% of orders have NULL payment_method	Low - affects payment method analysis	Legacy orders from 2023			Add default value 'unknown' in reporting layer		Q2 2024
DQ-002	Rare duplicate order_ids (0.01%)		High - inflates order counts		System glitch during high traffic		Deduplication logic added to ETL; fix deployed		Q1 2024
DQ-003	Future order_dates in some orders		Medium - affects time-based analysis	Timezone misconfiguration		Fixed in source; backfill scheduled			Q2 2024
DQ-004	Orphaned orders without customer_id	High - can't attribute to customers		Data deletion in source without cascade	Add referential integrity constraint			Q3 2024

📋 Validation Rules

Rule	Description														Query to Check										            Severity
V-001	Order total should equal sum of line items		      SELECT order_id FROM orders o JOIN (SELECT order_id, SUM(line_total) AS items_total FROM order_items GROUP BY 1) i ON o.order_id = i.order_id WHERE ABS(o.order_total - i.items_total) > 0.01	High
V-002	Order date cannot be in the future			      SELECT * FROM orders WHERE order_date > CURRENT_DATE																High
V-003	Cancelled orders should have cancellation_date populated SELECT * FROM orders WHERE order_status = 'cancelled' AND cancellation_date IS NULL											      Medium
V-004	Delivered orders must have delivery_date		      SELECT * FROM orders WHERE order_status = 'delivered' AND delivery_date IS NULL												      Medium

📚 Change History

Date	      Version	Change						Author		Approved By
2024-01-15	1.0	Initial creation			                Data Team	Product Owner
2024-02-20	1.1	Added payment_method values (apple_pay, google_pay)	Data Team	Product Owner
2024-03-01	1.2	Updated order_status enum (added 'refunded')	Data Team	Finance Team
2024-03-15	1.3	Added data quality metrics section			Data Steward	Data Architect
2024-04-01	1.4	Added validation rules				Data Engineer	Data Architect

👥 Stewardship Contacts

Role			Name/Team	    	Email			Slack Channel
Data Owner		Finance Team	 finance@company.com	 	#finance-data
Data Steward		Data Governance	 datasteward@company.com	 	#data-governance
Technical Contact	Data Engineering	 data-eng@company.com		#data-engineering
Business Contact		Sales Operations	 sales-ops@company.com		#sales-analytics
Source System Owner	Order Management	 orders-team@company.com		#order-system

🔒 Data Classification

Classification		Level						Description
Sensitivity		Internal				Contains business data but no PII
PII Present		No					No personally identifiable information
Confidential Data	No					Does not contain trade secrets or financial forecasts
Retention Policy		7 years					Meets legal requirements for transaction data
Access Restrictions	Finance, Sales, Analytics teams only	Role-based access control enforced

📊 Related Tables

Table Name	Schema		Description			Join Key
customers	sales		Customer master data		customer_id
order_items	sales	L	ine items for each order		order_id
products	inventory	Product catalog			product_id
addresses	customer	Customer addresses		address_id
promotions	marketing	Promotion codes and rules		promotion_id
payments	finance		Payment transactions		order_id
refunds		finance		Refund transactions		order_id
📝 Notes
This table is updated daily via ETL job at 3:00 AM UTC

Historical data is maintained for 7 years for compliance

For questions about this table, contact #data-engineering on Slack

When joining to this table, always use order_id for best performance

Consider using partitioned views for large date range queries

text

This comprehensive template includes:
- ✅ Table overview with metadata
- ✅ Column definitions with examples
- ✅ Business rules
- ✅ Relationships
- ✅ Sample data
- ✅ Common queries
- ✅ Data quality metrics
- ✅ Known issues
- ✅ Validation rules
- ✅ Change history
- ✅ Stewardship contacts
- ✅ Data classification


Get customer order history
SELECT 
    o.order_id,
    o.order_date,
    o.order_total,
    o.order_status,
    COUNT(oi.order_item_id) AS item_count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.customer_id = 'CUST-67890'
GROUP BY o.order_id, o.order_date, o.order_total, o.order_status
ORDER BY o.order_date DESC;

