# High-level idea

Implement change data capture (CDC) and automated data pipelines using Streams for tracking changes and Tasks for orchestration.

# Feature details & references

Show how to:
- Create streams on tables, views, and external tables
- Track INSERT, UPDATE, DELETE operations
- Build tasks with schedules and dependencies
- Create task trees and DAGs
- Handle error recovery and monitoring
- Implement incremental processing patterns

Documentations:
* [Streams Overview](https://docs.snowflake.com/en/user-guide/streams)
* [Tasks Overview](https://docs.snowflake.com/en/user-guide/tasks-intro)
* [CREATE STREAM](https://docs.snowflake.com/en/sql-reference/sql/create-stream)

# Test data setup

Use TPC-H tables to demonstrate CDC patterns, building aggregate tables that update incrementally based on order changes.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Show both append-only and standard streams. Demonstrate task suspension/resumption and monitoring with TASK_HISTORY.
