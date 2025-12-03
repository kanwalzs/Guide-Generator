# Template Requirements

## Overview

Templates in Snowsight are designed to showcase features and use cases in a quick, engaging, and interactive manner. They provide bite-sized, executable demonstrations that users can complete **in under 5 minutes**.

## Technical Requirements

### Environment & Setup
- **Must use Learning Environment**: 
  - `SNOWFLAKE_LEARNING_ROLE`
  - `SNOWFLAKE_LEARNING_DB` 
  - `SNOWFLAKE_LEARNING_WH`
- **Standard environment setup script**:
  ```sql
  USE ROLE SNOWFLAKE_LEARNING_ROLE;
  USE WAREHOUSE SNOWFLAKE_LEARNING_WH;
  USE DATABASE SNOWFLAKE_LEARNING_DB;
  SET schema_name = CONCAT(current_user(), '_<TEMPLATE_ID>');
  USE SCHEMA IDENTIFIER($schema_name);
  ```

### Data & Dependencies
- **Self-contained**: Must create own sample data or use pre-loaded S3 data (not available now)
- **No external dependencies**: Cannot rely on external services or accounts
- **Executable without setup barriers**: Users should be able to run immediately

### File & Structure Requirements
- **Single file**: All SQL and Python code must be combined into one `.ipynb` or `.sql` file. Notebook format is preferred if unspecified.
- **Schema-level only**: Can only create objects within template's unique schema
- **No account-level changes**: Cannot modify account parameters or create account-level objects
- **Time limit**: Must be completable in under 5 minutes (some sources say under 10 minutes)

### Cleanup Requirements
- **Cleanup at start**: Remove any existing objects from previous runs
- **Cleanup at end**: Clean up all created resources when finished
- **No destructive changes**: Cannot make changes that cannot be undone

## Content Requirements

### Structure & Format
Each template must include:

1. **Title** (36 characters max, 40 absolute max)
   - Clear, descriptive, concise
   - For introductory templates: "Intro to X"
   - For use cases: Start with verb (e.g., "Analyze Customer Churn with SQL")
   - For reference: "Quick Reference: [Topic]"

2. **Overview** (1-3 sentences)
   - Summarize what the template does
   - State the value/outcome user will achieve
   - Include business context when relevant

3. **Steps** 
   - Ordered instructions guiding execution
   - Each code block preceded by markdown explanation
   - Progressive complexity

4. **Key Takeaways**
   - Reinforce learning or outcome
   - Highlight main insights

5. **Additional Resources**
   - Links to relevant documentation
   - Related templates
   - Link to Templates hub (app.snowflake.com/templates)

### Content Standards

**Focus & Scope**:
- **Single feature or use case**: Avoid combining multiple unrelated concepts
- **Practical and hands-on**: Minimize theory, focus on action
- **Clear explanations**: Suitable for all experience levels
- **Actionable outcomes**: Guide users to key insights or completed tasks

**Tone & Voice**:
- Use **active voice** ("Run this query" vs "This query can be used")
- **Conversational but professional**
- Avoid jargon, spell out acronyms on first use
- Use contractions where natural

**Common Pitfalls to Avoid**:
- Too much theory
- Overwhelming details
- Assuming advanced knowledge

## Code Conventions

### SQL Standards
- **ALL CAPS** for SQL keywords (`SELECT`, `FROM`, `WHERE`)
- Code should be **executable without modification**
- Include code descriptions in markdown before each code block
- Use code comments to explain complex logic
- Proper formatting and indentation

### Python Standards
- Import necessary packages clearly
- Use Snowflake session management: `get_active_session()`
- Include Streamlit components when appropriate
- Follow Python best practices

### Snowflake API Access

The notebook can invoke Snowflake REST API with Python code using the built-in `_snowflake` library. A sample usage would be:

```python
import _snowflake

resp = _snowflake.send_snow_api_request(
    "POST", # method
    f"/api/v2/cortex/analyst/message",  # path
    {},  # headers
    {},  # params
    request_body,  # body
    None,  # request_guid
    30000,  # timeout in milliseconds
)

# Content is a string with serialized JSON object
parsed_content = json.loads(resp["content"])

# Check if the response is successful
if resp["status"] < 400:
    # Return the content of the response as a JSON object
    return parsed_content, None
```

### Output token limit

The LLM max output token is set to 8192 so that you might want to incrementally append to the output template file. Writing a single big file might end up in a deadloop.

