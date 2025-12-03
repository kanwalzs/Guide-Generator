/*
================================================================================
              Snowflake Replication - Simple Overview & Tutorial
================================================================================

OVERVIEW:
This worksheet provides a comprehensive guide to Snowflake Database Replication,
including step-by-step tutorials, working examples, and best practices for 
disaster recovery and high availability scenarios.

WHAT IS SNOWFLAKE REPLICATION?
Snowflake Database Replication allows you to create and maintain synchronized 
copies of your databases across different regions, clouds, or accounts. It's 
your safety net for disaster recovery and high availability scenarios.

KEY CONCEPTS:
• Primary Database - Your source database with the original data
• Replica Database - A synchronized copy in another account/region
• Replication Group - Collection of databases that replicate together
• Refresh - Operation that syncs changes from primary to replica
• Failover - Switching operations from primary to replica during disasters

BUSINESS BENEFITS:
✅ Disaster Recovery - Protect against regional outages  
✅ High Availability - Near-zero downtime for critical applications  
✅ Geographic Distribution - Serve global users with lower latency  
✅ Compliance - Meet data residency requirements  
✅ Load Distribution - Offload read queries to replicas

TIME TO COMPLETE: 15-20 minutes
SKILL LEVEL: Intermediate

================================================================================
*/

/*
================================================================================
                           STEP 1: BASIC REPLICATION SETUP
================================================================================
*/

-- Step 1A: Enable replication on your primary database
-- Note: Replace 'MY_PRODUCTION_DB' with your actual database name
-- Note: Replace 'TARGET_ACCOUNT_LOCATOR' with your target account identifier

-- Enable replication on your primary database
ALTER DATABASE MY_PRODUCTION_DB 
ENABLE REPLICATION TO ACCOUNTS ('TARGET_ACCOUNT_LOCATOR');

-- Check replication status
SHOW DATABASES LIKE 'MY_PRODUCTION_DB';

-- View detailed database information including replication settings
DESC DATABASE MY_PRODUCTION_DB;

-- Step 1B: Create replica database (run this in your target account)
-- Note: Replace 'SOURCE_ACCOUNT' with your source account identifier

-- In the target account, create replica from primary
CREATE DATABASE MY_REPLICA_DB 
AS REPLICA OF SOURCE_ACCOUNT.MY_PRODUCTION_DB;

-- Verify replica creation
SHOW DATABASES LIKE 'MY_REPLICA_DB';

-- Step 1C: Monitor replication status

-- Check replication group information
SHOW REPLICATION DATABASES;
SHOW DATABASES IN REPLICATION GROUP;

-- View replication history and details
SELECT * FROM INFORMATION_SCHEMA.REPLICATION_DATABASES;

-- Step 1D: Refresh replica (sync changes)

-- Manually refresh replica to get latest changes
ALTER DATABASE MY_REPLICA_DB REFRESH;

-- Set up automatic refresh schedule (every 4 hours)
ALTER DATABASE MY_REPLICA_DB 
SET REPLICATION_SCHEDULE = 'USING CRON 0 */4 * * * UTC';

/*
================================================================================
                    COMPLETE WORKING EXAMPLE: E-COMMERCE REPLICATION
================================================================================
*/

/*
SCENARIO: E-commerce Database Replication
We'll create a complete example demonstrating the entire replication workflow
from initial setup to disaster recovery scenarios.
*/

-- =============================================================================
-- PRIMARY ACCOUNT SETUP (US-EAST)
-- =============================================================================

-- 1. Create primary database with sample e-commerce data
CREATE DATABASE ECOMMERCE_PRIMARY;
USE DATABASE ECOMMERCE_PRIMARY;
CREATE SCHEMA SALES;
USE SCHEMA SALES;

