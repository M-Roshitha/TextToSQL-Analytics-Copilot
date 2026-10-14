import re
import requests
import streamlit as st
import pandas as pd

from llm import generate_sql
from database import execute_query


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Text-to-SQL Analytics Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Text-to-SQL Analytics Copilot")
st.caption("Ask questions about your sales data using natural language.")

st.info(
    "Powered by your local Qwen model through Ollama. "
    "No paid API required."
)


# ---------------- QUESTION INPUT ----------------

question = st.text_input(
    "Ask a question about your sales data",
    placeholder="e.g., Which product has the highest price?"
)

generate_button = st.button("Generate Answer", type="primary")


# ---------------- SQL CLEANING ----------------

def clean_sql(sql):
    """Remove Markdown code fences and surrounding whitespace."""

    sql = re.sub(
        r"```(?:sql)?",
        "",
        sql,
        flags=re.IGNORECASE
    )

    return sql.strip().rstrip(";").strip()


# ---------------- SQL VALIDATION ----------------

def validate_sql(sql):
    """Perform basic validation before read-only database execution."""

    if not sql:
        raise ValueError("The generated SQL is empty.")

    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    # Allow one optional trailing semicolon, but no multiple statements.
    if ";" in sql:
        raise ValueError("Only one SQL statement is allowed.")

    return sql


# ---------------- PROCESS QUESTION ----------------

if generate_button:

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            # Generate SQL using templates or the local Ollama model.
            with st.spinner("Generating SQL..."):
                sql = generate_sql(question)

            # Clean and validate the generated SQL.
            sql = clean_sql(sql)
            validate_sql(sql)

            # Display the generated SQL.
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # Execute the query using the read-only database layer.
            with st.spinner("Executing query..."):
                results = execute_query(sql)

            # Display query results.
            st.subheader("Query Results")

            if results:
                df = pd.DataFrame(results)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                st.success(
                    f"Successfully retrieved {len(df)} row(s)."
                )

                # Show a chart when the result has suitable numeric data.
                numeric_columns = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                if len(df) > 1 and numeric_columns:
                    with st.expander("View data visualization"):
                        if len(numeric_columns) == 1:
                            chart_df = df.set_index(df.columns[0])[
                                numeric_columns
                            ]
                            st.bar_chart(chart_df)
                        else:
                            st.bar_chart(df[numeric_columns])

            else:
                st.info("The query returned no results.")

        except requests.exceptions.RequestException as error:
            st.error(
                "Unable to contact Ollama. Check that Ollama is running "
                f"and the model is available. Details: {error}"
            )

        except Exception as error:
            st.error(f"Unable to process the question: {error}")


# ---------------- EXAMPLE QUESTIONS ----------------

st.divider()

with st.expander("Try example questions"):
    st.markdown("""
    **Basic**
    - How many orders are in the database?
    - Which product has the highest price?
    - What is the average product price?

    **Revenue analysis**
    - Which five products generated the highest revenue?
    - What is the total revenue of each product?
    - What is the total revenue across all orders?

    **Filtering and sorting**
    - Which products have a quantity greater than 5 in any order?
    - Show all orders sorted by price from highest to lowest.
    - Which products have a price greater than 10000?
    """)

st.caption(
    "Text-to-SQL Analytics Copilot | Local LLM + SQLite + Streamlit"
)
