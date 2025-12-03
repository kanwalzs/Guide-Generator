# Step 3: Code Validation

## Objective
**CRITICAL: Execute and validate EVERY line of generated code** against a live Snowflake session to ensure complete end-to-end functionality. This step requires **actual runtime execution** - static validation is insufficient.

## ⚠️ MANDATORY REQUIREMENTS
- **Execute ALL SQL statements** - Every CREATE, SELECT, INSERT, DROP command must run successfully
- **Call ALL Python functions** - Every function must be invoked and tested 
- **Verify ALL operations** - Data creation, semantic views, queries, cleanup must be validated
- **Test complete workflow** - Full script execution from start to finish required
- **Use real Snowflake session** - No mocking or simulation allowed

## Input
- Code file from Step 2 (.sql or .py)
- **Active Snowflake validation session** with appropriate credentials
- Validation tools (`snowsql -c validation` for SQL, isolated Python environment for Python)

## ❌ WHAT THIS IS NOT:
- **NOT static validation** - Syntax checking alone is insufficient
- **NOT code review** - Manual inspection without execution is inadequate  
- **NOT simulation** - Mock testing or dry runs do not count
- **NOT partial testing** - Every line of code must be executed

## ✅ WHAT THIS IS:
- **Runtime execution** against live Snowflake environment
- **End-to-end testing** of complete workflow
- **Data verification** with actual query results
- **Integration testing** of all components working together

## Process

### For SQL Files
1. **Execute complete SQL script**: Run `snowsql -c validation -f "FILENAME.sql"`
2. **Verify every operation**:
   - ✅ All tables/views/semantic views created successfully
   - ✅ All data inserted correctly with expected row counts
   - ✅ All queries return valid results
   - ✅ All cleanup commands execute without errors
   - ✅ No orphaned objects remain after cleanup
3. **Test individual statements**: Re-run each major SQL block separately to isolate any issues
4. **Validate semantic view functionality**: If present, test semantic view queries and metadata

### For Python Files
1. **Create isolated virtual environment**:
   ```bash
   python -m venv venv_validation_[TEMPLATE_ID]
   source venv_validation_[TEMPLATE_ID]/bin/activate
   ```
   Detect and install required packages by analyzing imports in the Python file.

2. **Create enhanced validation version** of the Python file:
   - Add explicit validation checks after each major operation
   - Verify objects exist (tables, views, semantic views)  
   - Add assertion statements to confirm expected results
   - Include error handling with detailed logging
   - **IMPORTANT**: Replace `import _snowflake` with `import sys; sys.path.insert(0, '../../'); import local_snowflake as _snowflake`
     - Use the **real API implementation** from project root: `/home/huguo/ai-templates/growth-generated-templates/local_snowflake.py`
     - This provides actual Cortex Analyst REST API calls, not mock responses
     - Do NOT create template-specific mock files - use the project's real implementation
   - Add validation session setup at the beginning of the file:
     ```python
     from snowflake.snowpark import Session
     # Create validation session - all get_active_session() calls will use this
     Session.builder.config("code-validation", "validation").create()
     ```

3. **Execute validation script with FULL RUNTIME TESTING**:
   
   **🚨 CRITICAL: DO NOT RUN IN A NOTEBOOK - Use standalone Python execution only**
   
   ```bash
   python validation_[TEMPLATE_NAME].py
   ```
   **MUST execute every single function and code path:**
   - ✅ Call every function defined in the code
   - ✅ Execute all SQL statements through session.sql()
   - ✅ Verify all data creation operations
   - ✅ Test all query operations return expected results
   - ✅ Validate all calculations and business logic
   - ✅ Confirm all API calls (like Cortex Analyst) handle correctly
   - ✅ Test complete cleanup workflow

4. **Verify execution results with DETAILED VALIDATION**:
   - ✅ All operations complete without errors
   - ✅ All validation checks pass with expected data volumes
   - ✅ All created objects are queryable and contain expected data
   - ✅ All calculations produce reasonable results
   - ✅ Proper cleanup occurs - verify by querying for remaining objects
   - ✅ Resource cleanup verified - no orphaned tables/views/schemas
   - ✅ Session management works correctly throughout execution
   - ✅ Error handling gracefully manages expected failure scenarios

