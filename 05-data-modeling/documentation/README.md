&nbsp;Data Warehouse Design Project



&nbsp;📋 Overview

This project demonstrates a complete star schema data warehouse design for an e-commerce business, following Kimball's dimensional modeling principles.



&nbsp;🏗️ Project Structure

05-data-modeling/

├── star-schema/

│ ├── star\_schema\_design.md  Complete schema documentation

│ ├── dim\_customer.sql  Customer dimension DDL

│ ├── dim\_product.sql  Product dimension DDL

│ ├── dim\_date.sql  Date dimension DDL

│ ├── dim\_store.sql  Store dimension DDL

│ └── fact\_sales.sql  Sales fact table DDL

├── data-models/

│ └── generate\_sample\_data.py  Script to generate sample data

├── etl-scripts/

│ └── etl\_pipeline.py  Python ETL pipeline example

├── images/

│ └── star\_schema\_diagram.png  Visual schema diagram

└── documentation/

└── README.md  This file





&nbsp;🎯 Key Features



&nbsp;Star Schema Design

\- Fact Table: `fact\_sales` at line-item granularity

\- Dimension Tables: `customer`, `product`, `date`, `store`, `promotion`

\- SCD Types: Type 2 for customer, Type 1 for product

\- Surrogate Keys: All dimensions use integer surrogate keys



&nbsp;Data Modeling Best Practices

\- ✅ Conformed dimensions for consistency

\- ✅ Degenerate dimensions (order\_id in fact table)

\- ✅ Audit columns for data lineage

\- ✅ Proper indexing strategy

\- ✅ Partitioning recommendations



&nbsp;ETL Pipeline

\- Extract from source systems

\- Transform with business logic

\- Load with SCD handling

\- Error handling and logging

\- Performance optimization



&nbsp;📊 Sample Business Queries



&nbsp;Monthly Sales by Category

```sql

SELECT 

&nbsp;   d.year,

&nbsp;   d.month\_name,

&nbsp;   p.category,

&nbsp;   SUM(f.sales\_amount) AS total\_sales

FROM fact\_sales f

JOIN dim\_date d ON f.date\_key = d.date\_key

JOIN dim\_product p ON f.product\_key = p.product\_key

GROUP BY d.year, d.month\_name, p.category;



Customer Lifetime Value

sql

SELECT 

&nbsp;   c.customer\_segment,

&nbsp;   COUNT(DISTINCT c.customer\_key) AS customers,

&nbsp;   SUM(f.sales\_amount) / COUNT(DISTINCT c.customer\_key) AS avg\_ltv

FROM fact\_sales f

JOIN dim\_customer c ON f.customer\_key = c.customer\_key

WHERE c.is\_current = TRUE

GROUP BY c.customer\_segment;



🛠️ Technologies

SQL (DDL, DML)



Python (ETL)



Star Schema Modeling



Slowly Changing Dimensions



Data Warehousing Concepts

👨‍💻 Author

Victor Makanju

