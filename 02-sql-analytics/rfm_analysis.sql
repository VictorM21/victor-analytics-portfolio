-- ======================================================
-- RFM Customer Segmentation
-- ======================================================
-- Skill: NTILE window functions, CASE statements, customer segmentation

WITH customer_metrics AS (
    SELECT 
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(order_amount) AS monetary
    FROM orders
    GROUP BY customer_id
),

rfm_scores AS (
    SELECT 
        customer_id,
        -- Recency: Lower days since last purchase = better score
        NTILE(5) OVER (ORDER BY DATE_PART('day', CURRENT_DATE - last_order_date) DESC) AS r_score,
        -- Frequency: Higher frequency = better score
        NTILE(5) OVER (ORDER BY frequency) AS f_score,
        -- Monetary: Higher spend = better score
        NTILE(5) OVER (ORDER BY monetary) AS m_score
    FROM customer_metrics
),

rfm_segments AS (
    SELECT 
        customer_id,
        r_score,
        f_score,
        m_score,
        CONCAT(r_score, f_score, m_score) AS rfm_cell,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 4 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score >= 2 AND m_score >= 2 THEN 'Potential Loyalists'
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Recent Users'
            WHEN r_score >= 3 AND f_score <= 2 AND m_score <= 2 THEN 'Promising'
            WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 4 THEN 'At Risk'
            WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'Need Attention'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 3 THEN 'Cannot Lose Them'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Hibernating'
            WHEN r_score <= 1 AND f_score <= 2 AND m_score <= 2 THEN 'Lost'
            ELSE 'Others'
        END AS customer_segment
    FROM rfm_scores
)

SELECT 
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM rfm_segments
GROUP BY customer_segment
ORDER BY customer_count DESC;

-- This segments customers based on:
-- Recency: How recently they purchased
-- Frequency: How often they purchase
-- Monetary: How much they spend
