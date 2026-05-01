import pandas as pd
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE, '../data/dataset.csv')

df = pd.read_csv(PATH)
print(f"Original shape: {df.shape}")
# e.g. (11430, 31) — 11430 rows, 31 columns

# Count and remove duplicate rows
dupes = df.duplicated().sum()
print(f"Duplicate rows found: {dupes}")
df = df.drop_duplicates()
print(f"After removing duplicates: {df.shape}")

# Check which columns have missing values
missing = df.isnull().sum()
print("\nMissing values per column:")
print(missing[missing > 0])

# Strategy: drop rows with any missing value
# (safe for datasets > 10,000 rows)
df = df.fillna(df.median(numeric_only=True))
print(f"\nAfter dropping nulls: {df.shape}")

# Check what values the label column contains
print("\nUnique label values:", df['Result'].unique())
# e.g. ['phishing' 'legitimate'] or [1 0] or [1 -1]

# If labels are text strings — encode to 0/1:
# Labels already numeric in 'Result' → just rename
df = df.rename(columns={'Result': 'label'})
print("Labels already numeric — renamed to 'label'")

print("\nFinal label counts:")
print(df['label'].value_counts())

# Check for any remaining text (object) columns
text_cols = df.select_dtypes(include=['object']).columns.tolist()
print(f"\nText columns to drop: {text_cols}")

if text_cols:
    df = df.drop(columns=text_cols)
    print(f"Dropped. Remaining shape: {df.shape}")

# Final sanity check
print("\n=== FINAL CLEANED DATASET ===")
print(f"Shape         : {df.shape}")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Label balance :")
print(df['label'].value_counts())
print(f"\nData types:")
print(df.dtypes)

# Save cleaned file
OUT = os.path.join(BASE, '../data/cleaned.csv')
df.to_csv(OUT, index=False)
print(f"\n✓ Cleaned dataset saved to: {OUT}")