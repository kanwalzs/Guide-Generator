# High-level idea

Implement Dynamic Data Masking and Row Access Policies to protect sensitive data while maintaining usability for authorized users.

# Feature details & references

Show how to:
- Create masking policies for columns
- Implement conditional masking logic
- Apply row access policies for filtering
- Manage policy assignments
- Combine multiple policies
- Audit policy usage

Documentations:
* [Dynamic Data Masking](https://docs.snowflake.com/en/user-guide/security-column-ddm)
* [Row Access Policies](https://docs.snowflake.com/en/user-guide/security-row-access-policies)
* [CREATE MASKING POLICY](https://docs.snowflake.com/en/sql-reference/sql/create-masking-policy)

# Test data setup

Create employee and customer tables with PII. Use TPC-H customer data with added sensitive fields like SSN, salary, credit cards.

# Format

Use snowflake worksheet.

# Length

Normal.

# Additional notes

Show role-based masking, partial masking patterns (e.g., XXX-XX-1234 for SSN), and performance impact analysis.
