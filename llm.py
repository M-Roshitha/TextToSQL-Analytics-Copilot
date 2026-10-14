
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"


def generate_sql(question):
    q = question.lower().strip()

    # --------------------------------------------------
    # 1. PREDEFINED SQL TEMPLATES
    # --------------------------------------------------

    # Highest product price
    if "highest price" in q or "most expensive" in q:
        return """
        SELECT description, stockcode, price
        FROM transactions
        ORDER BY price DESC
        LIMIT 1
        """

    # Lowest product price
    if "lowest price" in q or "cheapest" in q:
        return """
        SELECT description, stockcode, price
        FROM transactions
        ORDER BY price ASC
        LIMIT 1
        """

    # Count distinct orders
    if "how many orders" in q or "count the orders" in q:
        return """
        SELECT COUNT(DISTINCT invoice) AS total_orders
        FROM transactions
        """

    # Average unit price by country
    if (
        "average unit price by country" in q
        or "average price by country" in q
        or "average unit price for each country" in q
    ):
        return """
        SELECT country,
               ROUND(AVG(price), 2) AS average_unit_price
        FROM transactions
        GROUP BY country
        ORDER BY country
        """

    # Overall average unit price
    if (
        "average unit price" in q
        or "average product price" in q
        or "average price" in q
    ):
        return """
        SELECT ROUND(AVG(price), 2) AS average_unit_price
        FROM transactions
        """

    # Total revenue of each product
    if "total revenue of each product" in q:
        return """
        SELECT stockcode, description,
               ROUND(SUM(line_revenue), 2) AS total_revenue
        FROM transactions
        GROUP BY stockcode, description
        ORDER BY total_revenue DESC
        """

    # Top five products by revenue
    if (
        "highest revenue" in q
        or "generated the most revenue" in q
        or "highest revenue products" in q
    ):
        return """
        SELECT stockcode, description,
               ROUND(SUM(line_revenue), 2) AS total_revenue
        FROM transactions
        GROUP BY stockcode, description
        ORDER BY total_revenue DESC
        LIMIT 5
        """

    # Total revenue across all transaction rows
    if "total revenue across all orders" in q:
        return """
        SELECT ROUND(SUM(line_revenue), 2) AS total_revenue
        FROM transactions
        """

    # --------------------------------------------------
    # 2. LOCAL LLM FALLBACK USING OLLAMA
    # --------------------------------------------------

    prompt = f"""
You are a Text-to-SQL assistant for an Online Retail II database.

Convert the user's question into exactly one valid SQLite SELECT query.

Actual database schema:
transactions(
    invoice,
    stockcode,
    description,
    quantity,
    invoicedate,
    price,
    customer_id,
    country,
    source_year,
    is_cancellation,
    is_negative_quantity,
    line_revenue,
    has_zero_price,
    has_negative_price
)

Rules:
- Use only the transactions table and the columns listed above.
- Use AVG(price) for average unit-price questions.
- Use SUM(line_revenue) for revenue calculations.
- Count distinct invoice values when counting orders.
- Do not add WHERE filters unless the user requests filtering.
- Do not automatically exclude cancellations or negative quantities.
- Use SQLite-compatible SQL.
- Return only one SQL query, without Markdown or explanation.
- Generate only a read-only SELECT query.
- Do not invent table names or column names.
- Do not modify the database.

User question: {question}

SQL:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    sql = response.json()["response"].strip()

    if not sql:
        raise ValueError("Ollama returned an empty SQL response.")

    return sql
