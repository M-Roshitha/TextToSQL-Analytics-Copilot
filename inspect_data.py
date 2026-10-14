
from pathlib import Path
import pandas as pd

file_path = Path("data/online_retail_II.xlsx")

if not file_path.exists():
    print("Excel file not found:", file_path.resolve())
else:
    excel = pd.ExcelFile(file_path)

    print("Available sheets:", excel.sheet_names)

    for sheet in excel.sheet_names:
        print(f"\n--- Sheet: {sheet} ---")

        df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)

        print("Columns:", df.columns.tolist())
        print(df.to_string(index=False))