-- Create orders table with realistic business structure
CREATE TABLE ORDERS (
    ORDER_ID INT PRIMARY KEY,
    CUSTOMER_ID INT,
    ORDER_DATE DATE,
    TOTAL_AMOUNT DECIMAL(10,2),
    REGION VARCHAR(50),
    STATUS VARCHAR(20) DEFAULT 'COMPLETED'
);

-- Create customers table
CREATE TABLE CUSTOMERS (
    CUSTOMER_ID INT PRIMARY KEY,
    CUSTOMER_NAME VARCHAR(100),
    EMAIL VARCHAR(100),
    REGISTRATION_DATE DATE,
    REGION VARCHAR(50)
);

-- Create products table
CREATE TABLE PRODUCTS (
    PRODUCT_ID INT PRIMARY KEY,
    PRODUCT_NAME VARCHAR(100),
    CATEGORY VARCHAR(50),
    PRICE DECIMAL(10,2)
);

-- Insert sample customer data
INSERT INTO CUSTOMERS VALUES
(501, 'John Smith', 'john@email.com', '2023-01-15', 'North America'),
(502, 'Maria Garcia', 'maria@email.com', '2023-02-20', 'Europe'),
(503, 'Takeshi Tanaka', 'takeshi@email.com', '2023-03-10', 'Asia Pacific'),
(504, 'Carlos Rodriguez', 'carlos@email.com', '2023-04-05', 'South America'),
(505, 'Emma Wilson', 'emma@email.com', '2023-05-12', 'Australia');

-- Insert sample product data
INSERT INTO PRODUCTS VALUES
(1001, 'Wireless Headphones', 'Electronics', 299.99),
(1002, 'Running Shoes', 'Apparel', 129.99),
(1003, 'Coffee Maker', 'Home & Kitchen', 89.99),
(1004, 'Laptop Stand', 'Electronics', 49.99),
(1005, 'Water Bottle', 'Sports', 24.99);

-- Insert sample order data
INSERT INTO ORDERS VALUES
(2001, 501, '2024-01-15', 1250.00, 'North America', 'COMPLETED'),
(2002, 502, '2024-01-16', 875.50, 'Europe', 'COMPLETED'),
(2003, 503, '2024-01-17', 2100.75, 'Asia Pacific', 'COMPLETED'),
(2004, 504, '2024-01-18', 1575.25, 'South America', 'COMPLETED'),
(2005, 505, '2024-01-19', 950.00, 'Australia', 'COMPLETED');

-- Verify initial data
SELECT 'Orders' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM ORDERS
UNION ALL
SELECT 'Customers' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM CUSTOMERS
UNION ALL
SELECT 'Products' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM PRODUCTS;

-- 2. Enable replication to disaster recovery account
-- Note: Replace 'DR_ACCOUNT_LOCATOR' with your actual DR account identifier
ALTER DATABASE ECOMMERCE_PRIMARY 
ENABLE REPLICATION TO ACCOUNTS ('DR_ACCOUNT_LOCATOR');

-- 3. Verify replication is enabled
SHOW DATABASES LIKE 'ECOMMERCE_PRIMARY';

-- =============================================================================
-- REPLICA ACCOUNT SETUP (US-WEST - Disaster Recovery)
-- =============================================================================

-- Note: The following commands should be run in your replica/DR account

-- 1. Create replica database
-- Note: Replace 'PRIMARY_ACCOUNT' with your primary account identifier
CREATE DATABASE ECOMMERCE_REPLICA 
AS REPLICA OF PRIMARY_ACCOUNT.ECOMMERCE_PRIMARY;

-- 2. Verify data was replicated
USE DATABASE ECOMMERCE_REPLICA;
USE SCHEMA SALES;

-- Check that all data was replicated correctly
SELECT COUNT(*) AS ORDERS_COUNT FROM ORDERS; -- Should return 5
SELECT COUNT(*) AS CUSTOMERS_COUNT FROM CUSTOMERS; -- Should return 5
SELECT COUNT(*) AS PRODUCTS_COUNT FROM PRODUCTS; -- Should return 5

