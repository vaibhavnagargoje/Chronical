import os
import pandas as pd

def main():
    base_dir = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Environment"
    original_data_dir = os.path.join(base_dir, "Original Data")
    excel_file = os.path.join(original_data_dir, "Environment.xlsx")

    print(f"Reading {excel_file}...")
    try:
        # sheet_name=None reads all sheets into a dictionary
        sheets = pd.read_excel(excel_file, sheet_name=None)
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return

    for sheet_name, df in sheets.items():
        # Keep same names with lowercase and _ for space
        clean_name = sheet_name.lower().replace(' ', '_')
        output_filename = f"{clean_name}.xlsx"
        output_path = os.path.join(base_dir, output_filename)
        
        print(f"Saving sheet '{sheet_name}' as {output_filename}...")
        df.to_excel(output_path, index=False)
        
    print("All sheets have been extracted successfully!")

if __name__ == "__main__":
    main()
