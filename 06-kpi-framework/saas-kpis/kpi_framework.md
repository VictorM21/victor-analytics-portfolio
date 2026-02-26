&nbsp;KPI Framework: SaaS Business Model



&nbsp;📊 Overview

This document defines a comprehensive KPI framework for a Subscription-as-a-Service (SaaS) business, including definitions, calculation methodologies, benchmarks, and visualization recommendations.



&nbsp;🎯 KPI Categories



1\. Acquisition Metrics - How customers find and join

2\. Activation Metrics - First value experience

3\. Revenue Metrics - Monetary performance

4\. Retention Metrics - Customer loyalty

5\. Referral Metrics - Viral growth

6\. Financial Metrics - Business health



---



&nbsp;1. Acquisition Metrics



&nbsp;1.1 Customer Acquisition Cost (CAC)

Definition: The total cost of acquiring a new customer, including marketing and sales expenses.



Formula: CAC = Total Sales \& Marketing Expenses / Number of New Customers Acquired





Components:

\- Marketing spend (ads, content, events)

\- Sales team salaries and commissions

\- Software tools (CRM, marketing automation)

\- Agency fees



Benchmark:

\- Good: < $500

\- Average: $500 - $1,000

\- Concerning: > $1,500



SQL Calculation:

```sql

WITH monthly\_costs AS (

&nbsp;   SELECT 

&nbsp;       DATE\_TRUNC('month', expense\_date) AS month,

&nbsp;       SUM(marketing\_spend + sales\_salaries + software\_costs) AS total\_cost

&nbsp;   FROM marketing\_expenses

&nbsp;   GROUP BY 1

),

new\_customers AS (

&nbsp;   SELECT 

&nbsp;       DATE\_TRUNC('month', first\_payment\_date) AS month,

&nbsp;       COUNT(DISTINCT customer\_id) AS new\_customers

&nbsp;   FROM subscriptions

&nbsp;   GROUP BY 1

)

SELECT 

&nbsp;   c.month,

&nbsp;   c.total\_cost,

&nbsp;   nc.new\_customers,

&nbsp;   ROUND(c.total\_cost / nc.new\_customers, 2) AS cac

FROM monthly\_costs c

JOIN new\_customers nc ON c.month = nc.month

ORDER BY c.month DESC;



Dashboard Visualization:



Line chart showing CAC trend over time



Bar chart comparing CAC by channel



Gauge showing CAC vs. target



1.2 Marketing Qualified Leads (MQL)

Definition: Leads that have engaged with marketing and meet qualification criteria.



Formula: Count of leads meeting MQL criteria



Typical Criteria:



Downloaded premium content



Attended webinar



Visited pricing page multiple times



Engaged with email campaign



Benchmark:



Growth rate: 10-20% month-over-month



MQL to SQL conversion: 20-30%



1.3 Cost Per Lead (CPL)

Definition: Average cost to generate a qualified lead.



Formula: CPL = Total Marketing Spend / Total MQLs



Benchmark by Channel:



Channel	Average CPL

Google Ads	$50-100

LinkedIn	$75-150

Content Marketing	$20-50

Email Marketing	$10-30

Events	$100-300

2\. Activation Metrics

2.1 Time to First Value (TTFV)

Definition: The average time it takes for a new customer to experience their first "aha moment" or key value milestone.



Formula: TTFV = Average(First Value Date - Sign-up Date)



SaaS Examples:



Project management tool: First project created



Analytics tool: First dashboard viewed



CRM: First contact added



SQL Calculation:

SELECT 

&nbsp;   AVG(DATEDIFF('day', signup\_date, first\_value\_date)) AS avg\_ttfv\_days,

&nbsp;   PERCENTILE\_CONT(0.5) WITHIN GROUP (ORDER BY DATEDIFF('day', signup\_date, first\_value\_date)) AS median\_ttfv\_days

FROM user\_journey

WHERE first\_value\_date IS NOT NULL;



Benchmark: < 3 days is excellent, < 7 days is good



2.2 Activation Rate

Definition: Percentage of sign-ups that complete key activation steps.



Formula:



text

Activation Rate = (Users Completing Activation / Total Sign-ups) \* 100



Activation Steps Example:



Complete profile setup



Connect data source



Create first report



Invite team member



Benchmark: 70-80% is excellent



2.3 Onboarding Completion Rate

Definition: Percentage of users who complete the entire onboarding flow.



SQL Calculation:



WITH funnel AS (

&nbsp;   SELECT 

&nbsp;       user\_id,

&nbsp;       MAX(CASE WHEN event = 'signup' THEN 1 ELSE 0 END) AS step1,

&nbsp;       MAX(CASE WHEN event = 'profile\_complete' THEN 1 ELSE 0 END) AS step2,

&nbsp;       MAX(CASE WHEN event = 'data\_connected' THEN 1 ELSE 0 END) AS step3,

&nbsp;       MAX(CASE WHEN event = 'first\_report' THEN 1 ELSE 0 END) AS step4

&nbsp;   FROM user\_events

&nbsp;   GROUP BY user\_id

)

SELECT 

&nbsp;   COUNT(\*) AS total\_users,

&nbsp;   SUM(step1) AS signups,

&nbsp;   SUM(step2) AS profile\_complete,

&nbsp;   SUM(step3) AS data\_connected,

&nbsp;   SUM(step4) AS first\_report,

&nbsp;   ROUND(100.0 \* SUM(step4) / COUNT(\*), 2) AS overall\_completion\_rate

FROM funnel;



3\. Revenue Metrics

3.1 Monthly Recurring Revenue (MRR)

Definition: The predictable monthly revenue generated from subscriptions.



Formula: MRR = SUM(Monthly Subscription Amount for Active Customers)

MRR Components:



New MRR: From new customers



Expansion MRR: From upgrades/add-ons



Contraction MRR: From downgrades



Churn MRR: From cancellations



SQL Calculation: 

WITH daily\_mrr AS (

&nbsp;   SELECT 

&nbsp;       DATE\_TRUNC('month', date) AS month,

&nbsp;       SUM(CASE WHEN event\_type = 'new' THEN mrr\_amount ELSE 0 END) AS new\_mrr,

&nbsp;       SUM(CASE WHEN event\_type = 'upgrade' THEN mrr\_amount ELSE 0 END) AS expansion\_mrr,

&nbsp;       SUM(CASE WHEN event\_type = 'downgrade' THEN -mrr\_amount ELSE 0 END) AS contraction\_mrr,

&nbsp;       SUM(CASE WHEN event\_type = 'churn' THEN -mrr\_amount ELSE 0 END) AS churn\_mrr

&nbsp;   FROM mrr\_events

&nbsp;   GROUP BY 1

)

SELECT 

&nbsp;   month,

&nbsp;   new\_mrr,

&nbsp;   expansion\_mrr,

&nbsp;   contraction\_mrr,

&nbsp;   churn\_mrr,

&nbsp;   new\_mrr + expansion\_mrr - contraction\_mrr - churn\_mrr AS net\_new\_mrr

FROM daily\_mrr

ORDER BY month;



Benchmark: 10-20% month-over-month growth is healthy



3.2 Average Revenue Per User (ARPU)

Definition: Average revenue generated per active customer.



Formula:



ARPU = MRR / Total Active Customers



Benchmark by Segment:



Segment	ARPU Range

Small Business	$50-200

Mid-Market	$200-1,000

Enterprise	$1,000-10,000+

3.3 Customer Lifetime Value (LTV)

Definition: Total revenue expected from a customer over their entire relationship.



Formula: LTV = ARPU × Gross Margin × Average Customer Lifetime (months)

Simplified: LTV = ARPU / Monthly Churn Rate



Calculations SQL



WITH customer\_ltv AS (

&nbsp;   SELECT 

&nbsp;       customer\_id,

&nbsp;       SUM(revenue) AS total\_revenue,

&nbsp;       DATEDIFF('month', MIN(subscription\_date), MAX(subscription\_date)) + 1 AS lifetime\_months

&nbsp;   FROM subscriptions

&nbsp;   GROUP BY customer\_id

)

SELECT 

&nbsp;   AVG(total\_revenue) AS avg\_ltv,

&nbsp;   AVG(lifetime\_months) AS avg\_lifetime\_months,

&nbsp;   PERCENTILE\_CONT(0.5) WITHIN GROUP (ORDER BY total\_revenue) AS median\_ltv

FROM customer\_ltv;



LTV:CAC Ratio: Should be > 3:1 for healthy business



4\. Retention Metrics

4.1 Customer Churn Rate

Definition: Percentage of customers who cancel their subscriptions.



Formula: Customer Churn Rate = (Customers Lost in Period / Customers at Start of Period) × 100



WITH customers\_at\_start AS (

&nbsp;   SELECT COUNT(DISTINCT customer\_id) AS start\_count

&nbsp;   FROM subscriptions

&nbsp;   WHERE status = 'active'

&nbsp;   AND subscription\_date <= '2024-01-01'

),

customers\_lost AS (

&nbsp;   SELECT COUNT(DISTINCT customer\_id) AS lost\_count

&nbsp;   FROM subscriptions

&nbsp;   WHERE cancellation\_date BETWEEN '2024-01-01' AND '2024-01-31'

)

SELECT 

&nbsp;   start\_count,

&nbsp;   lost\_count,

&nbsp;   ROUND(100.0 \* lost\_count / start\_count, 2) AS churn\_rate

FROM customers\_at\_start, customers\_lost;



Benchmark:



B2B SaaS: < 5% monthly, < 15% annually



B2C SaaS: < 8% monthly, < 30% annually



4.2 Revenue Churn Rate

Definition: Percentage of recurring revenue lost from cancellations and downgrades.



Formula: Revenue Churn Rate = (Churned MRR + Contraction MRR) / Starting MRR × 100



4.3 Net Revenue Retention (NRR)

Definition: Revenue retained from existing customers including expansion, contraction, and churn.



Formula: NRR = (Starting MRR + Expansion MRR - Contraction MRR - Churn MRR) / Starting MRR × 100



Benchmark:



Good: > 100%



Excellent: > 120%



World-class: > 150%



4.4 Cohort Retention Table

Visualization: Heat map showing retention by cohort month



WITH cohorts AS (

&nbsp;   SELECT 

&nbsp;       customer\_id,

&nbsp;       DATE\_TRUNC('month', MIN(subscription\_date)) AS cohort\_month

&nbsp;   FROM subscriptions

&nbsp;   GROUP BY 1

),

cohort\_retention AS (

&nbsp;   SELECT 

&nbsp;       c.cohort\_month,

&nbsp;       DATE\_TRUNC('month', s.subscription\_date) AS activity\_month,

&nbsp;       COUNT(DISTINCT s.customer\_id) AS active\_customers

&nbsp;   FROM subscriptions s

&nbsp;   JOIN cohorts c ON s.customer\_id = c.customer\_id

&nbsp;   GROUP BY 1, 2

),

cohort\_size AS (

&nbsp;   SELECT 

&nbsp;       cohort\_month,

&nbsp;       active\_customers AS size

&nbsp;   FROM cohort\_retention

&nbsp;   WHERE cohort\_month = activity\_month

)

SELECT 

&nbsp;   cr.cohort\_month,

&nbsp;   cr.activity\_month,

&nbsp;   DATEDIFF('month', cr.cohort\_month, cr.activity\_month) AS months\_since,

&nbsp;   cr.active\_customers,

&nbsp;   cs.size,

&nbsp;   ROUND(100.0 \* cr.active\_customers / cs.size, 2) AS retention\_pct

FROM cohort\_retention cr

JOIN cohort\_size cs ON cr.cohort\_month = cs.cohort\_month

WHERE cr.activity\_month >= cr.cohort\_month

ORDER BY cr.cohort\_month, months\_since;



5\. Referral Metrics

5.1 Viral Coefficient (K-Factor)

Definition: Number of new users generated by each existing user.



Formula: K-Factor = Invites Sent × Conversion Rate



Interpretation:



K < 1: Viral growth not sustainable



K = 1: Stable viral growth



K > 1: Exponential viral growth



5.2 Net Promoter Score (NPS)

Definition: Customer loyalty and satisfaction metric.



Formula: NPS = % Promoters (9-10) - % Detractors (0-6)



Categories:



Promoters: 9-10 (loyal enthusiasts)



Passives: 7-8 (satisfied but unenthusiastic)



Detractors: 0-6 (unhappy customers)



Benchmark:



Excellent: > 50



Good: 30-50



Average: 10-30



Poor: < 10



6\. Financial Metrics

6.1 Gross Margin

Definition: Revenue minus cost of goods sold (COGS).



Formula: Gross Margin % = (Revenue - COGS) / Revenue × 100



SaaS Gross Margin: Typically 70-85%



6.2 Burn Multiple

Definition: How efficiently a company is spending to grow.



Formula: Burn Multiple = Net Burn / Net New ARR



Interpretation:



< 1.0: Very efficient



1.0 - 1.5: Efficient



1.5 - 2.0: Moderately efficient



2.0: Inefficient



6.3 Rule of 40

Definition: Growth rate + Profit margin should exceed 40%.



Formula: Rule of 40 = Revenue Growth % + Profit Margin % 



Interpretation:



40: Healthy business



20-40: Acceptable



< 20: Needs improvement



📊 KPI Dashboard Mockup

Executive Dashboard Layout



┌─────────────────────────────────────────────────────────────┐

│  KPI DASHBOARD - SAAS METRICS                    Q1 2024   │

├───────────────┬───────────────┬───────────────┬─────────────┤

│   MRR         │   NRR         │   CAC         │   LTV/CAC   │

│   $125K       │   115%        │   $450        │   3.2x      │

│   ▲ 12% MoM   │   ▲ 5% QoQ    │   ▼ 8% QoQ    │   ▲ 0.3x    │

├───────────────┴───────────────┴───────────────┴─────────────┤

│                                                             │

│  MRR Growth Trend                                           │

│  ┌────────────────────────────────────────────────────┐    │

│  │                                                    │    │

│  │                 Chart: Monthly MRR with           │    │

│  │                 New/Expansion/Churn breakdown     │    │

│  │                                                    │    │

│  └────────────────────────────────────────────────────┘    │

├───────────────┬─────────────────────────────────────────────┤

│  Cohort       │  Channel Performance                        │

│  Retention    │  ┌────────────────────────────────────┐    │

│  Heatmap      │  │                                    │    │

│  ┌─────────┐  │  │  Bar chart: CAC by channel        │    │

│  │         │  │  │                                    │    │

│  │ Month 1 │  │  └────────────────────────────────────┘    │

│  │ Month 2 │  │                                             │

│  │ Month 3 │  │  ┌────────────────────────────────────┐    │

│  └─────────┘  │  │                                    │    │

│               │  │  Pie chart: Revenue by segment     │    │

│               │  │                                    │    │

│               │  └────────────────────────────────────┘    │

└───────────────┴─────────────────────────────────────────────┘



📋 Data Dictionary Template

Table: subscriptions

Column	Data Type	Description	Example

subscription\_id	VARCHAR	Unique identifier	sub\_12345

customer\_id	VARCHAR	Foreign key to customers	cust\_67890

plan\_type	VARCHAR	Subscription tier	pro, enterprise

monthly\_amount	DECIMAL	Monthly recurring charge	99.00

start\_date	DATE	Subscription start	2024-01-15

end\_date	DATE	Subscription end (null if active)	null

status	VARCHAR	active, cancelled, paused	active

Table: mrr\_events

Column	Data Type	Description	Example

event\_id	VARCHAR	Unique identifier	evt\_12345

customer\_id	VARCHAR	Foreign key to customers	cust\_67890

event\_date	DATE	Date of event	2024-02-01

event\_type	VARCHAR	new, upgrade, downgrade, churn	upgrade

amount\_change	DECIMAL	Change in MRR amount	50.00

new\_mrr	DECIMAL	New total MRR for customer	149.00

✅ KPI Framework Checklist

KPI	Defined	Formula	SQL	Benchmark	Dashboard

CAC	✅	✅	✅	✅	✅

MQL	✅	✅	✅	✅	⬜

CPL	✅	✅	✅	✅	⬜

MRR	✅	✅	✅	✅	✅

ARPU	✅	✅	✅	✅	⬜

LTV	✅	✅	✅	✅	✅

Churn	✅	✅	✅	✅	✅

NRR	✅	✅	✅	✅	✅

NPS	✅	✅	⬜	✅	⬜

🔄 Next Steps

Create data dictionaries for all source tables



Build SQL queries for each KPI



Design dashboard mockups in Figma or similar



Implement in BI tool (Tableau/Power BI)



Set up automated reporting



👨‍💻 Author

Victor Makanju