-- 3. Check replication status
SHOW REPLICATION DATABASES LIKE 'ECOMMERCE_REPLICA';

-- =============================================================================
-- SIMULATE ONGOING BUSINESS OPERATIONS (Back to Primary Account)
-- =============================================================================

-- Switch back to primary database to simulate ongoing business
USE DATABASE ECOMMERCE_PRIMARY;
USE SCHEMA SALES;

-- Add new customers (business growth)
INSERT INTO CUSTOMERS VALUES
(506, 'Ahmed Hassan', 'ahmed@email.com', '2024-01-20', 'Middle East'),
(507, 'Lisa Johnson', 'lisa@email.com', '2024-01-21', 'North America');

-- Add new orders (continued sales)
INSERT INTO ORDERS VALUES
(2006, 506, '2024-01-20', 425.50, 'Middle East', 'COMPLETED'),
(2007, 507, '2024-01-21', 1875.25, 'North America', 'COMPLETED'),
(2008, 501, '2024-01-22', 299.99, 'North America', 'PROCESSING');

-- Verify new data in primary
SELECT COUNT(*) AS TOTAL_ORDERS FROM ORDERS; -- Should return 8
SELECT COUNT(*) AS TOTAL_CUSTOMERS FROM CUSTOMERS; -- Should return 7

-- Show recent orders
SELECT * FROM ORDERS WHERE ORDER_DATE >= '2024-01-20';

-- =============================================================================
-- REFRESH REPLICA WITH NEW DATA (Replica Account)
-- =============================================================================

-- Note: Run these commands in your replica account

-- Refresh replica to sync new data from primary
ALTER DATABASE ECOMMERCE_REPLICA REFRESH;

-- Verify new data is now available in replica
USE DATABASE ECOMMERCE_REPLICA;
USE SCHEMA SALES;

SELECT COUNT(*) AS REPLICA_ORDERS FROM ORDERS; -- Should now return 8
SELECT COUNT(*) AS REPLICA_CUSTOMERS FROM CUSTOMERS; -- Should now return 7

-- Verify specific new records made it to replica
SELECT * FROM ORDERS WHERE ORDER_DATE >= '2024-01-20';

-- Check for the new customers
SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID IN (506, 507);

/*
================================================================================
                           COMMON REPLICATION PATTERNS
================================================================================
*/

-- =============================================================================
-- PATTERN 1: Cross-Region Disaster Recovery
-- =============================================================================

-- Primary in US-EAST-1, Replica in US-WEST-2
-- Automatic refresh every 4 hours for near real-time sync

ALTER DATABASE PRODUCTION_DB 
SET REPLICATION_SCHEDULE = 'USING CRON 0 */4 * * * UTC';

-- Monitor replication lag
SELECT 
    database_name,
    DATEDIFF('minute', last_refresh_time, CURRENT_TIMESTAMP()) as lag_minutes
FROM INFORMATION_SCHEMA.REPLICATION_DATABASES
WHERE database_name = 'PRODUCTION_DB';

-- =============================================================================
-- PATTERN 2: Cross-Cloud Replication
-- =============================================================================

-- Primary on AWS, Replica on Azure
-- Manual refresh for critical updates when needed

-- When critical update happens in primary:
ALTER DATABASE AZURE_REPLICA REFRESH;

-- Verify sync completed
SELECT last_refresh_time, replication_status 
FROM INFORMATION_SCHEMA.REPLICATION_DATABASES
WHERE database_name = 'AZURE_REPLICA';

-- =============================================================================
-- PATTERN 3: Multi-Region Read Replicas
-- =============================================================================

-- Primary in US, Read replicas in Europe and Asia for global users
-- More frequent refresh for near real-time data access

-- Europe replica - refresh every hour
ALTER DATABASE EU_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 * * * * UTC';

