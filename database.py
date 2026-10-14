
import sqlite3

DB_PATH = "online_retail.db"


def execute_query(sql):
    """
    Execute a read-only SQL query against the retail database.
    SQLite's authorizer restricts operations to reading data.
    """

    connection = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )
    connection.row_factory = sqlite3.Row

    allowed_actions = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
        sqlite3.SQLITE_RECURSIVE,
    }

    def authorize(action, arg1, arg2, database_name, trigger_name):
        if action in allowed_actions:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    try:
        connection.set_authorizer(authorize)

        cursor = connection.execute(sql)

        # Limit displayed output to prevent enormous result sets.
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchmany(500)

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        connection.close()


if __name__ == "__main__":
    query = """
        SELECT country, ROUND(SUM(line_revenue), 2) AS revenue
        FROM transactions
        GROUP BY country
        ORDER BY revenue DESC
        LIMIT 10
    """

    for result in execute_query(query):
        print(result)
