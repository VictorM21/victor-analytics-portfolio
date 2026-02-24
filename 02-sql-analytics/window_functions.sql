-- ======================================================
-- Rolling Averages and Trends
-- ======================================================
-- Skill: Window functions, moving averages, LEAD/LAG

WITH daily_sales AS (
    SELECT 
        order_date,
        SUM(order_amount) AS daily_revenue,
        COUNT(DISTINCT order_id) AS daily_orders,
        COUNT(DISTINCT customer_id) AS daily_customers
    FROM orders
    GROUP BY order_date
)

SELECT 
    order_date,
    daily_revenue,
    daily_orders,
    daily_customers,
    -- 7-day rolling averages
    AVG(daily_revenue) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_7day_avg,
    AVG(daily_orders) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS orders_7day_avg,
    -- Compare to previous day
    LAG(daily_revenue, 1) OVER (ORDER BY order_date) AS prev_day_revenue,
    LAG(daily_revenue, 7) OVER (ORDER BY order_date) AS prev_week_revenue,
    -- Calculate changes
    ROUND(100.0 * (daily_revenue - LAG(daily_revenue, 1) OVER (ORDER BY order_date)) / 
          NULLIF(LAG(daily_revenue, 1) OVER (ORDER BY order_date), 0), 2) AS day_over_day_pct,
    -- Rank best sales days
    RANK() OVER (ORDER BY daily_revenue DESC) AS revenue_rank
FROM daily_sales
ORDER BY order_date;

-- This demonstrates advanced window functions for time series analysis
