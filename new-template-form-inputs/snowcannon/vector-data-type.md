# High-level idea

Introduce vector embeddings storage and similarity search using Snowflake's VECTOR data type and related functions for semantic search applications.

# Feature details & references

Show how to:
- Create tables with VECTOR columns
- Generate embeddings using EMBED_TEXT functions
- Store and index vector data efficiently
- Perform similarity searches (cosine, L2 distance)
- Combine vector search with filters
- Optimize vector operations for performance

Documentations:
* [VECTOR Data Type](https://docs.snowflake.com/en/sql-reference/data-types-vector)
* [Vector Embeddings](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings)
* [VECTOR_COSINE_SIMILARITY Function](https://docs.snowflake.com/en/sql-reference/functions/vector_cosine_similarity)

# Test data setup

Create product descriptions or document corpus with pre-computed or Cortex-generated embeddings. Use a subset of TPC-H product data enhanced with text descriptions.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Compare different embedding models, demonstrate hybrid search combining vector similarity with SQL filters, and show performance considerations for large-scale vector operations.