# High-level idea

Leverage Snowflake's Time Travel feature to query historical data, recover from mistakes, and analyze data changes over time.

# Feature details & references

Show how to:
- Query data at specific timestamps
- Use AT and BEFORE clauses
- Clone tables from historical points
- Undrop tables and schemas
- Configure retention periods
- Analyze data changes over time

Documentations:
* [Time Travel Overview](https://docs.snowflake.com/en/user-guide/data-time-travel)
* [AT | BEFORE Clause](https://docs.snowflake.com/en/sql-reference/constructs/at-before)

# Test data setup

Use TPC-H tables with simulated updates over time to demonstrate historical querying and recovery scenarios.

# Format

Use snowflake worksheet.

# Length

Normal.

# Additional notes

Include cost considerations, retention period management, and integration with Fail-safe. Show practical recovery scenarios.
