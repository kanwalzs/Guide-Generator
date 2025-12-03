# Step 5: Streamlit Generation (If Needed)

## Context
Read the following files to refresh your memory / context:
- `prompts/new-template-generation-workflow.md`
- `prompts/template-requirements.md`

## Objective
Generate Python file with Streamlit snippets.

## Input
- Decision from Step 4 to include Streamlit
- Validated core code from Step 3

## Process
Generate necessary Streamlit snippets
- The snippets must be able to fit into a notebook.
- The snippets should be simple and functional. The main goal is to demonstrate the ability of the snowflake feature used in the template, but is not to demonstrate the ability of streamlit.

This notebook is running in acaconda. So avoid using unnecessary / unavailable packages like `plotly[express]` (where plotly is available).

## Output
Python file containing Streamlit code snippets: `generated-templates/<template_id>/streamlit_code.py`