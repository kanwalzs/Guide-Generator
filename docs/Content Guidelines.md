
# Template Hub in Snowsight: Content Guidelines

## 1\. Introduction & Purpose

Templates in Snowsight are designed to showcase features and use cases in a quick, engaging, and interactive manner. These guidelines are in place to ensure consistency, clarity, and value for end users.

Templates are different from the Quickstart & Solution Center content in that they are meant to be bite-sized, giving users a way to see a feature as end-to-end **in under 5 minutes**. Quickstarts are more geared towards  sales-assisted, more complex workflows

## 2\. Template Goals & Characteristics

### What Makes a Good Template?

* **Executable without setup barriers** – Uses SNOWFLAKE\_LEARNING\_ROLE, SNOWFLAKE\_LEARNING\_DB, SNOWFLAKE\_LEARNING\_WH environment and sample data (generated, pre-loaded, or pulled from S3).  
* **Focused on a single feature or use case** – Avoids combining multiple unrelated concepts in one template.  
* **Concise & Actionable** – Guides users to a key insight or completed task in less than 5 minutes.  
* **User-Centric** – Clearly communicates the value proposition, reducing cognitive load.  
* **Consistent Structure** – Follows a standardized format for easy consumption.

### Common Pitfalls to Avoid

* **Too much theory** – Templates should be practical and hands-on, descriptions and theory should be *directly* related to the action a user will take.  
* **Overwhelming details** – Keep explanations and tasks simple and focused.  
* **Assuming advanced knowledge** – Templates should have clear explanations that cater to all experience levels.

## 3\. Content Standards

See our full style guide for writing in Snowsight at: [Product writing style guide](https://docs.google.com/document/d/1hnxNfFMYTK9o1xKsoy5iatAV87S0zxmTmkMo61QQA3s/edit) (go/product-style-guide)

### Tone & Voice

* Use **active voice** (e.g., "Run this query to analyze trends" instead of "This query can be used to analyze trends").  
* Avoid jargon where possible and spell out acronyms on first use.  
* Be **conversational but professional** – use contractions where natural.

*Example*: 

✅ **Do This:**  
*Run the following SQL command to retrieve sales data:*

```
SELECT * FROM sample_data.sales;
```

🚫 **Don’t Do This:**  
*The query below will fetch sales data, which you might want to analyze:*

```
select * from sample_data.sales;
```

### Formatting & Structure

Each template should include:

1. **Title** – Clear, descriptive, concise. *\-* 36 characters (max 40\)  
2. **Overview** – 1-3 sentences summarizing what the template does and *the value or outcome* the user will achieve.  
3. **Steps** – Ordered instructions guiding the user through execution.  
4. **Key Takeaways** – Reinforce the learning or outcome.  
5. **Additional resources** – Include links to relevant documentation, other relevant templates or next steps, and to the Templates hub (app.snowflake.com/templates)

### Acronyms, Capitalization, & Punctuation

* Follow Snowflake’s **sentence case** standard (e.g., "Run a query in a worksheet").  
* Only capitalize proper nouns and branded terms (e.g., "Streamlit").  
* Use the Oxford comma for clarity in lists.

### Code Conventions

* Include descriptions of code in markdown prior to each code block.  
* SQL & Python should be **included as code blocks within a Snowflake notebook**.  
* Always use **ALL CAPS** for SQL commands (e.g., `SELECT * FROM table_name;`).  
* Code should be **executable without modification** where possible.  
* Where possible, simplify code and split out with markdown explanations of what is happening. Code comments should be used to describe what code is doing if the code block can’t be simplified. 

### Use of Visuals

* Use **screenshots or diagrams** only when they add clarity or help illustrate what the Template will cover.  
* Ensure images are **high resolution and properly cropped**.

### Naming Conventions

* **For introductory templates:** Use **“Intro to X”** (e.g., "Intro to Snowpark Functions").  
* **For general use cases:** Use a descriptive approach that starts with a verb (e.g., "Analyze Customer Churn with SQL").  
* **For reference templates or cheat sheets:** Use a straightforward name like "Quick Reference: Python Functions in Snowpark" to clearly indicate its purpose.  
* Keep **titles under 36 (max 40\)  characters** to avoid truncation.  
* Feature Highlighting vs. Use Case Focus  
* **Include the feature name** if showcasing a specific Snowflake capability.  
* **Focus on a use case** when emphasizing business value or outcome.

## 4\. Maintaining & Updating Templates

* **Templates should be reviewed regularly** to ensure compatibility with Snowflake updates.  
* If a template becomes outdated, update the content and notify the Growth team for publishing.

## 5\. Template Submission Process

See [Templates Brainstorming Guide](https://docs.google.com/document/d/1Ssw7N5qngCu_sj2KUSrTA0VD57RpEzgSiSOLWMka1vQ/edit?tab=t.0) to get started

*Day \-14: Template Ideation*

* Product manager works with growth platform to ideate and align on a valuable, concise template topic

*Day 0: Template Submission*

* The product manager submits the initial template content to growth platform.

*Weeks 1-2: Internal Review and Feedback*

* The template undergoes a internal review, gathering feedback from stakeholders, making necessary adjustments, and ensuring that sample data is loaded to S3.

*End of Week 2: Final Sign-Off*

* The revised template is sent back to the product manager for approval.

*Post-Sign-Off: Publication*

* The approved template is scheduled for release through the regular product release cycle.

*Maintenance*

* Content updates are the responsibility of the Feature PM. As features are updated, PMs should work with Growth Platform to update the templates to reflect the latest.

---

