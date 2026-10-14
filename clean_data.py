
from pathlib import Path
import sqlite3
import pandas as pd

# ---------- FILE PATHS ----------
INPUT_FILE = Path("data/online_retail_II.xlsx")
OUTPUT_DB = Path("online_retail.db")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE.resolve()}"
    )

print("Loading Online Retail II dataset...")

# ---------- LOAD BOTH SHEETS ----------
sheets = pd.read_excel(INPUT_FILE, sheet_name=None)

frames = []
for sheet_name, df in sheets.items():
    df["source_year"] = sheet_name
    frames.append(df)

raw = pd.concat(frames, ignore_index=True)

print("Original rows:", len(raw))

# ---------- STANDARDIZE COLUMN NAMES ----------
raw.columns = [
    col.strip().lower().replace(" ", "_")
    for col in raw.columns
]

# Keep an unchanged copy of the loaded records for reference.
data = raw.copy()

# ---------- FIX DATA TYPES ----------
data["invoice"] = data["invoice"].astype("string").str.strip()
data["stockcode"] = data["stockcode"].astype("string").str.strip()
data["description"] = data["description"].astype("string").str.strip()
data["country"] = data["country"].astype("string").str.strip()

data["invoicedate"] = pd.to_datetime(
    data["invoicedate"], errors="coerce"
)

data["quantity"] = pd.to_numeric(
    data["quantity"], errors="coerce"
)

data["price"] = pd.to_numeric(
    data["price"], errors="coerce"
)

data["customer_id"] = pd.to_numeric(
    data["customer_id"], errors="coerce"
).astype("Int64")

# ---------- HANDLE MISSING DESCRIPTIONS ----------
# Use the most common known description for the same stock code.
description_lookup = (
    data.dropna(subset=["description"])
    .groupby("stockcode")["description"]
    .agg(lambda values: values.mode().iloc[0])
)

missing_description = data["description"].isna() | (
    data["description"] == ""
)

data.loc[missing_description, "description"] = (
    data.loc[missing_description, "stockcode"]
    .map(description_lookup)
)

data["description"] = data["description"].fillna(
    "Unknown product description"
)

# ---------- ADD ANALYTICS FIELDS ----------
# Cancellation invoices commonly have an invoice number starting with C.
data["is_cancellation"] = (
    data["invoice"].str.upper().str.startswith("C", na=False)
)

# A negative quantity can represent a return or credit adjustment.
data["is_negative_quantity"] = data["quantity"] < 0

# Revenue follows the sign of quantity, preserving negative adjustments.
data["line_revenue"] = data["quantity"] * data["price"]

# Flag unusual values instead of silently deleting them.
data["has_zero_price"] = data["price"] == 0
data["has_negative_price"] = data["price"] < 0

# ---------- DEDUPLICATION ----------
# Preserve all original rows in raw_transactions.
# In transactions, remove only exact duplicates across the original
# source columns. Do not deduplicate using invoice/product alone.
source_columns = [
    "invoice",
    "stockcode",
    "description",
    "quantity",
    "invoicedate",
    "price",
    "customer_id",
    "country",
    "source_year",
]

before = len(data)
data = data.drop_duplicates(
    subset=source_columns,
    keep="first"
).copy()

print("Exact duplicate rows removed from transactions:", before - len(data))
print("Rows retained for analysis:", len(data))

# ---------- SAVE TO A NEW SQLITE DATABASE ----------
if OUTPUT_DB.exists():
    OUTPUT_DB.unlink()

with sqlite3.connect(OUTPUT_DB) as connection:
    raw.to_sql(
        "raw_transactions",
        connection,
        if_exists="replace",
        index=False,
        chunksize=10000
    )

    data.to_sql(
        "transactions",
        connection,
        if_exists="replace",
        index=False,
        chunksize=10000
    )

    connection.execute("""
        CREATE INDEX idx_transactions_invoice
        ON transactions(invoice)
    """)

    connection.execute("""
        CREATE INDEX idx_transactions_customer
        ON transactions(customer_id)
    """)

    connection.execute("""
        CREATE INDEX idx_transactions_stockcode
        ON transactions(stockcode)
    """)

    connection.execute("""
        CREATE INDEX idx_transactions_date
        ON transactions(invoicedate)
    """)

    connection.commit()

# ---------- VERIFY DATABASE ----------
with sqlite3.connect(OUTPUT_DB) as connection:
    for table in ["raw_transactions", "transactions"]:
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count:,} rows")

print("\nDatabase created:", OUTPUT_DB.resolve())
print("Cleaning and database import completed.")