5. **Remove validation logic and merge back**:
   - Remove extra debugging and validation assertions from validation file
   - Verify cleaned file still executes correctly
   - Merge improvements back to original Python file with these reverts:
     - Replace `import sys; sys.path.insert(0, '../../'); import local_snowflake as _snowflake` with `import _snowflake`
     - Remove validation session setup (keep original `get_active_session()` calls unchanged)
   - Keep original imports and session management in the final file
   - **Note**: The original template uses `import _snowflake` which works in Snowflake Notebook environments

6. **Clean up validation environment**:
   ```bash
   deactivate
   rm -rf venv_validation_[TEMPLATE_ID]
   ```

## Output
- **For SQL**: 
  - **Original**: `generated-templates/<template_id>/code.sql` validated and updated
  - **Validation version**: `generated-templates/<template_id>/validate_code.sql` kept for future runs
- **For Python**: 
  - **Original**: `generated-templates/<template_id>/code.py` validated and updated  
  - **Validation version**: `generated-templates/<template_id>/validate_code.py` kept for future runs
  - **Validation execution report**: Confirming all operations work
  - **Clean virtual environment removal**

## Success Criteria

### 🎯 MANDATORY RUNTIME VALIDATION REQUIREMENTS:
1. **Complete execution success**: Code runs from start to finish without any errors
2. **All database operations verified**: Every CREATE, INSERT, SELECT, DROP command executes successfully
3. **Data validation**: All created objects contain expected data with correct row counts and values
4. **Query functionality**: All SELECT queries return reasonable results matching business logic
5. **API integration**: All external API calls (Cortex Analyst, etc.) handle gracefully with appropriate responses
6. **Resource management**: All cleanup operations execute successfully with verified object removal
7. **Session management**: Snowflake session connectivity works throughout entire execution
8. **Business logic validation**: All calculated fields, metrics, and transformations produce expected results

### 🔍 VERIFICATION CHECKLIST:
- ✅ **No syntax errors** in any code execution
- ✅ **No runtime errors** during full script execution  
- ✅ **All functions called** and tested successfully
- ✅ **All data created** with expected volumes and structure
- ✅ **All queries tested** and return valid business data
- ✅ **All cleanup verified** by confirming object deletion
- ✅ **Session credentials** work with validation environment
- ✅ **End-to-end workflow** completes successfully in under 5 minutes

## 🚨 VALIDATION FAILURE PROTOCOL

If **ANY** aspect of runtime validation fails:

1. **STOP immediately** - Do not proceed to subsequent steps
2. **Document the failure** - Record exact error messages and failure points
3. **Fix the code** - Address the root cause of the failure
4. **Re-run complete validation** - Full runtime testing required again
5. **Repeat until success** - No partial passes accepted

**Common failure scenarios:**
- ❌ SQL syntax errors in semantic view creation
- ❌ Data type mismatches in sample data
- ❌ Missing dependencies or imports
- ❌ Authentication/permission issues
- ❌ Resource cleanup failures leaving orphaned objects
- ❌ Query results not matching expected business logic
- ❌ API integration failures (Cortex Analyst, etc.)

**Resolution requirement:** ALL failures must be completely resolved with successful re-validation before proceeding to subsequent template generation steps.

## 🎓 CRITICAL LEARNINGS - AVOID THESE MISTAKES

### ❌ **MISTAKE 1: Claiming validation without actual execution**
**Problem**: Creating validation scripts but not actually running them against live Snowflake, then claiming validation was successful
**Solution**: Always execute the validation script in a real environment and show actual results with assertion outputs

### ❌ **MISTAKE 2: Using incorrect semantic view syntax**
**Problem**: Using outdated or incorrect CREATE SEMANTIC VIEW syntax leading to SQL compilation errors like "unexpected 'AS'" 
**Solution**: Always research current Snowflake documentation for semantic view syntax. Correct format:
```sql
CREATE SEMANTIC VIEW view_name
  TABLES (logical_table AS physical_table PRIMARY KEY (...))
  DIMENSIONS (dim_name AS column_name WITH SYNONYMS = (...) COMMENT = '...')
  METRICS (metric_name AS aggregation_expression COMMENT = '...')
```

