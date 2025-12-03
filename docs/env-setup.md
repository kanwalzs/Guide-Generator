### Template Content Requirements

* Each template must be stand-alone. If the template depends on data or an entity, it must create it.   
* Templates should help the user achieve a goal or build an app in less than 10 minutes.  
* Each template should have a unique identifier  
* Templates should use the learning environment. The learning environment is made up of: SNOWFLAKE\_LEARNING\_DB, SNOWFLAKE\_LEARNING\_ROLE and SNOWFLAKE\_LEARNING\_ROLE. Set the learning environment as the context using the following script for consistency across templates:

```
---> set the Role
USE ROLE SNOWFLAKE_LEARNING_ROLE;

---> set the Warehouse
USE WAREHOUSE SNOWFLAKE_LEARNING_WH;

---> set the Database
USE DATABASE SNOWFLAKE_LEARNING_DB;

---> set the Schema
SET schema_name = CONCAT(current_user(), '_<TEMPLATE_ID>'); //Replace with template id, underscore expected before template id
USE SCHEMA IDENTIFIER($schema_name);
```

* Template can only create new entities in its corresponding schema as set above. Account level objects should not be created in the template.  
* Templates must be in one file. If the template is made up of multiple sql and python files, they must be combined into one.  
* Cannot include any changes that are destructive to the account or cannot be undone. For example, changing account level parameters without saving the current parameter value first is not allowed.  
* All templates should clean up any changes made at the end of the template.   
* The template should contain comments to help users understand the concepts presented in the template. There is no additional guide or quickstart to help the user understand the content.