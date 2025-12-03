# High-level idea

Create User-Defined Functions (UDFs) and User-Defined Table Functions (UDTFs) in multiple languages (SQL, JavaScript, Python, Java) to extend Snowflake's capabilities.

# Feature details & references

Show how to:
- Create scalar UDFs for custom calculations
- Build UDTFs for generating table results
- Use Python UDFs with external packages
- Implement JavaScript UDFs for complex logic
- Handle secure UDFs with data access
- Optimize performance and manage dependencies

Documentations:
* [User-Defined Functions Overview](https://docs.snowflake.com/en/developer-guide/udf/udf-overview)
* [CREATE FUNCTION](https://docs.snowflake.com/en/sql-reference/sql/create-function)

# Test data setup

Use TPC-H data to create custom business logic functions: pricing calculations, text processing, and data validation rules.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Compare performance across languages, show vectorized Python UDFs, and demonstrate package management with Anaconda integration.
