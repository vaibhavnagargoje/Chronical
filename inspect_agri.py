import csv, os, glob

folder = 'Agriculture/cleaned_csv'
for f in sorted(glob.glob(os.path.join(folder, '*.csv'))):
    name = os.path.basename(f)
    with open(f, encoding='utf-8') as fh:
        r = csv.reader(fh)
        headers = next(r)
        row1 = next(r, None)
        lines = sum(1 for _ in fh) + 1  # +1 for row1
    print(f"\n=== {name} ({lines} rows) ===")
    print(f"  Headers: {headers}")
    if row1:
        print(f"  Sample:  {row1}")
