# Step 7: Template Assembly

Read the following files to refresh your memory / context:
- `prompts/new-template-generation-workflow.md`
- `prompts/template-requirements.md`
- `prompts/notebook-limitations.md`

## Objective
Convert all generated files into the final template (SQL file or Notebook file).

## Input
- Template concept from Step 1 (must have)
  `generated-templates/<template_id>/plan.md`
- Validated core code from Step 3 (must have)
  `generated-templates/<template_id>/code.(sql/py)`
- Streamlit snippets from Step 5 (if applicable)
  `generated-templates/<template_id>/streamlit_code.py`

## Process
**SQL Templates**: Add background story, instructions for each SQL block, summaries, and additional materials to the original SQL file.

**Notebook Templates**: Combine Python file and Streamlit snippets, inserting Streamlit code at appropriate locations with markdown explanations.

### ⚠️ CRITICAL: Notebook Creation Approach

**RECOMMENDED APPROACH (Use This):**
1. Create complete notebook as a text file (`.txt`) using the `Write` tool
2. Include proper JSON structure with all cells, metadata, and SQL cell formatting
3. Rename the `.txt` file to `.ipynb` using bash `mv` command
4. Verify with `NotebookRead` to ensure proper structure

**Example workflow:**
```bash
# Create complete notebook structure in a text file
Write -> template.txt (complete .ipynb JSON structure)
# Rename to proper extension  
mv template.txt final-template.ipynb
# Verify structure
NotebookRead -> final-template.ipynb
```

### ❌ AVOID: NotebookEdit Tool Issues

- **NEVER USE the tool `NotebookEdit` for creating or appending cells**
- NotebookEdit causes cell order chaos, wrong metadata, and formatting issues
- NotebookEdit wraps SQL in Python triple quotes instead of proper SQL cells
- Results in broken notebooks that don't execute properly in Snowflake

### 📋 Notebook Structure Requirements

When creating the notebook text file, ensure:
- Proper SQL cell metadata: `"vscode": {"languageId": "sql"}, "language": "sql", "name": "CELL_NAME"`
- Correct cell ordering (Step 1, Step 2, Step 3...)
- Pure SQL code in SQL cells (not wrapped in Python)
- Markdown cells for explanations and structure
- Always read `prompts/notebook-limitations.md` before starting

### 🎯 Advanced SQL Feature Assembly

**For Complex SQL Features (Semantic Views, etc.):**
- Use EXACT syntax validated in Step 3 - do not modify working syntax during assembly
- Preserve critical syntax elements like DIMENSIONS before METRICS order
- Include syntax comments explaining key requirements for user reference
- Test final assembled template if any modifications were made to validated code
- For semantic views, maintain table.column AS table.column format throughout

## Output
Final template file (.sql or .ipynb) ready for user execution. This should just be a single file.

The LLM max output token is set to 8192 so that you might want to incrementally append to the output template file. Writing a single big file might end up in a deadloop.
