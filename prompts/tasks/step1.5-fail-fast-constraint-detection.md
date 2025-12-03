# Step 1.5: Fail-Fast Constraint Detection

## 🚨 **CRITICAL: Fail-Fast Constraint Detection**

Before generating any code, analyze the feature requirements against template constraints. If violations are detected, **STOP and ERROR OUT** with clear guidance.

### **Account-Level Operations (❌ FORBIDDEN - FAIL IMMEDIATELY)**

These operations will FAIL in the learning environment and cannot be simulated meaningfully:

**Database Operations:**
```sql
-- ❌ WILL FAIL - Account-level database operations
CREATE DATABASE database_name;
ALTER DATABASE db_name ENABLE REPLICATION TO ACCOUNTS ('account');
CREATE DATABASE replica_db AS REPLICA OF source_account.source_db;
DROP DATABASE database_name;
SHOW DATABASES IN REPLICATION GROUP;
```

**Account & Warehouse Operations:**
```sql
-- ❌ WILL FAIL - Account-level modifications
CREATE WAREHOUSE warehouse_name;
ALTER ACCOUNT SET parameter = value;
CREATE ROLE role_name;
CREATE USER user_name;
```

**Cross-Account Operations:**
```sql
-- ❌ WILL FAIL - Requires multiple accounts
GRANT IMPORTED PRIVILEGES ON DATABASE shared_db TO ROLE role_name;
CREATE SHARE share_name;
ALTER SHARE share_name ADD ACCOUNT = 'target_account';
```

**External Dependencies:**
```sql
-- ❌ WILL FAIL - External integrations
CREATE STORAGE INTEGRATION s3_integration;
CREATE NOTIFICATION INTEGRATION sns_integration;
COPY INTO table FROM @external_stage;
```

### **🛑 Constraint Detection Algorithm**

When planning code generation, check for these patterns and **FAIL IMMEDIATELY**:

1. **Database-level DDL**: `CREATE DATABASE`, `ALTER DATABASE`, `DROP DATABASE`
2. **Account-level objects**: `CREATE WAREHOUSE`, `CREATE ROLE`, `CREATE USER`
3. **Cross-account references**: `account_name.database_name`
4. **Replication commands**: `ENABLE REPLICATION`, `AS REPLICA OF`, `REFRESH`
5. **External integrations**: `CREATE INTEGRATION`, `@external_stage`
6. **Account parameters**: `ALTER ACCOUNT SET`

### **🚫 Fail-Fast Response**

When constraint violations are detected, immediately return an error with this structure:

```
❌ TEMPLATE GENERATION FAILED: Learning Environment Constraints Violated

DETECTED VIOLATIONS:
- Database Replication (requires account-level privileges)
- Cross-account operations (requires multiple Snowflake accounts)

REASON FOR FAILURE:
This feature cannot be demonstrated in the Snowflake Learning Environment due to 
privilege restrictions. The learning environment only allows schema-level operations
within a single account.

ALTERNATIVE APPROACHES:
1. Create a conceptual/educational template explaining the feature
2. Focus on related features that work within schema constraints
3. Create documentation-only template with step-by-step instructions

SUGGESTED ALTERNATIVE FEATURES:
- Schema-level data sharing using views
- Table cloning and time travel
- Data transformation pipelines
- Query optimization techniques

PRODUCTION DOCUMENTATION:
For actual database replication setup, users should refer to:
- https://docs.snowflake.com/en/user-guide/db-replication-config
- https://docs.snowflake.com/en/user-guide/account-replication-config
```

## 🎯 **Updated Step 2 Process**

### **New Fail-Fast Process:**
1. **Analyze feature requirements** for constraint violations
2. **If violations detected**: 
   - **STOP immediately**
   - **Return constraint violation error**
   - **Suggest alternative approaches**
   - **Do NOT generate code**
3. **If no violations**: Proceed with normal code generation
4. **Choose file format** (SQL or Python)
5. **Generate core code**: setup, data creation, feature demo, cleanup
6. **Follow code conventions** (ALL CAPS SQL, proper formatting)
7. **Exclude Streamlit components**

### **Constraint-Compatible Features Only**

Templates should only be created for features that can work within these constraints:

✅ **Schema-level operations**: Tables, views, procedures, functions  
✅ **Data manipulation**: INSERT, UPDATE, DELETE, SELECT  
✅ **Data transformation**: CTEs, window functions, aggregations  
✅ **Built-in functions**: String, date, math, conditional functions  
✅ **Query optimization**: Clustering, partitioning (at table level)  
✅ **Time travel**: Table-level time travel and cloning  
✅ **Semi-structured data**: JSON, VARIANT operations  
✅ **User-defined functions**: SQL and JavaScript UDFs  
✅ **Stored procedures**: Within schema scope  

❌ **Account-level features**: Replication, sharing, account management  
❌ **Cross-account operations**: Multi-account scenarios  
❌ **External integrations**: Storage integrations, external stages  
❌ **Infrastructure management**: Warehouses, roles, users  

## 📋 **Pre-Generation Constraint Checklist**

Before generating ANY code, verify the feature is compatible:

✅ **Can be demonstrated within a single schema**
✅ **Requires only SNOWFLAKE_LEARNING_ROLE privileges**  
✅ **Uses only SNOWFLAKE_LEARNING_DB database**
✅ **No external dependencies or integrations**
✅ **No cross-account operations required**
✅ **No account-level object creation/modification**
✅ **Completable in under 5 minutes**

**If ANY item fails**: STOP and return constraint violation error.

## 🔧 **Implementation Example**

**❌ BAD - Would generate failing code:**
```sql
-- This would fail in Step 3 validation
CREATE DATABASE PRIMARY_DB;
ALTER DATABASE PRIMARY_DB ENABLE REPLICATION TO ACCOUNTS ('DR_ACCOUNT');
```

**✅ GOOD - Fails fast with clear error:**
```
❌ TEMPLATE GENERATION FAILED: Database Replication Constraints

REASON: Database replication requires account-level privileges not available 
in the Snowflake Learning Environment.

ALTERNATIVE: Consider creating a template for table cloning and time travel,
which provides similar data protection concepts within schema constraints.
```

## 🎯 **Benefits of Fail-Fast Approach**

✅ **Clear Expectations** - Users know immediately if a feature can't be templated  
✅ **No Confusion** - No misleading simulations that don't represent real functionality  
✅ **Better UX** - Honest about limitations rather than fake demonstrations  
✅ **Focus Resources** - Only spend time on features that can work properly  
✅ **Quality Control** - Ensures all templates are genuinely executable  
✅ **Educational Integrity** - Templates show real features, not approximations  

## 🚀 **Recommended Alternative Features**

Instead of constraint-violating features, focus on these rich areas:

### **Data Transformation & Analytics**
- Advanced SQL techniques (window functions, CTEs, pivots)
- Semi-structured data processing (JSON, XML, VARIANT)
- Time series analysis and forecasting
- Statistical functions and data science SQL

### **Performance & Optimization**  
- Query optimization techniques
- Table clustering strategies
- Materialized views and caching
- Efficient data loading patterns

### **Data Quality & Governance**
- Data validation and quality checks
- Masking and privacy functions (within schema)
- Data lineage tracking
- Audit logging patterns

### **Modern Data Stack Integration**
- dbt model development patterns
- ELT pipeline design
- Data testing strategies
- Documentation generation

This approach ensures every template provides genuine value while working within the learning environment constraints.
