/*
================================================================================
         Set up database replication for disaster recovery
================================================================================

OVERVIEW:
Learn how to configure Snowflake database replication for seamless failover 
across regions and clouds. This template demonstrates the complete workflow 
from enabling replication to performing refresh operations for disaster recovery.

BUSINESS CONTEXT:
Modern businesses require high availability and disaster recovery capabilities 
to ensure business continuity. Snowflake's database replication feature enables
organizations to maintain synchronized copies of critical data across different
regions and cloud providers, providing protection against regional outages and
ensuring rapid recovery in disaster scenarios.

TIME TO COMPLETE: 3-5 minutes
SKILL LEVEL: Intermediate
FEATURE: Database Replication

WHAT YOU'LL LEARN:
• How to enable database replication in Snowflake
• SQL commands for creating and managing replicas
• How to perform refresh operations to sync data
• Best practices for monitoring replication status
• Disaster recovery workflow using replication

================================================================================
*/

/*
STEP 1: Environment Setup and Cleanup
--------------------------------------

First, we'll set up our environment in the learning database and create a 
unique schema for this demonstration. We'll also clean up any existing 
objects from previous runs to ensure a fresh start.
*/

USE ROLE SNOWFLAKE_LEARNING_ROLE;
USE WAREHOUSE SNOWFLAKE_LEARNING_WH;  
USE DATABASE SNOWFLAKE_LEARNING_DB;

SET schema_name = CONCAT(current_user(), '_REPLICATION');
USE SCHEMA IDENTIFIER($schema_name);

-- Clean up any existing objects from previous runs
DROP SCHEMA IF EXISTS REPLICATION_PRIMARY_SCHEMA CASCADE;
DROP SCHEMA IF EXISTS REPLICATION_REPLICA_SCHEMA CASCADE;

/*
STEP 2: Create Primary Schema and Sample Data
----------------------------------------------

We'll create a primary schema that simulates a production database containing
customer, product, and sales data. In a real scenario, this would be your 
primary database located in one region or cloud provider.
*/

-- Create primary schema to simulate database replication
-- Note: In production, this would be a separate database in another region/account
CREATE SCHEMA IF NOT EXISTS REPLICATION_PRIMARY_SCHEMA;
USE SCHEMA REPLICATION_PRIMARY_SCHEMA;

-- Create sample customers table with realistic business data
CREATE OR REPLACE TABLE CUSTOMERS (
    CUSTOMER_ID INT PRIMARY KEY,
    CUSTOMER_NAME VARCHAR(100),
    EMAIL VARCHAR(100),
    REGION VARCHAR(50),
    REGISTRATION_DATE DATE,
    STATUS VARCHAR(20)
);

-- Insert sample customer data representing global customers
INSERT INTO CUSTOMERS VALUES
(1, 'Acme Corporation', 'contact@acme.com', 'North America', '2023-01-15', 'Active'),
(2, 'Global Solutions Ltd', 'info@globalsolutions.com', 'Europe', '2023-02-20', 'Active'),
(3, 'Tech Innovations Inc', 'hello@techinnovations.com', 'Asia Pacific', '2023-03-10', 'Active'),
(4, 'Digital Dynamics', 'support@digitaldynamics.com', 'North America', '2023-04-05', 'Active'),
(5, 'Future Systems', 'contact@futuresystems.com', 'Europe', '2023-05-12', 'Inactive');

-- Create products table with enterprise solutions
CREATE OR REPLACE TABLE PRODUCTS (
    PRODUCT_ID INT PRIMARY KEY,
    PRODUCT_NAME VARCHAR(100),
    CATEGORY VARCHAR(50),
    PRICE DECIMAL(10,2),
    LAUNCH_DATE DATE
);

-- Insert product data representing a software company's offerings
INSERT INTO PRODUCTS VALUES
(101, 'Enterprise Analytics Platform', 'Software', 15000.00, '2023-01-01'),
(102, 'Cloud Storage Service', 'Infrastructure', 500.00, '2023-02-01'),
(103, 'AI Development Toolkit', 'Software', 8000.00, '2023-03-01'),
(104, 'Security Monitoring Suite', 'Security', 12000.00, '2023-04-01'),
(105, 'Mobile App Framework', 'Software', 3000.00, '2023-05-01');

-- Create sales table to track customer transactions
CREATE OR REPLACE TABLE SALES (
    SALE_ID INT PRIMARY KEY,
    CUSTOMER_ID INT,
    PRODUCT_ID INT,
    SALE_DATE DATE,
    QUANTITY INT,
    TOTAL_AMOUNT DECIMAL(12,2),
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID),
    FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS(PRODUCT_ID)
);

