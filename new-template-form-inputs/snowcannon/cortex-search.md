# High-level idea

Demonstrate how to build a RAG (Retrieval Augmented Generation) application using Cortex Search for semantic and hybrid search over your Snowflake data, powering AI chat and search experiences.

# Feature details & references

Show how to:
- Create a Cortex Search Service on text columns
- Configure embedding models and search parameters
- Query using both semantic and keyword search
- Integrate with Cortex LLM functions for RAG applications
- Monitor service performance and costs
- Handle index refreshes and updates

Documentations:
* [Cortex Search Overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)

# Test data setup

Create sample knowledge base documents (FAQs, product descriptions, support tickets) as text data. Can also use TPC-H `PART.P_COMMENT` and `LINEITEM.L_COMMENT` for additional text corpus.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Focus on RAG use case - show how retrieved context enhances LLM responses. Include examples of both REST API and SQL function usage.