-- Asia replica - refresh every 2 hours
ALTER DATABASE ASIA_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 */2 * * * UTC';

/*
================================================================================
                              PRACTICAL USE CASES
================================================================================
*/

-- =============================================================================
-- USE CASE 1: Disaster Recovery Scenario
-- =============================================================================

-- Normal operations: Use primary database
USE DATABASE PRODUCTION_DB;
SELECT * FROM CRITICAL_ORDERS WHERE order_date = CURRENT_DATE();

-- During disaster: Switch applications to replica
-- (Applications would be reconfigured to point to replica)
USE DATABASE DR_REPLICA_DB;
SELECT * FROM CRITICAL_ORDERS WHERE order_date = CURRENT_DATE();
-- Same data, different location - business continues

-- =============================================================================
-- USE CASE 2: Regulatory Compliance (Data Residency)
-- =============================================================================

-- EU data must stay in EU region for GDPR compliance
CREATE DATABASE EU_COMPLIANCE_REPLICA 
AS REPLICA OF US_PRIMARY_DB;

-- Set up frequent refresh to keep EU replica current
ALTER DATABASE EU_COMPLIANCE_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 */2 * * * UTC';

-- EU applications can query local replica for compliance
USE DATABASE EU_COMPLIANCE_REPLICA;
SELECT * FROM CUSTOMER_DATA WHERE region = 'Europe';

-- =============================================================================
-- USE CASE 3: Development/Testing Environment
-- =============================================================================

-- Create development replica from production
CREATE DATABASE DEV_REPLICA 
AS REPLICA OF PRODUCTION_DB;

-- Developers can safely test against production-like data
USE DATABASE DEV_REPLICA;

-- Safe to run experimental queries without affecting production
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(total_amount) as lifetime_value
FROM ORDERS 
GROUP BY customer_id
HAVING lifetime_value > 5000;

-- Refresh dev environment weekly to get latest production structure
ALTER DATABASE DEV_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 2 * * 1 UTC'; -- Monday at 2 AM

/*
================================================================================
                         MONITORING & MANAGEMENT QUERIES
================================================================================
*/

-- =============================================================================
-- Replication Health Monitoring
-- =============================================================================

-- View all replication databases and their status
SHOW REPLICATION DATABASES;

-- Detailed replication status for specific database
SELECT 
    database_name,
    replication_status,
    last_refresh_time,
    next_scheduled_refresh,
    source_database_name,
    source_account_locator
FROM INFORMATION_SCHEMA.REPLICATION_DATABASES
WHERE database_name = 'MY_REPLICA';

-- View refresh history for troubleshooting
SELECT 
    database_name,
    refresh_time,
    refresh_type,
    refresh_status,
    error_message
FROM INFORMATION_SCHEMA.REPLICATION_DATABASE_REFRESH_HISTORY
WHERE database_name = 'MY_REPLICA'
ORDER BY refresh_time DESC
LIMIT 10;

-- =============================================================================
-- Replication Lag Analysis
-- =============================================================================

-- Check how current your replicas are
SELECT 
    database_name,
    last_refresh_time,
    DATEDIFF('minute', last_refresh_time, CURRENT_TIMESTAMP()) as lag_minutes,
    CASE 
        WHEN DATEDIFF('minute', last_refresh_time, CURRENT_TIMESTAMP()) < 60 THEN 'CURRENT'
        WHEN DATEDIFF('minute', last_refresh_time, CURRENT_TIMESTAMP()) < 240 THEN 'ACCEPTABLE'
        ELSE 'STALE'
    END as freshness_status
FROM INFORMATION_SCHEMA.REPLICATION_DATABASES;

-- =============================================================================
-- Replication Performance Monitoring
-- =============================================================================

