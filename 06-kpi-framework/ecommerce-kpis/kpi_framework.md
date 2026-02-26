📝 1. E-commerce KPI Framework



markdown

KPI Framework: E-Commerce Business Model



📊 Overview

This document defines key performance indicators for an e-commerce business, including metrics for sales, marketing, operations, and customer experience.



🎯 KPI Categories



1\. Sales Metrics - Revenue and transaction performance

2\. Marketing Metrics - Traffic and conversion

3\. Product Metrics - Catalog and inventory performance

4\. Customer Metrics - Behavior and loyalty

5\. Operational Metrics - Fulfillment and logistics





&nbsp;1. Sales Metrics



&nbsp;1.1 Gross Merchandise Value (GMV)

Definition: Total value of merchandise sold over a period.



Formula: GMV = SUM(Price × Quantity Sold)





SQL Calculation:

```sql

SELECT 

&nbsp;   DATE\_TRUNC('month', order\_date) AS month,

&nbsp;   SUM(quantity \* unit\_price) AS gmv,

&nbsp;   COUNT(DISTINCT order\_id) AS orders,

&nbsp;   AVG(quantity \* unit\_price) AS average\_order\_value

FROM orders

GROUP BY 1

ORDER BY 1 DESC;

Benchmark: Growth of 15-30% year-over-year



1.2 Average Order Value (AOV)

Definition: Average amount spent per order.



Formula: AOV = Total Revenue / Number of Orders

SQL Calculation:



sql

SELECT 

&nbsp;   DATE\_TRUNC('month', order\_date) AS month,

&nbsp;   ROUND(SUM(order\_total) / COUNT(DISTINCT order\_id), 2) AS aov,

&nbsp;   ROUND(AVG(order\_total), 2) AS avg\_order\_value\_alt

FROM orders

GROUP BY 1

ORDER BY 1;

Benchmark by Industry:



Industry	Average AOV

Fashion	$75-150

Electronics	$200-500

Home Goods	$100-250

Beauty	$40-80

Grocery	$50-120

1.3 Revenue by Category

Definition: Sales breakdown by product category.



SQL Calculation:



sql

SELECT 

&nbsp;   p.category,

&nbsp;   SUM(oi.quantity \* oi.unit\_price) AS revenue,

&nbsp;   SUM(oi.quantity) AS units\_sold,

&nbsp;   COUNT(DISTINCT o.order\_id) AS orders,

&nbsp;   ROUND(100.0 \* SUM(oi.quantity \* oi.unit\_price) / SUM(SUM(oi.quantity \* oi.unit\_price)) OVER (), 2) AS revenue\_pct

FROM orders o

JOIN order\_items oi ON o.order\_id = oi.order\_id

JOIN products p ON oi.product\_id = p.product\_id

WHERE o.order\_date >= '2024-01-01'

GROUP BY p.category

ORDER BY revenue DESC;

2\. Marketing Metrics

2.1 Conversion Rate (CVR)

Definition: Percentage of visitors who make a purchase.



Formula: CVR = (Number of Orders / Number of Website Visitors) × 100



Funnel Breakdown:



Stage	Metric	Typical Rate

Visitors → Product Views	Browse Rate	40-60%

Product Views → Add to Cart	Cart Addition Rate	10-30%

Add to Cart → Checkout	Checkout Start Rate	50-80%

Checkout → Purchase	Purchase Completion Rate	60-90%

Overall	Visitor → Purchase	1-4%

SQL Calculation:



sql

WITH funnel AS (

&nbsp;   SELECT 

&nbsp;       session\_id,

&nbsp;       MAX(CASE WHEN event\_type = 'page\_view' AND page = 'product' THEN 1 ELSE 0 END) AS viewed\_product,

&nbsp;       MAX(CASE WHEN event\_type = 'add\_to\_cart' THEN 1 ELSE 0 END) AS added\_to\_cart,

&nbsp;       MAX(CASE WHEN event\_type = 'checkout\_start' THEN 1 ELSE 0 END) AS started\_checkout,

&nbsp;       MAX(CASE WHEN event\_type = 'purchase' THEN 1 ELSE 0 END) AS purchased

&nbsp;   FROM user\_events

&nbsp;   WHERE event\_date >= '2024-01-01'

&nbsp;   GROUP BY session\_id

)

SELECT 

&nbsp;   COUNT(\*) AS total\_sessions,

&nbsp;   SUM(viewed\_product) AS product\_views,

&nbsp;   SUM(added\_to\_cart) AS cart\_adds,

&nbsp;   SUM(started\_checkout) AS checkouts,

&nbsp;   SUM(purchased) AS purchases,

&nbsp;   ROUND(100.0 \* SUM(purchased) / COUNT(\*), 2) AS overall\_conversion\_rate,

&nbsp;   ROUND(100.0 \* SUM(added\_to\_cart) / NULLIF(SUM(viewed\_product), 0), 2) AS view\_to\_cart\_rate,

&nbsp;   ROUND(100.0 \* SUM(purchased) / NULLIF(SUM(started\_checkout), 0), 2) AS checkout\_completion\_rate

FROM funnel;

2.2 Traffic by Channel

Definition: Website visitors segmented by acquisition channel.



Channel	Description	Typical CPC	Conversion Rate

Organic Search	SEO traffic	Free	2-5%

Paid Search	Google Ads	$1-5	2-4%

Social Media	Instagram, Facebook	$0.50-3	1-3%

Email Marketing	Newsletters	$0.10-1	3-8%

Direct	Type-in/Bookmark	Free	3-6%

Referral	Links from other sites	Free	2-5%

2.3 Return on Ad Spend (ROAS)

Definition: Revenue generated per dollar spent on advertising.



Formula: ROAS = Revenue from Campaign / Ad Spend

Benchmark:



Good: > 4.0 (400% return)



Average: 2.5 - 4.0



Poor: < 2.0



SQL Calculation:



sql

SELECT 

&nbsp;   campaign\_name,

&nbsp;   SUM(revenue) AS attributed\_revenue,

&nbsp;   SUM(ad\_spend) AS total\_spend,

&nbsp;   ROUND(SUM(revenue) / NULLIF(SUM(ad\_spend), 0), 2) AS roas

FROM marketing\_campaigns

GROUP BY campaign\_name

ORDER BY roas DESC;

3\. Product Metrics

3.1 Top Selling Products

Definition: Products with highest sales volume.



SQL Calculation:



sql

SELECT 

&nbsp;   p.product\_name,

&nbsp;   p.category,

&nbsp;   SUM(oi.quantity) AS units\_sold,

&nbsp;   SUM(oi.quantity \* oi.unit\_price) AS revenue,

&nbsp;   COUNT(DISTINCT o.order\_id) AS orders,

&nbsp;   AVG(oi.unit\_price) AS avg\_price

FROM order\_items oi

JOIN products p ON oi.product\_id = p.product\_id

JOIN orders o ON oi.order\_id = o.order\_id

WHERE o.order\_date >= DATEADD('month', -3, CURRENT\_DATE)

GROUP BY p.product\_name, p.category

ORDER BY revenue DESC

LIMIT 20;

3.2 Inventory Turnover

Definition: How quickly inventory is sold.



Formula: Inventory Turnover = Cost of Goods Sold / Average Inventory Value

Benchmark by Industry:



Industry	Turns/Year

Fashion	4-6

Electronics	6-8

Grocery	12-20

Furniture	2-4

3.3 Stockout Rate

Definition: Percentage of time products are out of stock.



Formula: Stockout Rate = (Days Out of Stock / Total Days) × 100

&nbsp;

4\. Customer Metrics

4.1 Repeat Purchase Rate

Definition: Percentage of customers who make more than one purchase.



Formula: Repeat Purchase Rate = (Customers with 2+ Orders / Total Customers) × 100

SQL Calculation:



sql

WITH customer\_orders AS (

&nbsp;   SELECT 

&nbsp;       customer\_id,

&nbsp;       COUNT(DISTINCT order\_id) AS order\_count

&nbsp;   FROM orders

&nbsp;   GROUP BY customer\_id

)

SELECT 

&nbsp;   COUNT(\*) AS total\_customers,

&nbsp;   SUM(CASE WHEN order\_count >= 2 THEN 1 ELSE 0 END) AS repeat\_customers,

&nbsp;   ROUND(100.0 \* SUM(CASE WHEN order\_count >= 2 THEN 1 ELSE 0 END) / COUNT(\*), 2) AS repeat\_rate

FROM customer\_orders;

Benchmark: 20-40% is healthy



4.2 Customer Lifetime Value (E-commerce)

Definition: Total revenue from a customer over their relationship.



Formula: LTV = Average Order Value × Purchase Frequency × Customer Lifespan

4.3 Cart Abandonment Rate

Definition: Percentage of users who add items to cart but don't purchase.



Formula: Cart Abandonment Rate = (1 - (Purchases / Cart Adds)) × 100

Benchmark: 60-80% is typical



5\. Operational Metrics

5.1 Order Fulfillment Time

Definition: Time from order to delivery.



SQL Calculation:



sql

SELECT 

&nbsp;   AVG(DATEDIFF('day', order\_date, delivery\_date)) AS avg\_fulfillment\_days,

&nbsp;   PERCENTILE\_CONT(0.5) WITHIN GROUP (ORDER BY DATEDIFF('day', order\_date, delivery\_date)) AS median\_fulfillment\_days

FROM orders

WHERE delivery\_date IS NOT NULL;

Benchmark:



Standard: 3-5 days



Express: 1-2 days



Premium: Same/Next day



5.2 Return Rate

Definition: Percentage of orders returned.



Formula: Return Rate = (Number of Returned Orders / Total Orders) × 100

Benchmark by Category:



Category	Return Rate

Fashion	20-40%

Electronics	5-10%

Home Goods	5-15%

Beauty	5-10%

📊 KPI Dashboard Mockup

text

┌─────────────────────────────────────────────────────────────┐

│  E-COMMERCE DASHBOARD                           Q1 2024    │

├───────────────┬───────────────┬───────────────┬─────────────┤

│   GMV         │   AOV         │   CVR         │   ROAS      │

│   $1.2M       │   $85.50      │   3.2%        │   4.5x      │

│   ▲ 15% YoY   │   ▼ 2% YoY    │   ▲ 0.3pp     │   ▲ 0.5x    │

├───────────────┴───────────────┴───────────────┴─────────────┤

│                                                             │

│  Sales Trend                                                │

│  ┌────────────────────────────────────────────────────┐    │

│  │                                                    │    │

│  │         Daily/Weekly/Monthly Revenue Chart        │    │

│  │                                                    │    │

│  └────────────────────────────────────────────────────┘    │

├───────────────┬─────────────────────────────────────────────┤

│  Top Products │  Traffic by Channel                         │

│  ┌─────────┐  │  ┌────────────────────────────────────┐    │

│  │ 1. iPhone│  │  │                                    │    │

│  │ 2. Laptop│  │  │  Pie/Bar chart: Sessions by       │    │

│  │ 3. Headphones│  │  Organic, Paid, Social, Email    │    │

│  └─────────┘  │  │                                    │    │

│               │  └────────────────────────────────────┘    │

│  Category     │                                             │

│  Performance  │  ┌────────────────────────────────────┐    │

│  ┌─────────┐  │  │                                    │    │

│  │Electronics│  │  │  Conversion Rate by Device       │    │

│  │Clothing   │  │  │  Desktop vs Mobile vs Tablet     │    │

│  │Home       │  │  │                                    │    │

│  └─────────┘  │  └────────────────────────────────────┘    │

└───────────────┴─────────────────────────────────────────────┘



✅ E-commerce KPI Checklist

&nbsp;   KPI	                Defined	Formula	SQL	Benchmark	Dashboard

GMV	                   ✅	   ✅	✅	    ✅	          ✅

AOV	                   ✅	   ✅	✅	    ✅	          ✅

Conversion Rate	           ✅	   ✅	✅	    ✅	          ✅

Traffic by Channel	   ✅	   ✅	✅	    ✅	          ⬜

ROAS	                   ✅	   ✅	✅	    ✅	          ✅

Top Products	           ✅	   ✅	✅	    ✅	  	  ✅

Inventory Turnover	   ✅	   ✅	⬜	    ✅	          ⬜

Repeat Rate	           ✅	   ✅	✅	    ✅		  ✅

Cart Abandonment	   ✅	   ✅	✅ 	    ✅         	  ⬜

Return Rate	           ✅	   ✅	⬜	    ✅		  ⬜



