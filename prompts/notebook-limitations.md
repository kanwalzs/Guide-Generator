## Caveats

### Format Selection Guidelines
- **Notebook Format**: 
  - ML/AI workflows, data science explorations
  - Multi-step processes with visualizations
  - Python-heavy implementations
  - Complex data transformations

For SQL cells, use 

```
   "metadata": {
    "vscode": {
     "languageId": "sql"
    },
    "language": "sql",
    "name": "IMPORT_DATA"
   },
```

instead of

```
   "metadata": {
    "language": "sql",
    "name": "IMPORT_DATA"
   },
```

### 🚨 CRITICAL: Notebook Tool Limitations

**The NotebookEdit tool has SEVERE limitations that will break your notebook if not handled correctly:**

#### Problem 1: Wrong Cell Types and Metadata
NotebookEdit does NOT automatically add proper SQL metadata. When using NotebookEdit to insert SQL code cells, they will be created as **Python cells** with basic metadata, causing serious formatting issues.

**What you get (WRONG):**
```json
{
  "cell_type": "code",
  "source": "# SQL code wrapped in Python triple quotes\ncovid_data = \"\"\"\nCREATE TABLE...\n\"\"\"\nsession.sql(covid_data).collect()",
  "metadata": {}
}
```

**What you need (CORRECT):**
```json
{
  "cell_type": "code", 
  "source": "CREATE TABLE COVID_DATA AS...",
  "metadata": {
    "vscode": {
     "languageId": "sql"
    },
    "language": "sql",
    "name": "CREATE_DATA"
   }
}
```

#### Problem 2: Cell Order Chaos
NotebookEdit inserts cells in unpredictable order, often resulting in:
- Step 3 appearing before Step 2
- Introduction cells appearing at the bottom
- Completely scrambled cell sequence

#### Problem 3: Code Structure Issues
SQL code gets wrapped in Python with triple quotes instead of being pure SQL cells, making it:
- Harder to read and maintain
- Incompatible with Snowflake's SQL execution environment
- Missing proper syntax highlighting

### ⚠️ RECOMMENDED APPROACHES:

**Option 1 (STRONGLY RECOMMENDED): Write Complete Notebook**
```
Write -> Complete .ipynb JSON with proper structure and SQL metadata for ALL cells
```

**Option 2 (HIGH MAINTENANCE): NotebookEdit + Manual Fixes**
```
NotebookEdit -> Insert SQL cell -> Edit -> Fix metadata AND cell order
```
*Note: You must fix EVERY SQL cell's metadata immediately after insertion*

**Option 3 (AVOID): Using NotebookEdit without fixes**
```
❌ NotebookEdit -> Insert SQL cell -> Results in broken notebook
```

### 🔍 How to Verify Your Notebook
Always read your generated notebook with `NotebookRead` to check:
1. ✅ Cells are in correct order (Step 1, Step 2, Step 3...)
2. ✅ SQL cells have proper `"vscode": {"languageId": "sql"}` metadata  
3. ✅ SQL code is pure SQL, not wrapped in Python triple quotes
4. ✅ Cell types match content (markdown for explanations, code for executable content)

### 📋 Template Assembly Best Practice
For notebook templates containing SQL:
1. Plan the complete notebook structure first
2. Use `Write` tool to create the entire .ipynb file at once
3. Include proper SQL cell metadata from the beginning
4. Verify with `NotebookRead` before completing
