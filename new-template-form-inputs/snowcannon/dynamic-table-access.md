# High-level idea

Demonstrate creating and managing Dynamic Tables for automated, incremental data transformations with declarative SQL.

# Feature details & references

Show how to:
- Create dynamic tables with target lag specifications
- Monitor refresh status and data freshness
- Query dynamic tables like regular tables
- Manage dependencies between dynamic tables
- Control costs with warehouse and lag settings
- Handle schema evolution

Documentations:
* [Dynamic Tables Overview](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
* [Creating Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-create)
* [Managing Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-manage)

# Test data setup

Use TPC-H tables to create a pipeline of dynamic tables for order analytics, aggregating at different levels (daily, weekly, monthly) with automatic refresh.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Demonstrate the advantage over traditional views and tasks. Show monitoring queries using DYNAMIC_TABLE_REFRESH_HISTORY. Include cost optimization strategies.