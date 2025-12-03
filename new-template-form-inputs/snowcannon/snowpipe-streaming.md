# High-level idea

Demonstrate real-time data ingestion using Snowpipe Streaming for low-latency, high-throughput streaming data loads.

# Feature details & references

Show how to:
- Set up Snowpipe Streaming channels
- Configure streaming ingestion from Kafka/Kinesis
- Monitor ingestion metrics and latency
- Handle schema detection and evolution
- Implement exactly-once semantics
- Optimize for cost and performance

Documentations:
* [Snowpipe Streaming Overview](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview)
* [Kafka Connector for Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-kafka)

# Test data setup

Simulate streaming events (orders, clickstream, IoT sensors) and demonstrate near real-time ingestion. Can enrich with TPC-H dimension tables.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Compare with batch Snowpipe, show monitoring using SNOWPIPE_STREAMING_FILE_MIGRATION_HISTORY, and demonstrate offset management for exactly-once delivery.