import pandas as pd
import os

env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Original Data")
f = os.path.join(env_dir, "Environment.xlsx")

# Read just the evapotranspiration monthly sheet with no header to see raw structure
df = pd.read_excel(f, sheet_name='Evapotranspiration Monthly', header=None, nrows=5)
print("=== Evapotranspiration Monthly from Original ===")
print(df.to_string())
