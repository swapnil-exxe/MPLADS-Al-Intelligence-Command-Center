import pandas as pd
import numpy as np

filepath = "backend/data/Allocated_Limit_for_Honble_MPs.csv"

df_raw = pd.read_csv(filepath)
print("--- RAW DATA SUMMARY ---")
print("Raw Shape:", df_raw.shape)
print("Columns:", list(df_raw.columns))

# Separate Grand Total row
grand_total_row = df_raw[df_raw['Sr. No.'].astype(str).str.contains('Grand Total', case=False, na=False)]
df = df_raw[~df_raw['Sr. No.'].astype(str).str.contains('Grand Total', case=False, na=False)].copy()

print("Data Rows Count (excluding Grand Total):", len(df))

# Clean amount column
df['Allocated_Amount_Clean'] = df['Allocated AMOUNT ( ₹ )'].astype(str).str.replace(',', '').str.strip()
df['Allocated_Amount_Numeric'] = pd.to_numeric(df['Allocated_Amount_Clean'], errors='coerce')

missing_amt = df['Allocated_Amount_Numeric'].isna().sum()
print("Missing / Invalid Allocated Amount rows:", missing_amt)
print("Rows with missing amount:")
print(df[df['Allocated_Amount_Numeric'].isna()])

# Distribution of Allocated Amount
print("\n--- ALLOCATION STATS (₹) ---")
print("Total Sum (calculated):", df['Allocated_Amount_Numeric'].sum())
print("Mean:", df['Allocated_Amount_Numeric'].mean())
print("Median:", df['Allocated_Amount_Numeric'].median())
print("Min:", df['Allocated_Amount_Numeric'].min())
print("Max:", df['Allocated_Amount_Numeric'].max())
print("Standard Deviation:", df['Allocated_Amount_Numeric'].std())
print("Value Counts of Allocation:")
print(df['Allocated_Amount_Numeric'].value_counts().head(10))

# States
print("\n--- STATE STATS ---")
print("Unique States Count:", df['State'].nunique())
state_counts = df.groupby('State')['Allocated_Amount_Numeric'].agg(['count', 'sum', 'mean', 'min', 'max']).sort_values('count', ascending=False)
print(state_counts)

# Duplicate check
print("\n--- DUPLICATE CHECKS ---")
print("Duplicate MP names:", df[df.duplicated('Hon\'ble Members of Parliaments', keep=False)][['Sr. No.', 'State', 'Hon\'ble Members of Parliaments', 'Constituency', 'Allocated AMOUNT ( ₹ )']])
print("Duplicate Constituencies:", df[df.duplicated('Constituency', keep=False)][['Sr. No.', 'State', 'Hon\'ble Members of Parliaments', 'Constituency', 'Allocated AMOUNT ( ₹ )']])
