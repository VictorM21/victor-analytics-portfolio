-- ======================================================
-- Marketing Funnel Analysis
-- ======================================================
-- Skill: Subqueries, conditional aggregation, conversion rates

WITH funnel_stages AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) AS viewed_product,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) AS started_checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM user_events
    WHERE event_date BETWEEN '2024-01-01' AND '2024-12-31'
    GROUP BY user_id
)

SELECT 
    COUNT(*) AS total_users,
    SUM(viewed_product) AS viewed_product,
    SUM(added_to_cart) AS added_to_cart,
    SUM(started_checkout) AS started_checkout,
    SUM(purchased) AS purchased,
    -- Conversion rates
    ROUND(100.0 * SUM(viewed_product) / COUNT(*), 2) AS view_rate,
    ROUND(100.0 * SUM(added_to_cart) / SUM(viewed_product), 2) AS cart_rate,
    ROUND(100.0 * SUM(started_checkout) / SUM(added_to_cart), 2) AS checkout_rate,
    ROUND(100.0 * SUM(purchased) / SUM(started_checkout), 2) AS purchase_rate,
    ROUND(100.0 * SUM(purchased) / COUNT(*), 2) AS overall_conversion
FROM funnel_stages;

-- This shows the conversion funnel from product views to purchases
