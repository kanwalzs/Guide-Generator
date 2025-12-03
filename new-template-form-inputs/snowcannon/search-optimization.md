# High-level idea

Demonstrate using Search Optimization Service to accelerate point lookup queries and substring searches on large tables.

# Feature details & references

Show how to:
- Add search optimization to tables
- Configure optimization for specific columns
- Monitor search optimization maintenance
- Query performance improvements
- Handle different search patterns
- Manage costs and maintenance windows

Documentations:
* [Search Optimization Service Overview](https://docs.snowflake.com/en/user-guide/search-optimization-service)
* [ALTER TABLE](https://docs.snowflake.com/en/sql-reference/sql/alter-table)

# Test data setup

Use large TPC-H tables (LINEITEM, ORDERS) and demonstrate performance improvements for selective filters, substring searches, and IN predicates.

# Format

Use snowflake worksheet.

# Length

Normal.

# Additional notes

Include before/after query performance comparisons, cost analysis using SEARCH_OPTIMIZATION_HISTORY, and guidance on appropriate use cases.
