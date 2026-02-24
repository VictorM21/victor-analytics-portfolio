-- ======================================================
-- GOOGLE BIGQUERY - CORRECTED QUERIES
-- ======================================================

-- 1. Monthly Sales Trends with YoY Comparison
-- Demonstrates: DATE functions, window functions, partitioning
SELECT 
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    FORMAT_DATE('%B', DATE(EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date), 1)) AS month_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(order_total), 2) AS revenue,
    ROUND(AVG(order_total), 2) AS avg_order_value,
    -- YoY Growth calculation
    ROUND(
        (SUM(order_total) - LAG(SUM(order_total)) OVER (
            PARTITION BY EXTRACT(MONTH FROM order_date) 
            ORDER BY EXTRACT(YEAR FROM order_date)
        )) / NULLIF(LAG(SUM(order_total)) OVER (
            PARTITION BY EXTRACT(MONTH FROM order_date) 
            ORDER BY EXTRACT(YEAR FROM order_date)
        ), 0) * 100, 2
    ) AS yoy_growth_percent
FROM `your-project.your_dataset.orders`
GROUP BY year, month
ORDER BY year, month;

-- 2. Customer Lifetime Value (LTV) Analysis
-- Demonstrates: CTEs, window functions, customer segmentation
WITH customer_metrics AS (
    SELECT 
        o.customer_id,
        c.customer_segment,
        c.registration_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(o.order_total), 2) AS monetary,
        DATE_DIFF(CURRENT_DATE(), MAX(DATE(o.order_date)), DAY) AS recency_days,
        MIN(DATE(o.order_date)) AS first_order,
        MAX(DATE(o.order_date)) AS last_order
    FROM `your-project.your_dataset.orders` o
    JOIN `your-project.your_dataset.customers` c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.customer_segment, c.registration_date
)

SELECT 
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(frequency), 2) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_ltv,
    ROUND(AVG(recency_days), 2) AS avg_recency_days,
    -- RFM-style segmentation
    CASE 
        WHEN AVG(monetary) >= 1000 THEN 'High Value'
        WHEN AVG(monetary) >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS value_segment
FROM customer_metrics
GROUP BY customer_segment
ORDER BY customer_segment, avg_ltv DESC;

-- 3. Product Affinity Analysis (Market Basket)
-- Demonstrates: Self-joins, association rules
WITH order_pairs AS (
    SELECT 
        a.order_id,
        a.product_id AS product_a,
        b.product_id AS product_b
    FROM `your-project.your_dataset.order_items` a
    JOIN `your-project.your_dataset.order_items` b 
        ON a.order_id = b.order_id 
        AND a.product_id < b.product_id
    WHERE a.order_id IS NOT NULL AND b.order_id IS NOT NULL
)

SELECT 
    p1.product_name AS product_1,
    p2.product_name AS product_2,
    COUNT(*) AS times_bought_together,
    ROUND(COUNT(*) / (SELECT COUNT(DISTINCT order_id) FROM `your-project.your_dataset.orders`), 4) AS purchase_probability
FROM order_pairs op
JOIN `your-project.your_dataset.products` p1 ON op.product_a = p1.product_id
JOIN `your-project.your_dataset.products` p2 ON op.product_b = p2.product_id
GROUP BY product_1, product_2
ORDER BY times_bought_together DESC
LIMIT 20;

-- 4. Cohort Retention Analysis
-- Demonstrates: Date truncation, cohort analysis
WITH cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC(MIN(DATE(order_date)), MONTH) AS cohort_month
    FROM `your-project.your_dataset.orders`
    GROUP BY customer_id
),

cohort_data AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC(DATE(o.order_date), MONTH) AS order_month,
        COUNT(DISTINCT o.customer_id) AS customers
    FROM `your-project.your_dataset.orders` o
    JOIN cohorts c ON o.customer_id = c.customer_id
    GROUP BY c.cohort_month, DATE_TRUNC(DATE(o.order_date), MONTH)
),

cohort_size AS (
    SELECT 
        cohort_month,
        customers AS size
    FROM cohort_data
    WHERE cohort_month = order_month
)

SELECT 
    FORMAT_DATE('%Y-%m', cd.cohort_month) AS cohort_month,
    FORMAT_DATE('%Y-%m', cd.order_month) AS order_month,
    DATE_DIFF(cd.order_month, cd.cohort_month, MONTH) AS months_since,
    cd.customers,
    cs.size AS cohort_size,
    ROUND(SAFE_DIVIDE(cd.customers, cs.size) * 100, 2) AS retention_rate
FROM cohort_data cd
JOIN cohort_size cs ON cd.cohort_month = cs.cohort_month
WHERE cd.order_month >= cd.cohort_month
ORDER BY cd.cohort_month, months_since;

-- 5. Customer Segmentation with Percentiles
-- Demonstrates: NTILE window function
WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.customer_segment,
        COUNT(DISTINCT o.order_id) AS order_count,
        ROUND(SUM(IFNULL(o.order_total, 0)), 2) AS total_spent,
        ROUND(AVG(IFNULL(o.order_total, 0)), 2) AS avg_order_value,
        DATE_DIFF(CURRENT_DATE(), MAX(DATE(o.order_date)), DAY) AS days_since_last
    FROM `your-project.your_dataset.customers` c
    LEFT JOIN `your-project.your_dataset.orders` o ON c.customer_id = o.customer_id
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
    ROUND((NTILE(4) OVER (ORDER BY total_spent DESC) + 
           NTILE(4) OVER (ORDER BY order_count DESC) + 
           NTILE(4) OVER (ORDER BY days_since_last)) / 3.0, 2) AS rfm_score
FROM customer_stats
WHERE total_spent > 0
ORDER BY rfm_score DESC
LIMIT 100;