-- Monitor refresh duration and success rate
SELECT 
    database_name,
    COUNT(*) as total_refreshes,
    SUM(CASE WHEN refresh_status = 'SUCCEEDED' THEN 1 ELSE 0 END) as successful_refreshes,
    ROUND(successful_refreshes / total_refreshes * 100, 2) as success_rate_pct,
    AVG(DATEDIFF('second', refresh_start_time, refresh_time)) as avg_duration_seconds
FROM INFORMATION_SCHEMA.REPLICATION_DATABASE_REFRESH_HISTORY
WHERE refresh_time >= DATEADD('day', -7, CURRENT_TIMESTAMP()) -- Last 7 days
GROUP BY database_name;

/*
================================================================================
                              BEST PRACTICES
================================================================================
*/

-- =============================================================================
-- 1. Refresh Strategy Based on Business Requirements
-- =============================================================================

-- Critical systems: Hourly refresh for near real-time sync
ALTER DATABASE CRITICAL_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 * * * * UTC';

-- Reporting systems: Daily refresh is usually sufficient
ALTER DATABASE REPORTING_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 2 * * * UTC'; -- Daily at 2 AM

-- Development/Testing: Weekly refresh to save costs
ALTER DATABASE DEV_REPLICA 
SET REPLICATION_SCHEDULE = 'USING CRON 0 2 * * 1 UTC'; -- Mondays at 2 AM

-- =============================================================================
-- 2. Cost Optimization Strategies
-- =============================================================================

-- Suspend replica when not needed (e.g., dev environments on weekends)
ALTER DATABASE DEV_REPLICA SUSPEND;

-- Resume when needed
ALTER DATABASE DEV_REPLICA RESUME;

-- Check current warehouse usage for replication
SELECT 
    warehouse_name,
    start_time,
    end_time,
    credits_used,
    query_type
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE query_type = 'REPLICATION'
AND start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP());

-- =============================================================================
-- 3. Security Best Practices
-- =============================================================================

-- Replicas inherit security policies from primary
-- But you can add additional restrictions for replica access

-- Create read-only role for replica access
CREATE ROLE REPLICA_READ_ONLY;

-- Grant minimal necessary permissions
GRANT USAGE ON DATABASE DISASTER_REPLICA TO ROLE REPLICA_READ_ONLY;
GRANT USAGE ON ALL SCHEMAS IN DATABASE DISASTER_REPLICA TO ROLE REPLICA_READ_ONLY;
GRANT SELECT ON ALL TABLES IN DATABASE DISASTER_REPLICA TO ROLE REPLICA_READ_ONLY;

-- Future tables will also be accessible
GRANT SELECT ON FUTURE TABLES IN DATABASE DISASTER_REPLICA TO ROLE REPLICA_READ_ONLY;

-- Create service account for disaster recovery applications
CREATE USER DR_SERVICE_ACCOUNT 
    PASSWORD = 'SecurePassword123!' 
    DEFAULT_ROLE = REPLICA_READ_ONLY;

GRANT ROLE REPLICA_READ_ONLY TO USER DR_SERVICE_ACCOUNT;

/*
================================================================================
                        DISASTER RECOVERY PROCEDURES
================================================================================
*/

-- =============================================================================
-- Normal Operations Monitoring
-- =============================================================================

-- Regular health check query for primary database
SELECT 
    'PRIMARY_HEALTHY' as status,
    CURRENT_TIMESTAMP() as check_time,
    COUNT(*) as active_sessions
FROM INFORMATION_SCHEMA.SESSIONS 
WHERE created_on >= DATEADD('hour', -1, CURRENT_TIMESTAMP());

-- =============================================================================
-- Disaster Detection and Response
-- =============================================================================

-- 1. Detect primary unavailability (this would typically be automated)
-- Check if primary database is accessible
-- If this query fails, primary may be unavailable

-- 2. Switch to replica for read operations
USE DATABASE DR_REPLICA_DB;

-- Critical business queries can continue on replica
SELECT 
    order_date,
    COUNT(*) as orders_today,
    SUM(total_amount) as revenue_today
