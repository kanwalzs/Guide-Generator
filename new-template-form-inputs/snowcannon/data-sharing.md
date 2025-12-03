# High-level idea

Set up secure data sharing to provide live, read-only access to data across Snowflake accounts without copying or moving data.

# Feature details & references

Show how to:
- Create and configure shares
- Add database objects to shares
- Manage consumer accounts
- Implement reader accounts
- Use secure views for row-level security
- Monitor usage and costs

Documentations:
* [Secure Data Sharing Overview](https://docs.snowflake.com/en/user-guide/data-sharing-intro)
* [CREATE SHARE](https://docs.snowflake.com/en/sql-reference/sql/create-share)
* [Data Marketplace](https://docs.snowflake.com/en/user-guide/data-marketplace)

# Test data setup

Share filtered TPC-H data with simulated partner accounts, demonstrating both direct shares and marketplace listings.

# Format

Use snowflake worksheet.

# Length

Normal.

# Additional notes

Include examples of sharing across regions/clouds, managing access controls, and implementing usage-based sharing models.