### ❌ **MISTAKE 3: Attempting IDE execution for validation**
**Problem**: Trying to use `mcp__ide__executeCode` or notebook execution tools that require active notebook environments
**Solution**: Always create standalone Python scripts for validation that can be executed via `python script.py`

### ❌ **MISTAKE 4: Incomplete validation coverage**
**Problem**: Testing syntax without validating data creation, query results, business logic, and cleanup
**Solution**: Use comprehensive assertion-based validation for every operation:
```python
assert row_count == expected_count, f"Expected {expected_count}, got {row_count}"
assert len(query_results) > 0, "Query returned no results"
```

### ❌ **MISTAKE 5: Not using the project's real API implementation**
**Problem**: Code references `_snowflake` module that doesn't exist in validation environment, leading to creation of inadequate mocks
**Solution**: Always use the project's real API implementation from `/home/huguo/ai-templates/growth-generated-templates/local_snowflake.py`
- This provides actual REST API calls to Snowflake Cortex services
- Includes proper authentication, error handling, and response parsing
- Validates real integration patterns, not just mock responses

### ❌ **MISTAKE 6: Insufficient session configuration testing**
**Problem**: Assuming session configuration works without actually testing connection and permissions
**Solution**: Always test connection first with current user/account queries before proceeding

## Session Configuration

**🚨 IMPORTANT: Run validation as standalone Python script, NOT in notebooks**

### Environment Setup

1. **Copy connection configuration to working directory**:
   ```bash
   # Copy connections.toml to the template directory
   cp /home/huguo/ai-templates/growth-generated-templates/connections.toml .
   ```

2. **Verify TOML format** - All string values MUST be quoted:
   ```toml
   [validation]
   #Connection for validating generated templates
   accountname = "XHTGURV-JXB26700"  # MUST be quoted
   username = "HUAYANG"              # MUST be quoted  
   password = "Snowflake@2025"       # MUST be quoted
   authenticator = "snowflake"       # MUST be quoted
   ```
   **❌ COMMON ERROR**: Unquoted strings cause TOML parsing errors like `invalid literal for int() with base 0`

### Session Creation Approach

**✅ WORKING METHOD**: Create session directly using connection parameters

Add this at the beginning of your validation file:

```python
import toml
from snowflake.snowpark import Session
import sys
sys.path.insert(0, '../../')  # Add project root to Python path
import local_snowflake as _snowflake  # Use real API implementation

# Global session variable
_validation_session = None

def create_validation_session():
    """Create validation session using connections.toml"""
    global _validation_session
    
    if _validation_session is not None:
        return _validation_session
        
    try:
        # Read connection configuration from connections.toml
        config = toml.load("connections.toml")
        validation_config = config["validation"]
        
        # Create session directly with connection parameters
        connection_parameters = {
            "account": validation_config["accountname"],
            "user": validation_config["username"],
            "password": validation_config["password"],
            "authenticator": validation_config["authenticator"],
            "role": "SNOWFLAKE_LEARNING_ROLE",
            "warehouse": "SNOWFLAKE_LEARNING_WH",
            "database": "SNOWFLAKE_LEARNING_DB"
        }
        
        _validation_session = Session.builder.configs(connection_parameters).create()
        print("✅ Validation session created with connection parameters")
        return _validation_session
        
    except Exception as e:
        print(f"❌ Session creation failed: {e}")
        raise

# Replace get_active_session() calls with create_validation_session()
session = create_validation_session()  # Use direct session creation
```

**❌ DEPRECATED METHOD**: The following approach does NOT work reliably:
```python
# DON'T USE - This fails with "No default Session is found" errors
Session.builder.config("code-validation", "validation").create()
session = get_active_session()
```

### **Why NOT Notebooks?**
- Notebook environments may override session configuration
- `get_active_session()` behaves differently in notebook contexts
- Validation requires isolated, controlled execution environment
- Standalone Python scripts provide consistent session management

### **Proper Execution Method:**
```bash
# In your terminal/command line:
cd generated-templates/[template-id]/
python validate_code.py

# NOT in Jupyter/Snowflake notebooks
# NOT through notebook cell execution
```