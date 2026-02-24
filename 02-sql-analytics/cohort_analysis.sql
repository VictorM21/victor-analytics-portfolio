-- ======================================================
-- Customer Cohort Analysis
-- ======================================================
-- Skill: Window functions, date manipulation, cohort retention

WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
),

cohort_size AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS customers
    FROM customer_cohorts
    GROUP BY cohort_month
),

cohort_activity AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS order_month,
        COUNT(DISTINCT o.customer_id) AS active_customers
    FROM orders o
    JOIN customer_cohorts c ON o.customer_id = c.customer_id
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)

SELECT 
    ca.cohort_month,
    ca.order_month,
    EXTRACT(MONTH FROM AGE(ca.order_month, ca.cohort_month)) AS months_since_first,
    ca.active_customers,
    cs.customers AS cohort_size,
    ROUND(100.0 * ca.active_customers / cs.customers, 2) AS retention_rate
FROM cohort_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
WHERE ca.order_month >= ca.cohort_month
ORDER BY ca.cohort_month, months_since_first;

-- This query shows how many customers from each signup month
-- continue to make purchases in subsequent months
