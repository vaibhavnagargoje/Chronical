"""
Script to:
1. Explore all sheets in Demography.xlsx
2. Print each sheet name, shape, and columns
3. Export each sheet as a CSV file
"""
import os
import re
import pandas as pd

EXCEL_PATH = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Demography\Original Data\Demography.xlsx"
CSV_OUT_DIR = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Demography"

os.makedirs(CSV_OUT_DIR, exist_ok=True)

xl = pd.ExcelFile(EXCEL_PATH)
print(f"Total sheets: {len(xl.sheet_names)}")
print("=" * 60)

for sheet in xl.sheet_names:
    df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
    # Print info
    print(f"\nSheet: '{sheet}'  |  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    
    # Save as CSV
    safe_name = re.sub(r'[^\w\s-]', '', sheet).strip().replace(' ', '_')
    csv_path = os.path.join(CSV_OUT_DIR, f"{safe_name}.csv")
    df.to_csv(csv_path, index=False)
    print(f"  -> Saved: {csv_path}")

print("\nDone!")
