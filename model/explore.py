import pandas as pd
import os

# Build path relative to this script's location
BASE = r"C:\Users\Cypher\3D Objects\projects\Phishing"
PATH = r"C:\Users\Cypher\3D Objects\projects\Phishing\data\dataset.csv"

# ── Load ─────────────────────────────────────────
df = pd.read_csv(PATH)

# ── Basic info ───────────────────────────────────
print("=== DATASET LOADED ===")
print(f"Rows     : {df.shape[0]}")
print(f"Columns  : {df.shape[1]}")
print(f"File size: {os.path.getsize(PATH) / 1024:.1f} KB")

# ── Column names ─────────────────────────────────
print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

# ── First 5 rows ─────────────────────────────────
print("\n=== FIRST 5 ROWS ===")
print(df.head())

# ── Class balance ────────────────────────────────
label_col = 'Result'
print(f"\n=== CLASS BALANCE ('{label_col}') ===")
print(df[label_col].value_counts())

# ── Missing values ───────────────────────────────
print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "None found ✓")

# ── Data types ───────────────────────────────────
print("\n=== DATA TYPES ===")
print(df.dtypes)