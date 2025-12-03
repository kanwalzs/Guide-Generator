# Step 3.5: Sanity Check

## Objective
Ensure that Step 3 was validated against a real Snowflake environment with actual runtime execution. This step exists because Step 3 is frequently done incorrectly with static validation instead of real runtime testing.

## Process

### 1. **Verify Step 3 Was Actually Executed**
Check for evidence that Step 3 validation script was run against live Snowflake:

**✅ Required Evidence:**
- Validation script exists (e.g., `validation_[template_id].py`)
- Script contains real Snowflake connection setup
- All code paths have assertion-based validation
- Mock modules created for external dependencies
- Script can be executed standalone (not in notebook)

**❌ Red Flags (Step 3 NOT properly done):**
- Only static code review was performed
- No actual SQL execution against Snowflake
- Claims of validation without execution evidence
- Missing validation scripts or incomplete coverage
- Attempts to use notebook execution tools
- Falls back using a different feature because of challenges or validation failures. 

### 2. **Test Key Validation Points**
If Step 3 appears incomplete, verify these critical areas were tested:

**🔍 Database Operations:**
- Environment setup (role, warehouse, database, schema)
- Sample data creation with expected row counts
- Object creation (tables, views, semantic views)
- Query execution with result validation
- Complete resource cleanup

**🔍 Syntax Validation:**
- Semantic view creation with correct Snowflake syntax (DIMENSIONS before METRICS, proper table.column format)
- All SQL statements execute without compilation errors
- Business logic calculations produce reasonable results
- Complex SQL features tested against actual Snowflake parser (not just syntax checkers)

**🔍 Integration Testing:**
- Session management works throughout execution
- External API calls handled appropriately (with mocks if needed)
- Error handling gracefully manages failures

**🔍 Feature usage:**
- Should be using exactly the feature as requested in the planning doc. 

### 3. **Action Required If Step 3 Incomplete**

If Step 3 was NOT properly validated against real Snowflake:

1. **STOP immediately** - Do not proceed to subsequent steps
2. **Go back and fix Step 3** - Create proper validation script
3. **Execute actual runtime testing** - Run against live Snowflake environment  
4. **Document validation results** - Show evidence of successful execution
5. **Complete Step 3.5** - Only after Step 3 is properly done

## Success Criteria

**✅ Step 3.5 passes only if:**
- Step 3 validation script exists and is executable
- Script was run against live Snowflake environment
- All assertions passed during execution
- Evidence of successful runtime testing is documented
- No syntax errors or runtime failures occurred

**❌ Step 3.5 fails if:**
- Step 3 was only static validation without execution
- Validation script missing or incomplete
- Claims of validation without actual runtime testing
- Syntax errors discovered during real usage
- A desired feature was revereted in step 3 because of validation failure.

## 🎓 Common Step 3.5 Findings

### **Finding 1: Fake Validation Reports**
**Problem**: Step 3 reports claim successful validation but no actual execution occurred
**Evidence**: User reports syntax errors when running template, proving validation was never done
**Action**: Require actual execution proof and fix all discovered issues

### **Finding 2: Incomplete Coverage**  
**Problem**: Step 3 tested some parts but missed critical components like semantic view syntax
**Evidence**: Template fails at specific operations that should have been validated
**Action**: Expand validation to cover all code paths and operations

### **Finding 3: Environment Issues**
**Problem**: Step 3 validation didn't test actual Snowflake connection setup
**Evidence**: Authentication, permission, or session configuration errors in real usage
**Action**: Include connection testing as first validation step

### **Finding 4: Semantic View Syntax Failures**
**Problem**: Step 3 didn't validate complex SQL syntax like semantic views against live Snowflake
**Evidence**: User reports "unexpected 'AS'" or "unexpected 'DIMENSIONS'" SQL compilation errors
**Action**: Must test semantic view creation syntax with proper DIMENSIONS before METRICS order and table.column format
**Common Errors**: Wrong order (METRICS before DIMENSIONS), missing table aliases, missing aggregation functions

## Output

**If Step 3.5 Passes:**
- Step 3 was properly validated against real Snowflake
- Template code is ready for assembly
- All runtime issues have been resolved

**If Step 3.5 Fails:**
- Return to Step 3 with mandatory runtime execution
- Do not proceed until actual validation is complete
- Document and fix all discovered issues