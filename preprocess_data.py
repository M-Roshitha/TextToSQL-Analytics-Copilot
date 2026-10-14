
from pathlib import Path
import pandas as pd

FILE_PATH = Path("data/online_retail_II.xlsx")

if not FILE_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {FILE_PATH.resolve()}"
    )

print("Loading Excel sheets...")

sheets = pd.read_excel(
    FILE_PATH,
    sheet_name=None
)

frames = []

for sheet_name, df in sheets.items():
    df["SourceYear"] = sheet_name
    frames.append(df)

data = pd.concat(frames, ignore_index=True)

print("\n========== DATASET OVERVIEW ==========")
print("Total rows:", len(data))
print("Total columns:", len(data.columns))
print("\nColumn names:")
print(data.columns.tolist())

print("\n========== MISSING VALUES ==========")
print(data.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print("Exact duplicate rows:", data.duplicated().sum())

print("\n========== QUANTITY ANALYSIS ==========")
print("Negative quantity rows:", (data["Quantity"] < 0).sum())
print("Zero quantity rows:", (data["Quantity"] == 0).sum())

print("\n========== PRICE ANALYSIS ==========")
print("Negative price rows:", (data["Price"] < 0).sum())
print("Zero price rows:", (data["Price"] == 0).sum())

print("\n========== INVOICE ANALYSIS ==========")
invoice = data["Invoice"].astype("string").str.strip()
cancelled = invoice.str.startswith("C", na=False)

print("Cancellation invoice rows:", cancelled.sum())
print("Unique invoices:", data["Invoice"].nunique())

print("\n========== DATE ANALYSIS ==========")
dates = pd.to_datetime(data["InvoiceDate"], errors="coerce")

print("Invalid dates:", dates.isna().sum())
print("Earliest date:", dates.min())
print("Latest date:", dates.max())

print("\n========== CUSTOMER ANALYSIS ==========")
print("Unique customers:", data["Customer ID"].nunique())
print("Unique countries:", data["Country"].nunique())
print("Unique products:", data["StockCode"].nunique())

print("\n========== SAMPLE DATA ==========")
print(data.head(5).to_string(index=False))

print("\nInspection completed. No source data was modified.")
