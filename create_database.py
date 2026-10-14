
import sqlite3

# Create a local database file
connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

# Create the orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

# Insert sample sales records
sales_data = [
    (1, "Laptop", 2, 50000),
    (2, "Phone", 5, 20000),
    (3, "Headphones", 10, 1500),
    (4, "Laptop", 1, 50000),
    (5, "Phone", 3, 20000),
    (6, "Keyboard", 8, 1200),
    (7, "Monitor", 4, 12000),
    (8, "Headphones", 5, 1500),
    (9, "Monitor", 2, 12000),
    (10, "Keyboard", 4, 1200)
]

cursor.executemany("""
INSERT OR IGNORE INTO orders
(order_id, product_name, quantity, price)
VALUES (?, ?, ?, ?)
""", sales_data)

connection.commit()

# Display all records
cursor.execute("SELECT * FROM orders")

for row in cursor.fetchall():
    print(row)

connection.close()

print("\nDatabase created successfully!")