FROM ORDERS 
WHERE order_date = CURRENT_DATE()
GROUP BY order_date;

-- Customer service can continue with replica data
SELECT 
    c.customer_name,
    c.email,
    o.order_id,
    o.order_date,
    o.total_amount,
    o.status
FROM CUSTOMERS c
JOIN ORDERS o ON c.customer_id = o.customer_id
WHERE c.customer_id = 501; -- Look up specific customer

-- =============================================================================
-- Recovery Procedures
-- =============================================================================

-- 1. When primary comes back online, verify data consistency
USE DATABASE PRODUCTION_DB;

-- Check if primary has any data that replica missed
SELECT MAX(order_id) as max_order_id FROM ORDERS;

-- 2. Resume normal replication once primary is stable
ALTER DATABASE PRODUCTION_DB 
ENABLE REPLICATION TO ACCOUNTS ('DR_ACCOUNT');

-- 3. Verify replication is working
SHOW DATABASES LIKE 'PRODUCTION_DB';

/*
================================================================================
                            COST ANALYSIS QUERIES
================================================================================
*/

-- =============================================================================
-- Replication Cost Analysis
-- =============================================================================

-- Storage costs for replicas
SELECT 
    database_name,
    ROUND(SUM(bytes_used) / (1024*1024*1024), 2) as size_gb,
    ROUND(SUM(bytes_used) * 0.023 / (1024*1024*1024), 2) as monthly_storage_cost_usd
FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY
WHERE database_name LIKE '%REPLICA%'
AND usage_date >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY database_name;

-- Compute costs for replication refreshes
SELECT 
    DATE_TRUNC('day', start_time) as refresh_date,
    SUM(credits_used) as daily_replication_credits,
    ROUND(SUM(credits_used) * 2.0, 2) as daily_cost_usd -- Assuming $2 per credit
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE query_type = 'REPLICATION'
AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY DATE_TRUNC('day', start_time)
ORDER BY refresh_date;

/*
================================================================================
                              QUICK START CHECKLIST
================================================================================

Step 1: ✅ Enable replication on primary database
   ALTER DATABASE MY_DB ENABLE REPLICATION TO ACCOUNTS ('TARGET_ACCOUNT');

Step 2: ✅ Create replica in target account
   CREATE DATABASE MY_REPLICA AS REPLICA OF SOURCE_ACCOUNT.MY_DB;

Step 3: ✅ Set up refresh schedule
   ALTER DATABASE MY_REPLICA SET REPLICATION_SCHEDULE = 'USING CRON 0 */4 * * * UTC';

Step 4: ✅ Test failover procedures
   USE DATABASE MY_REPLICA; SELECT COUNT(*) FROM CRITICAL_TABLE;

Step 5: ✅ Monitor replication health
   SELECT * FROM INFORMATION_SCHEMA.REPLICATION_DATABASES;

Step 6: ✅ Document disaster recovery process
   Create runbook with connection strings and procedures

================================================================================
                                   SUMMARY
================================================================================

Snowflake replication provides powerful capabilities for:

DISASTER RECOVERY: Keep your business running during outages by maintaining
synchronized copies of critical databases in different regions or clouds.

HIGH AVAILABILITY: Minimize downtime with automated refresh schedules and
monitoring to ensure replicas stay current with primary databases.

GLOBAL DISTRIBUTION: Serve users worldwide with local data copies, reducing
latency and improving user experience.

REGULATORY COMPLIANCE: Meet data residency requirements by keeping sensitive
data within specific geographic boundaries.

KEY SUCCESS FACTORS:
• Plan refresh schedules based on RPO (Recovery Point Objective)
• Monitor replication health and lag regularly  
• Test disaster recovery procedures periodically
• Optimize costs with appropriate refresh frequencies
• Document procedures for operations teams

For more information, visit:
https://docs.snowflake.com/en/user-guide/db-replication-config

================================================================================
*/
