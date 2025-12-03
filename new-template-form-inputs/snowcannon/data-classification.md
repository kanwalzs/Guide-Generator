# High-level idea

Implement automated sensitive data discovery and classification to identify and tag PII, financial, and other sensitive data across your Snowflake environment.

# Feature details & references

Show how to:
- Run automatic classification on databases
- Define custom classification rules
- Apply system and custom tags
- Query classification results
- Implement data masking policies
- Generate compliance reports

Documentations:
* [Data Classification Overview](https://docs.snowflake.com/en/user-guide/governance-classify)
* [EXTRACT_SEMANTIC_CATEGORIES](https://docs.snowflake.com/en/sql-reference/functions/extract_semantic_categories)

# Test data setup

Create tables with mixed data including fake PII (SSN, email, phone), financial data, and general business data from TPC-H.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Show integration with masking policies and row access policies. Demonstrate compliance reporting for GDPR/CCPA requirements.
