# Step 8: Validate assembled template.

## Objective
If the generated template file from previous step is a SQL file, we can skip this step. Otherwise we should validate if the generated file is a valid Notebook file. 

## Process
1. Read and validate if the generated Notebook file is valid.
2. If it's not, try to fix the syntax issue with notebook file without maniputlating its logic.

## Output
Modified template file (if it was invalid). Modification will be in the original file, no need to create a new file.
