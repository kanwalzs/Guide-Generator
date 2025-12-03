# High-level idea

Walk through extracting structured data from unstructured documents (PDFs, images) using Snowflake's Document AI capabilities powered by large language models.

# Feature details & references

Show how to:
- Stage documents (PDFs, images) in Snowflake
- Use BUILD_SCOPED_FILE_URL to create accessible URLs
- Extract information using SNOWFLAKE.CORTEX.PARSE_DOCUMENT
- Process extraction results and store in tables
- Handle different document types and formats
- Query and analyze extracted data

Documentations:
* [Document Intelligence Class](https://docs.snowflake.com/en/sql-reference/classes/document-intelligence)
* [BUILD_SCOPED_FILE_URL Function](https://docs.snowflake.com/en/sql-reference/functions/build_scoped_file_url)

# Test data setup

Create sample invoices, forms, or receipts as PDF/image files. Stage them in Snowflake. Optionally join extracted data with TPC-H tables for enrichment.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Emphasize practical extraction scenarios like invoice processing, form data extraction, or receipt parsing. Show error handling for unsupported formats.