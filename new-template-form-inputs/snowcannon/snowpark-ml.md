# High-level idea

Demonstrate end-to-end machine learning workflows using Snowpark ML, from feature engineering to model training and deployment, all within Snowflake.

# Feature details & references

Show how to:
- Use Snowpark ML preprocessing and feature engineering
- Train models using built-in algorithms
- Register models in the Snowflake Model Registry
- Deploy models for batch inference
- Use model versioning and lifecycle management
- Monitor model performance

Documentations:
* [Snowpark ML Overview](https://docs.snowflake.com/en/developer-guide/snowflake-ml/overview)
* [Snowpark ML Modeling](https://docs.snowflake.com/en/developer-guide/snowflake-ml/modeling)
* [Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview)

# Test data setup

Use TPC-H tables (CUSTOMER, ORDERS, LINEITEM) to build a customer churn or demand forecasting model. Create derived features from order history and customer segments.

# Format

Use snowflake notebook.

# Length

Normal.

# Additional notes

Include model evaluation metrics, feature importance analysis, and comparison of different algorithms. Show both training and inference pipelines.