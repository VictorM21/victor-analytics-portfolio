\# BigQuery vs Snowflake: Platform Comparison



\## 📊 Overview

This document compares Google BigQuery and Snowflake based on hands-on experience with the same dataset.



\## 🏗️ Architecture Comparison



| Feature | BigQuery | Snowflake |

|---------|----------|-----------|

| \*\*Architecture\*\* | Serverless, columnar storage | Multi-cluster, shared data |

| \*\*Storage\*\* | Columnar (Capacitor) | Columnar (Micro-partitions) |

| \*\*Compute\*\* | Slot-based (on-demand or flat-rate) | Virtual warehouses (XS to 6XL) |

| \*\*Pricing Model\*\* | $5 per TB scanned + storage | Compute credits + storage |

| \*\*Separation\*\* | Compute and storage separated | Complete separation |

| \*\*Clustering\*\* | Automatic with options | Manual with clustering keys |

| \*\*Caching\*\* | Query results cached for 24h | Result caching for 24h |



\## 🔧 Setup Experience



\### BigQuery

\- Google Cloud Console access required

\- Dataset and table creation via UI or SQL

\- Automatic partitioning and clustering options

\- Free tier: 10GB storage, 1TB query per month

\- No server setup required



\### Snowflake

\- Web UI or SnowSQL client

\- Need to create warehouse, database, schema

\- Manual configuration of clustering

\- Free trial: $400 credits

\- Warehouse must be running to query



\## 📝 SQL Syntax Differences



| Operation | BigQuery | Snowflake |

|-----------|----------|-----------|

| Date Difference | `DATE\_DIFF(date1, date2, DAY)` | `DATEDIFF('day', date1, date2)` |

| Date Truncation | `DATE\_TRUNC(date, MONTH)` | `DATE\_TRUNC('month', date)` |

| NULL Handling | `IFNULL(expr, 0)` | `COALESCE(expr, 0)` |

| Safe Division | `SAFE\_DIVIDE(numerator, denominator)` | `DIV0(numerator, denominator)` |

| String Concatenation | `CONCAT(str1, str2)` or `str1 || str2` | `str1 || str2` |

| Current Date | `CURRENT\_DATE()` | `CURRENT\_DATE()` |

| Extract Year | `EXTRACT(YEAR FROM date)` | `EXTRACT(YEAR FROM date)` |



\## ⚡ Performance Comparison



\### BigQuery Strengths

\- Faster for full-table scans

\- Better for ad-hoc queries on large datasets

\- Automatic optimization

\- Integration with Google ecosystem

\- No index management needed



\### Snowflake Strengths

\- Better for mixed workloads

\- Caching for repeated queries

\- More control over compute resources

\- Better for complex joins

\- Time travel feature (up to 90 days)



\## 💰 Cost Optimization Tips



\### BigQuery

\- Use clustered tables for common filters

\- Avoid SELECT \* (scan all columns)

\- Use partitioned tables for date-filtered queries

\- Set query quotas and cost controls

\- Use `LIMIT` to reduce query costs



\### Snowflake

\- Use auto-suspend for warehouses (5-10 minutes)

\- Choose right warehouse size (start small)

\- Use clustering keys wisely

\- Leverage result caching

\- Scale down warehouses when not in use



\## 🚀 Getting Started Guides



\### BigQuery Setup

```sql

-- Create dataset

CREATE SCHEMA IF NOT EXISTS `your-project.analytics\_dataset`;



-- Create table

CREATE TABLE `your-project.analytics\_dataset.orders` (

&nbsp;   order\_id INT64,

&nbsp;   customer\_id INT64,

&nbsp;   order\_date DATE,

&nbsp;   order\_total FLOAT64,

&nbsp;   payment\_method STRING

);



-- Load data (using CLI)

-- bq load --source\_format=CSV analytics\_dataset.orders gs://bucket/orders.csv

