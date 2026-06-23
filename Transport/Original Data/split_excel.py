import pandas as pd
import os

file_path = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Transport\Original Data\transport_data.xlsx"
out_dir = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Transport\Original Data"

print("Loading excel file...")
try:
    sheets_dict = pd.read_excel(file_path, sheet_name=None)
    for sheet_name, df in sheets_dict.items():
        print(f"Exporting '{sheet_name}' to CSV...")
        safe_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in " _-")
        out_path = os.path.join(out_dir, f"{safe_sheet_name}.csv")
        df.to_csv(out_path, index=False)
    print("Successfully exported all sheets.")
except Exception as e:
    print(f"Error: {e}")
