-- ======================================================
-- SNOWFLAKE - CORRECTED QUERIES
-- ======================================================

-- 1. Time-Series Analysis with Window Functions
-- Demonstrates: Window frames, rolling calculations
SELECT 
    DATE_TRUNC('month', order_date::DATE) AS order_month,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(order_total), 2) AS revenue,
    -- 3-month rolling average
    ROUND(AVG(SUM(order_total)) OVER (
        ORDER BY DATE_TRUNC('month', order_date::DATE)
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS revenue_3month_avg,
    -- Year-over-year comparison
    LAG(ROUND(SUM(order_total), 2), 12) OVER (ORDER BY DATE_TRUNC('month', order_date::DATE)) AS revenue_prev_year,
    -- Percentage change
    ROUND(
        100.0 * (SUM(order_total) - LAG(SUM(order_total), 12) OVER (ORDER BY DATE_TRUNC('month', order_date::DATE))) /
        NULLIF(LAG(SUM(order_total), 12) OVER (ORDER BY DATE_TRUNC('month', order_date::DATE)), 0),
        2
    ) AS yoy_growth
FROM ANALYTICS_DB.SALES_SCHEMA.ORDERS
GROUP BY 1
ORDER BY 1;

-- 2. Customer Segmentation with NTILE
-- Demonstrates: Window functions, CASE statements, ranking
WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.customer_segment,
        COUNT(DISTINCT o.order_id) AS order_count,
        COALESCE(ROUND(SUM(o.order_total), 2), 0) AS total_spent,
        COALESCE(ROUND(AVG(o.order_total), 2), 0) AS avg_order_value,
        COALESCE(DATEDIFF('day', MAX(o.order_date::DATE), CURRENT_DATE()), 999) AS days_since_last
    FROM ANALYTICS_DB.SALES_SCHEMA.CUSTOMERS c
    LEFT JOIN ANALYTICS_DB.SALES_SCHEMA.ORDERS o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
)

SELECT 
    customer_id,
    customer_segment,
    order_count,
    total_spent,
    avg_order_value,
    days_since_last,
    NTILE(4) OVER (ORDER BY total_spent DESC) AS spend_quartile,
    NTILE(4) OVER (ORDER BY order_count DESC) AS frequency_quartile,
    NTILE(4) OVER (ORDER BY days_since_last) AS recency_quartile,
    -- Combined score
    ROUND((NTILE(4) OVER (ORDER BY total_spent DESC) + 
           NTILE(4) OVER (ORDER BY order_count DESC) + 
           NTILE(4) OVER (ORDER BY days_since_last)) / 3.0, 2) AS rfm_score
FROM customer_stats
WHERE total_spent > 0
ORDER BY rfm_score DESC
LIMIT 100;

-- 3. Snowflake-Specific: Time Travel Queries
-- Demonstrates: Snowflake's unique time travel feature
-- Query data as of 1 hour ago
WITH current_stats AS (
    SELECT 
        COUNT(*) AS current_orders, 
        ROUND(SUM(order_total), 2) AS current_revenue
    FROM ANALYTICS_DB.SALES_SCHEMA.ORDERS
),
past_stats AS (
    SELECT 
        COUNT(*) AS past_orders, 
        ROUND(SUM(order_total), 2) AS past_revenue
    FROM ANALYTICS_DB.SALES_SCHEMA.ORDERS AT(TIMESTAMP => DATEADD('hour', -1, CURRENT_TIMESTAMP()))
)
SELECT 
    current_orders,
    past_orders,
    ROUND(100.0 * (current_orders - past_orders) / NULLIF(past_orders, 0), 2) AS order_change_pct,
    current_revenue,
    past_revenue,
    ROUND(100.0 * (current_revenue - past_revenue) / NULLIF(past_revenue, 0), 2) AS revenue_change_pct
FROM current_stats, past_stats;

-- 4. Advanced Aggregation with GROUP BY CUBE
-- Demonstrates: Multi-level aggregations
SELECT 
    COALESCE(p.category, 'ALL') AS category,
    COALESCE(c.customer_segment, 'ALL') AS segment,
    COALESCE(c.region, 'ALL') AS region,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.order_total), 2) AS revenue,
    ROUND(AVG(o.order_total), 2) AS avg_order_value
FROM ANALYTICS_DB.SALES_SCHEMA.ORDERS o
JOIN ANALYTICS_DB.SALES_SCHEMA.CUSTOMERS c ON o.customer_id = c.customer_id
JOIN ANALYTICS_DB.SALES_SCHEMA.PRODUCTS p ON o.product_id = p.product_id
GROUP BY CUBE(p.category, c.customer_segment, c.region)
ORDER BY category, segment, region;

-- 5. Top Products by Revenue with Rank
-- Demonstrates: RANK() window function
WITH product_revenue AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue,
        RANK() OVER (PARTITION BY p.category ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) DESC) AS rank_in_category
    FROM ANALYTICS_DB.SALES_SCHEMA.PRODUCTS p
    JOIN ANALYTICS_DB.SALES_SCHEMA.ORDER_ITEMS oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category
)

SELECT 
    product_id,
    product_name,
    category,
    revenue,
    rank_in_category
FROM product_revenue
WHERE rank_in_category <= 5
ORDER BY category, rank_in_category;

-- 6. Monthly Active Users and Retention
-- Demonstrates: LAG() for retention calculation
WITH monthly_activity AS (
    SELECT 
        DATE_TRUNC('month', order_date::DATE) AS month,
        customer_id
    FROM ANALYTICS_DB.SALES_SCHEMA.ORDERS
    GROUP BY 1, 2
),

monthly_users AS (
    SELECT 
        month,
        COUNT(DISTINCT customer_id) AS active_users,
        COUNT(DISTINCT CASE WHEN LAG(month) OVER (PARTITION BY customer_id ORDER BY month) = DATEADD('month', -1, month) 
                       THEN customer_id END) AS retained_users
    FROM monthly_activity
    GROUP BY month
)

SELECT 
    month,
    active_users,
    retained_users,
    ROUND(100.0 * retained_users / NULLIF(active_users, 0), 2) AS retention_rate
FROM monthly_users
ORDER BY month;