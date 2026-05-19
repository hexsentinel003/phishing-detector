import pandas as pd, joblib, sys, os, re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# features.py is in the same model/ directory
from features import extract_features

FEATURE_NAMES = [
    'url_length','dot_count','hyphen_count','at_count','slash_count',
    'query_count','equals_count','percent_count','is_https','is_ip',
    'subdomain_depth','domain_length','path_length','query_length',
    'has_login','has_secure','has_bank','has_account','has_verify',
    'tld_length','underscore_count','tilde_count','hostname_length',
    'digits_in_domain','total_digits','has_paypal','has_update',
    'has_confirm','has_signin','fragment_count'
]

# ── Step 0: Clean garbage URLs ────────────────────────────────
def is_clean_url(url):
    """Filter out URLs with binary/non-ASCII garbage data."""
    try:
        url.encode('ascii')
        return bool(re.match(r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+$', str(url)))
    except Exception:
        return False

# ── Step 1: Load & filter dataset ────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE, '..', 'data', 'phishing_site_urls.csv')

print("Loading URLs...")
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows. Filtering garbage URLs...")

df = df[df['URL'].apply(is_clean_url)].reset_index(drop=True)
print(f"After cleaning: {len(df)} rows remain.")
print(df['Label'].value_counts())

df['label'] = (df['Label'] == 'bad').astype(int)  # bad=1, good=0

# ── Step 2: Extract features ──────────────────────────────────
print(f"\nExtracting features from {len(df)} URLs (this may take a few minutes)...")
rows = []
errors = 0
for i, row in df.iterrows():
    try:
        rows.append(extract_features(row['URL']))
    except Exception:
        rows.append([0] * 30)
        errors += 1
    if i % 50000 == 0:
        print(f"  {i}/{len(df)} processed...")

X = pd.DataFrame(rows, columns=FEATURE_NAMES)
y = df['label']
print(f"Done. Errors skipped: {errors}")

# ── Step 3: Train ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"\nTrain: {len(X_train)} rows | Test: {len(X_test)} rows")

model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',   # handles the 2.5:1 good/bad imbalance
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("Training complete!")

# ── Step 4: Evaluate ──────────────────────────────────────────
preds = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, preds):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, preds, target_names=['Legitimate', 'Phishing']))
print("Confusion Matrix:")
print(confusion_matrix(y_test, preds))

# ── Step 5: Save ──────────────────────────────────────────────
OUT = os.path.join(BASE, 'phishing_model.pkl')
joblib.dump(model, OUT)
print(f"\nModel saved to: {OUT}")

importances = pd.Series(model.feature_importances_, index=FEATURE_NAMES)
print("\nTop 10 most important features:")
print(importances.sort_values(ascending=False).head(10))
