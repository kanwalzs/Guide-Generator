# High-level idea

Demonstrate using Cortex LLM functions for text generation, summarization, translation, and sentiment analysis directly within SQL queries.

# Feature details & references

Show how to:
- Use COMPLETE function for text generation
- Apply SUMMARIZE for document summarization
- Perform TRANSLATE for multi-language support
- Analyze SENTIMENT of text data
- Choose appropriate models for different tasks
- Handle token limits and costs

Documentations:
* [Cortex LLM Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
* [COMPLETE Function](https://docs.snowflake.com/en/sql-reference/functions/complete)

# Test data setup

Create sample customer reviews, support tickets, and product descriptions. Use TPC-H comments fields for additional text data.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Compare different models (Mistral, Llama, etc.) for various tasks. Show batch processing patterns and cost optimization strategies.
