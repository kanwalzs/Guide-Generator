# Step 2: Core Code Generation

## Context
Read the following files to refresh your memory / context:
- `prompts/new-template-generation-workflow.md`
- `prompts/template-requirements.md`

## Objective
Generate a SQL file or Python file containing all necessary code in a single file for validation. This does not include Streamlit code snippets if using Notebook format.

## Input
- Template concept from Step 1

## Process
1. Choose file format (SQL or Python)
2. Generate core code: setup, data creation, feature demo, cleanup
3. Follow code conventions (ALL CAPS SQL, proper formatting)
4. Exclude Streamlit components

## 🎯 Advanced Feature Syntax Guidelines

### Semantic Views (CREATE SEMANTIC VIEW)
If creating semantic views, follow these **critical syntax requirements**:

**✅ CORRECT Format:**
```sql
CREATE OR REPLACE SEMANTIC VIEW view_name
  TABLES (
    table_alias AS physical_table
  )
  DIMENSIONS (
    table_alias.column_name AS table_alias.column_name
      WITH SYNONYMS = ('synonym1', 'synonym2', 'synonym3')
      COMMENT = 'Dimension description',
    -- More dimensions...
  )
  METRICS (
    table_alias.metric_name AS AGGREGATION_FUNCTION(table_alias.column_name)
      WITH SYNONYMS = ('synonym1', 'synonym2', 'synonym3')
      COMMENT = 'Metric description',
    -- More metrics...
  )
  COMMENT = 'Semantic view description'
```

**❌ Common Mistakes to AVOID:**
- NEVER put METRICS before DIMENSIONS (order matters!)
- NEVER omit table alias: `column AS column` (wrong) vs `table.column AS table.column` (correct) 
- NEVER forget aggregation functions in METRICS: `total_cases` (wrong) vs `SUM(table.total_cases)` (correct)
- NEVER use incorrect synonym format: `SYNONYMS = 'single'` (wrong) vs `SYNONYMS = ('single', 'multiple')` (correct)
- AVOID import * from a package. For example, avoid `from snowflake.snowpark.functions import *`

**🔍 Validation Requirements:**
- All METRICS must use aggregation functions (SUM, AVG, COUNT, etc.)
- DIMENSIONS section must come before METRICS section
- Each dimension/metric must use fully qualified `table_alias.column_name` format
- Synonyms help AI tools understand business terminology

## Output
Single executable file with all core functionality: `generated-templates/<template_id>/code.sql` or `generated-templates/<template_id>/code.py`

Pay attention that your max output token is set to 8192 so that you might want to incrementally append to the output file. Writing a single big file might end up failing.
