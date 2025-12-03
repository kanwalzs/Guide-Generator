# High-level idea

Demonstrate creating and managing Materialized Views to pre-compute and store query results for improved performance.

# Feature details & references

Show how to:
- Create materialized views on complex queries
- Configure automatic background maintenance
- Monitor refresh history and costs
- Query rewrite optimization
- Handle base table changes
- Compare with dynamic tables and regular views

Documentations:
* [Materialized Views Overview](https://docs.snowflake.com/en/user-guide/views-materialized)
* [CREATE MATERIALIZED VIEW](https://docs.snowflake.com/en/sql-reference/sql/create-materialized-view)

# Test data setup

Use TPC-H tables to create materialized views for common aggregate queries (revenue by customer, product sales summaries) showing query acceleration.

# Format

Use snowflake worksheet.

# Length

Normal.

# Additional notes

Include performance comparisons, cost analysis using MATERIALIZED_VIEW_REFRESH_HISTORY, and guidance on when to use MVs vs Dynamic Tables.