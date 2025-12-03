# New Template Generation Workflow

The generation of a new template follows these steps:

## Step 1: Template Planning
Read user inputs and template generation requirements. Draft a high-level plan for structuring the template, covering what will be included, the steps, background story, and materials. Revise user input into a concrete template idea.

## Step 2: Core Code Generation  
Generate a SQL file or Python file containing all necessary code in a single file for validation. This does not include Streamlit code snippets if using Notebook format.

## Step 3: Code Validation
Validate the generated SQL file or Python file to ensure it executes successfully.

## Step 4: Streamlit Assessment
Decide if Streamlit snippets are needed (typically for Notebook templates). If not needed, skip Steps 5-6. Otherwise, generate a Python file for Streamlit snippets.

## Step 5: Streamlit Generation (If Needed)
Generate Python file with Streamlit snippets.

## Step 6: Streamlit Validation (If Generated)
Validate Streamlit snippets work correctly. This requires executing all data setup from the previous Python or SQL file without cleaning up data, then testing that Streamlit snippets render correctly.

## Step 7: Template Assembly
Convert all generated files into the final template (SQL file or Notebook file):

- **SQL Templates**: Use the original SQL file and add background story, instructions for each SQL block, summaries, and additional materials
- **Notebook Templates**: Combine the original Python file and Streamlit snippets, inserting Streamlit code at appropriate locations