-- Insert sales data showing business activity
INSERT INTO SALES VALUES
(1001, 1, 101, '2023-06-01', 1, 15000.00),
(1002, 2, 102, '2023-06-02', 10, 5000.00),
(1003, 3, 103, '2023-06-03', 1, 8000.00),
(1004, 1, 104, '2023-06-04', 2, 24000.00),
(1005, 4, 105, '2023-06-05', 3, 9000.00),
(1006, 2, 101, '2023-06-06', 1, 15000.00),
(1007, 5, 102, '2023-06-07', 5, 2500.00);

-- Verify initial data creation
SELECT 'Customers' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM CUSTOMERS
UNION ALL
SELECT 'Products' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM PRODUCTS  
UNION ALL
SELECT 'Sales' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM SALES;

/*
STEP 3: Enable Database Replication
------------------------------------

In production, you would enable replication on your primary database to allow
it to be replicated to other accounts. Here we show the SQL commands that would
be used in a real multi-account replication setup.
*/

-- In production: ALTER DATABASE REPLICATION_PRIMARY_DB ENABLE REPLICATION TO ACCOUNTS ('TARGET_ACCOUNT');
-- For demonstration: We'll show the commands that would be used
SELECT 'Database replication would be enabled with:' AS REPLICATION_SETUP;
SELECT 'ALTER DATABASE PRIMARY_DB ENABLE REPLICATION TO ACCOUNTS (TARGET_ACCOUNT)' AS SQL_COMMAND;

-- Check current objects that would be replicated
SHOW TABLES IN SCHEMA REPLICATION_PRIMARY_SCHEMA;

/*
STEP 4: Create Replica Database
--------------------------------

This step demonstrates creating a replica database from the primary. In 
production, this replica would typically be in a different account, region,
or cloud provider to provide true disaster recovery capabilities.
*/

-- Create replica schema to simulate database replica in another region
-- In production: CREATE DATABASE REPLICA_DB AS REPLICA OF PRIMARY_DB;
CREATE SCHEMA IF NOT EXISTS REPLICATION_REPLICA_SCHEMA;

-- Copy initial data to simulate replica creation
CREATE TABLE REPLICATION_REPLICA_SCHEMA.CUSTOMERS AS 
SELECT * FROM REPLICATION_PRIMARY_SCHEMA.CUSTOMERS;

CREATE TABLE REPLICATION_REPLICA_SCHEMA.PRODUCTS AS
SELECT * FROM REPLICATION_PRIMARY_SCHEMA.PRODUCTS;

CREATE TABLE REPLICATION_REPLICA_SCHEMA.SALES AS
SELECT * FROM REPLICATION_PRIMARY_SCHEMA.SALES;

-- Switch to replica schema to verify contents
USE SCHEMA REPLICATION_REPLICA_SCHEMA;

-- Verify replica contains same data as primary
SELECT 'Replica - Customers' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM CUSTOMERS
UNION ALL  
SELECT 'Replica - Products' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM PRODUCTS
UNION ALL
SELECT 'Replica - Sales' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM SALES;

/*
STEP 5: Simulate Data Changes and Perform Refresh
--------------------------------------------------

This step demonstrates how new data in the primary database can be synchronized
to the replica through refresh operations. This is critical for maintaining
data consistency between primary and replica databases.
*/

-- Switch back to primary schema and add more data
USE SCHEMA REPLICATION_PRIMARY_SCHEMA;

-- Add new customer to primary (simulating business growth)
INSERT INTO CUSTOMERS VALUES
(6, 'Innovative Enterprises', 'contact@innovative.com', 'Asia Pacific', '2023-07-01', 'Active');

-- Add new sales record to primary (showing continued business activity)
INSERT INTO SALES VALUES
(1008, 6, 103, '2023-07-15', 2, 16000.00);

-- Verify new data in primary
SELECT COUNT(*) AS PRIMARY_CUSTOMERS FROM CUSTOMERS;
SELECT COUNT(*) AS PRIMARY_SALES FROM SALES;

-- Refresh the replica schema to sync latest changes
-- In production: ALTER DATABASE REPLICA_DB REFRESH;
-- For demonstration: We'll manually sync the changes
INSERT INTO REPLICATION_REPLICA_SCHEMA.CUSTOMERS
SELECT * FROM REPLICATION_PRIMARY_SCHEMA.CUSTOMERS 
WHERE CUSTOMER_ID NOT IN (SELECT CUSTOMER_ID FROM REPLICATION_REPLICA_SCHEMA.CUSTOMERS);

INSERT INTO REPLICATION_REPLICA_SCHEMA.SALES
SELECT * FROM REPLICATION_PRIMARY_SCHEMA.SALES
WHERE SALE_ID NOT IN (SELECT SALE_ID FROM REPLICATION_REPLICA_SCHEMA.SALES);

-- Switch to replica schema and verify refresh worked
USE SCHEMA REPLICATION_REPLICA_SCHEMA;

-- Check if replica now has updated data
SELECT COUNT(*) AS REPLICA_CUSTOMERS FROM CUSTOMERS;
SELECT COUNT(*) AS REPLICA_SALES FROM SALES;

