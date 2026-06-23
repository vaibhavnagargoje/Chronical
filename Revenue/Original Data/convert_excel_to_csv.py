import pandas as pd
import os

def convert_excel_to_csv():
    excel_file = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Revenue\Original Data\revenue_data.xlsx"
    output_dir = r"c:\Users\vaibh\Desktop\CKA Projects\Chronical\Revenue"

    try:
        # Load the spreadsheet
        xls = pd.ExcelFile(excel_file)
        
        # Iterate over all the sheets
        for sheet_name in xls.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            # Read the sheet data
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Format the output CSV filename
            safe_sheet_name = str(sheet_name).replace(" ", "_").replace("/", "_").replace("\\", "_")
            output_csv_path = os.path.join(output_dir, f"{safe_sheet_name}.csv")
            
            # Save as CSV
            df.to_csv(output_csv_path, index=False)
            print(f"Saved: {output_csv_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_excel_to_csv()
