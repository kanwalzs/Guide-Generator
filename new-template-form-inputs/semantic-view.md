# High-level idea
Creation of new semantic views, and then consumption view Snowsight SQL, Streamlit, and Cortex Analyst
Step 1: Set up your Database and Schema
Step 2: Create Views from Sample Data
Step 3: Verify your Environment Setup
Step 4: Define the Semantic View
Step 5: Verify the Semantic View Creation
Step 6: Describe the Semantic View
Step 7: "Talk To" the Semantic View with Cortex Analyst
Step 8: Query the Semantic View Using SQL
Step 9 (Optional): Build an Interactive Data App
App 1. Interactive Data Visualization
App 2. Dashboard

# Feature details & references
Snowflake Semantic Views natively store your semantic model—business dimensions, metrics, relationships, and definitions—directly inside the Snowflake database, ensuring a single, consistent semantic foundation for AI, BI tools, and SQL analysis. By embedding metadata like synonyms, sample values, and verified queries, Semantic Views help eliminate ambiguity, reduce "hallucinations" in conversational analytics, and foster trust across enterprise insights. Whether accessed via Cortex Analyst, BI dashboards, notebooks, or SQL clients, these semantic definitions drive unified, governed, and accurate analytics at scale. As a result, organizations can unlock AI-powered business intelligence confidently and efficiently, knowing every query honors the same shared business logic.

Documentations:
* https://docs.snowflake.com/en/user-guide/views-semantic/overview
* https://docs.snowflake.com/en/user-guide/views-semantic/sql
* https://docs.snowflake.com/en/user-guide/views-semantic/example
* https://docs.snowflake.com/en/user-guide/views-semantic/ui
* https://docs.snowflake.com/en/user-guide/views-semantic/validation-rules
* https://docs.snowflake.com/en/user-guide/views-semantic/querying
* https://docs.snowflake.com/en/user-guide/ui-snowsight-data-databases-view
* https://docs.snowflake.com/user-guide/views-semantic/sql

# Test data setup

use the covid dataset from the snowflake marketplace: https://app.snowflake.com/marketplace/listing/GZSNZ7F5UH/starschema-covid-19-epidemiological-data

# Format

Use snowflake notebook

# Length

Normal.

# Additional notes

None