-- Compare primary vs replica data to ensure sync
SELECT 
    'Customer 6 in Replica' AS CHECK_TYPE,
    CASE WHEN EXISTS (SELECT 1 FROM CUSTOMERS WHERE CUSTOMER_ID = 6) 
         THEN 'FOUND' ELSE 'NOT_FOUND' END AS RESULT;

/*
STEP 6: Monitor Replication Status and History
-----------------------------------------------

Monitoring replication health and performance is crucial for maintaining a 
reliable disaster recovery system. Here we show the types of monitoring 
queries you would use in production.
*/

-- Show schemas that would be replicated
SHOW SCHEMAS LIKE 'REPLICATION_%';

-- In production, you would use these commands for monitoring:
SELECT 'Production replication monitoring commands:' AS MONITORING_INFO;
SELECT 'SHOW DATABASES IN REPLICATION GROUP' AS COMMAND_1;
SELECT 'SHOW REPLICATION DATABASES' AS COMMAND_2; 
SELECT 'SELECT * FROM INFORMATION_SCHEMA.REPLICATION_DATABASES' AS COMMAND_3;

-- Simulate replication metadata monitoring
SELECT 
    'REPLICATION_REPLICA_SCHEMA' AS REPLICA_SCHEMA,
    CURRENT_TIMESTAMP() AS LAST_CHECK_TIME,
    'ACTIVE' AS REPLICATION_STATUS,
    '< 1 minute' AS REPLICATION_LAG,
    'PRIMARY_HEALTHY' AS PRIMARY_STATUS;

/*
STEP 7: Demonstrate Disaster Recovery Scenario
-----------------------------------------------

This step shows how you would use the replica database for business-critical 
queries during a disaster scenario when the primary database is unavailable.
*/

-- Simulate using replica for read operations during primary unavailability
USE SCHEMA REPLICATION_REPLICA_SCHEMA;

-- Business-critical query that could run on replica during disaster
SELECT 
    c.REGION,
    COUNT(s.SALE_ID) AS TOTAL_SALES,
    SUM(s.TOTAL_AMOUNT) AS TOTAL_REVENUE,
    AVG(s.TOTAL_AMOUNT) AS AVG_SALE_VALUE
FROM CUSTOMERS c
JOIN SALES s ON c.CUSTOMER_ID = s.CUSTOMER_ID  
WHERE s.SALE_DATE >= '2023-06-01'
GROUP BY c.REGION
ORDER BY TOTAL_REVENUE DESC;

-- Show customer activity summary from replica
SELECT 
    c.CUSTOMER_NAME,
    c.STATUS,
    COUNT(s.SALE_ID) AS PURCHASE_COUNT,
    SUM(s.TOTAL_AMOUNT) AS TOTAL_SPENT
FROM CUSTOMERS c
LEFT JOIN SALES s ON c.CUSTOMER_ID = s.CUSTOMER_ID
GROUP BY c.CUSTOMER_ID, c.CUSTOMER_NAME, c.STATUS
ORDER BY TOTAL_SPENT DESC;

/*
STEP 8: Cleanup
----------------

Finally, we'll clean up all the objects we created during this demonstration
to leave the environment clean for future runs.
*/

-- Switch back to learning schema
SET schema_name = CONCAT(current_user(), '_REPLICATION');
USE SCHEMA IDENTIFIER($schema_name);

-- Drop replica schema first (dependencies)
DROP SCHEMA IF EXISTS REPLICATION_REPLICA_SCHEMA CASCADE;

-- Drop primary schema
DROP SCHEMA IF EXISTS REPLICATION_PRIMARY_SCHEMA CASCADE;

-- Verify cleanup completed
SHOW SCHEMAS LIKE 'REPLICATION_%';

-- Final confirmation message
SELECT 'Database replication demonstration completed successfully!' AS STATUS;

/*
================================================================================
KEY TAKEAWAYS:
================================================================================

1. DATABASE REPLICATION provides seamless failover capabilities across regions
   and cloud providers for disaster recovery scenarios.

2. REPLICATION SETUP involves enabling replication on primary databases and 
   creating replica databases in target accounts/regions.

3. REFRESH OPERATIONS keep replica databases synchronized with primary databases,
   ensuring data consistency for disaster recovery.

4. MONITORING REPLICATION status and performance is essential for maintaining
   reliable disaster recovery capabilities.

5. DISASTER RECOVERY scenarios can be handled by switching read operations to
   replica databases when primary systems are unavailable.

================================================================================
ADDITIONAL RESOURCES:
================================================================================

📖 Database Replication Configuration:
   https://docs.snowflake.com/en/user-guide/db-replication-config

📖 Account Replication Configuration:
   https://docs.snowflake.com/en/user-guide/account-replication-config

🎯 More Templates:
   Visit app.snowflake.com/templates to explore additional templates

================================================================================
*/
