&nbsp;KPI Framework: Financial Health Metrics



&nbsp;📊 Overview

This document defines key financial metrics for assessing business health, profitability, and efficiency.



&nbsp;🎯 KPI Categories



1\. Profitability Metrics - Bottom-line performance

2\. Liquidity Metrics - Short-term financial health

3\. Efficiency Metrics - Resource utilization

4\. Growth Metrics - Expansion indicators

5\. Valuation Metrics - Business worth



---



&nbsp;1. Profitability Metrics



&nbsp;1.1 Gross Profit Margin

Definition: Percentage of revenue retained after cost of goods sold.



Formula: Gross Margin % = (Revenue - COGS) / Revenue × 100



SQL Calculation:

```sql

SELECT 

&nbsp;   DATE\_TRUNC('month', order\_date) AS month,

&nbsp;   SUM(order\_total) AS revenue,

&nbsp;   SUM(cogs) AS cost\_of\_goods,

&nbsp;   ROUND(100.0 \* (SUM(order\_total) - SUM(cogs)) / SUM(order\_total), 2) AS gross\_margin\_pct

FROM orders

GROUP BY 1

ORDER BY 1;



Benchmark by Industry:



Industry	Gross Margin

SaaS	        70-85%

E-commerce	40-60%

Retail	        30-50%

Manufacturing	20-40%

Consulting	50-70%



1.2 Net Profit Margin

Definition: Percentage of revenue remaining after all expenses.



Formula: Net Margin % = Net Income / Revenue × 100



Components:



Revenue



COGS



Operating Expenses (Sales, Marketing, R\&D, G\&A)



Interest



Taxes



1.3 EBITDA

Definition: Earnings Before Interest, Taxes, Depreciation, and Amortization.



Formula: EBITDA = Net Income + Interest + Taxes + Depreciation + Amortization



Use Case: Measures operational profitability without financing and accounting decisions.



1.4 Operating Margin

Definition: Operating income as percentage of revenue.



Formula: Operating Margin = Operating Income / Revenue × 100



2\. Liquidity Metrics

2.1 Current Ratio

Definition: Ability to pay short-term obligations.



Formula:





Current Ratio = Current Assets / Current Liabilities



Interpretation:



2.0: Very safe



1.5 - 2.0: Healthy



1.0 - 1.5: Adequate



< 1.0: Concerning



2.2 Quick Ratio (Acid Test)

Definition: Ability to pay short-term obligations without selling inventory.



Formula:





Quick Ratio = (Cash + Marketable Securities + Accounts Receivable) / Current Liabilities



2.3 Cash Runway

Definition: Months until cash runs out at current burn rate.



Formula:





Runway (months) = Current Cash Balance / Monthly Burn Rate



3\. Efficiency Metrics

3.1 Revenue Per Employee

Definition: Efficiency of workforce in generating revenue.



Formula:





Revenue Per Employee = Annual Revenue / Number of Employees

Benchmark by Industry:



Industry	Revenue/Employee

SaaS	$200K - $400K

Consulting	$150K - $250K

E-commerce	$300K - $600K

Manufacturing	$250K - $500K

3.2 Asset Turnover

Definition: Efficiency in using assets to generate revenue.



Formula:





Asset Turnover = Revenue / Average Total Assets

3.3 Days Sales Outstanding (DSO)

Definition: Average days to collect payment.



Formula:





DSO = (Accounts Receivable / Total Credit Sales) × Number of Days

4\. Growth Metrics

4.1 Year-over-Year Growth

Definition: Revenue growth compared to same period last year.



Formula:





YoY Growth % = (Current Period Revenue - Prior Period Revenue) / Prior Period Revenue × 100

SQL Calculation:



sql

WITH monthly\_revenue AS (

&nbsp;   SELECT 

&nbsp;       DATE\_TRUNC('month', order\_date) AS month,

&nbsp;       SUM(order\_total) AS revenue

&nbsp;   FROM orders

&nbsp;   GROUP BY 1

)

SELECT 

&nbsp;   month,

&nbsp;   revenue,

&nbsp;   LAG(revenue, 12) OVER (ORDER BY month) AS revenue\_prev\_year,

&nbsp;   ROUND(100.0 \* (revenue - LAG(revenue, 12) OVER (ORDER BY month)) / 

&nbsp;         NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2) AS yoy\_growth\_pct

FROM monthly\_revenue

ORDER BY month;

4.2 Compound Annual Growth Rate (CAGR)

Definition: Smooth annual growth rate over multiple years.



Formula:





CAGR = (Ending Value / Beginning Value)^(1 / Number of Years) - 1

5\. Valuation Metrics

5.1 Price-to-Earnings (P/E) Ratio

Definition: Valuation relative to earnings.



Formula:





P/E = Stock Price / Earnings Per Share

5.2 Enterprise Value / Revenue

Definition: Common valuation metric for high-growth companies.



Formula:





EV/Revenue = Enterprise Value / Annual Revenue

Benchmark by Stage:



Stage	EV/Revenue Multiple

Early Stage	3-6x

Growth Stage	6-12x

Public Company	2-8x

5.3 Rule of 40

Definition: Growth rate + Profit margin should exceed 40%.



Formula:





Rule of 40 = Revenue Growth % + EBITDA Margin %

Interpretation:



Score	Classification

> 40	Excellent

30-40	Good

20-30	Average

< 20	Needs improvement

📊 Financial Dashboard Mockup



┌─────────────────────────────────────────────────────────────┐

│  FINANCIAL DASHBOARD                              Q1 2024  │

├───────────────┬───────────────┬───────────────┬─────────────┤

│   Revenue     │   Gross Margin│   EBITDA     │   Cash      │

│   $5.2M       │   72%         │   $1.8M      │   $8.5M     │

│   ▲ 25% YoY   │   ▲ 2pp       │   ▲ 15% YoY  │   ▼ 10% QoQ │

├───────────────┴───────────────┴───────────────┴─────────────┤

│                                                             │

│  P\&L Summary                                                │

│  ┌────────────────────────────────────────────────────┐    │

│  │                                                    │    │

│  │  Revenue     ████████████████████████  $5.2M      │    │

│  │  COGS        ████████                       $1.5M │    │

│  │  Gross Profit████████████████████        $3.7M    │    │

│  │  OpEx        ██████████                   $1.9M   │    │

│  │  EBITDA      ██████████                   $1.8M   │    │

│  └────────────────────────────────────────────────────┘    │

├───────────────┬─────────────────────────────────────────────┤

│  Ratios       │  Trends                                     │

│  ┌─────────┐  │  ┌────────────────────────────────────┐    │

│  │Current:1.8│  │  │                                    │    │

│  │Quick: 1.2│  │  │  Revenue vs. Expense Trend         │    │

│  │DSO: 45d  │  │  │                                    │    │

│  │Runway: 14mo│  │  └────────────────────────────────────┘    │

│  └─────────┘  │                                             │

│               │  ┌────────────────────────────────────┐    │

│  Rule of 40   │  │                                    │    │

│  ┌─────────┐  │  │  Monthly Burn Rate                 │    │

│  │Growth:25%│  │  │                                    │    │

│  │Margin: 35%│  │  └────────────────────────────────────┘    │

│  │Score: 60 │  │                                             │

│  └─────────┘  │                                             │

└───────────────┴─────────────────────────────────────────────┘



