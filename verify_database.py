
import sqlite3

DB_PATH = "online_retail.db"

with sqlite3.connect(DB_PATH) as connection:
    connection.row_factory = sqlite3.Row

    print("DATABASE TABLES")
    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    for table in tables:
        print("-", table["name"])

    print("\nTRANSACTION COUNT")
    print(connection.execute("""
        SELECT COUNT(*) FROM transactions
    """).fetchone()[0])

    print("\nSAMPLE TRANSACTIONS")
    rows = connection.execute("""
        SELECT invoice, description, quantity, price,
               line_revenue, country
        FROM transactions
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(dict(row))

    print("\nTOP 10 PRODUCTS BY SIGNED LINE REVENUE")
    rows = connection.execute("""
        SELECT
            stockcode,
            description,
            ROUND(SUM(line_revenue), 2) AS total_revenue
        FROM transactions
        GROUP BY stockcode, description
        ORDER BY total_revenue DESC
        LIMIT 10
    """).fetchall()

    for row in rows:
        print(dict(row))
