# High-level idea

Demonstrate working with Apache Iceberg tables in Snowflake for open table format interoperability and multi-engine access.

# Feature details & references

Show how to:
- Create Snowflake-managed Iceberg tables
- Configure external Iceberg tables on cloud storage
- Query Iceberg metadata and snapshots
- Handle schema evolution and partitioning
- Perform time travel queries
- Convert between native and Iceberg formats

Documentations:
* [Iceberg Tables Overview](https://docs.snowflake.com/en/user-guide/tables-iceberg)
* [CREATE ICEBERG TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table)

# Test data setup

Create Iceberg tables from TPC-H data, demonstrating both managed and external table scenarios. Show Parquet file generation and catalog integration.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Highlight interoperability benefits, compare performance with native tables, and demonstrate metadata operations. Include external catalog integration examples.