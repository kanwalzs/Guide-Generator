# High-level idea

Create and query External Tables to access data stored in cloud storage (S3, Azure Blob, GCS) without loading it into Snowflake.

# Feature details & references

Show how to:
- Configure external stages
- Create external tables with schema detection
- Partition external tables for performance
- Refresh metadata automatically
- Query semi-structured data (JSON, Parquet, ORC)
- Optimize with materialized views

Documentations:
* [External Tables Overview](https://docs.snowflake.com/en/user-guide/tables-external)
* [CREATE EXTERNAL TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-external-table)

# Test data setup

Stage TPC-H data as Parquet files in cloud storage. Create external tables with partitions based on date columns.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Compare performance with native tables, demonstrate auto-refresh with cloud events, and show cost implications of external table queries.
