# High-level idea

Deploy containerized applications and services using Snowpark Container Services (SPCS) to run custom workloads directly within Snowflake.

# Feature details & references

Show how to:
- Create compute pools with CPU/GPU resources
- Build and push container images
- Deploy services with specifications
- Configure networking and endpoints
- Mount volumes and stages
- Implement job services vs long-running services

Documentations:
* [Snowpark Container Services Overview](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview)
* [CREATE COMPUTE POOL](https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool)

# Test data setup

Deploy a sample ML model serving application that processes TPC-H data for predictions.

# Format

Use snowflake notebook.

# Length

Long.

# Additional notes

Include Dockerfile examples, service specifications, and monitoring patterns. Show both CPU and GPU workloads if applicable.
