import pandas as pd, joblib, sys, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

sys.path.append(os.path.dirname(__file__))
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

# ── Step 1: Build feature matrix from URLs ────────────────────
print("Loading URLs...")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'phishing_site_urls.csv'))
df['label'] = (df['Label'] == 'bad').astype(int)  # bad=1, good=0

print(f"Extracting features from {len(df)} URLs (this may take a few minutes)...")
rows = []
errors = 0
for i, row in df.iterrows():
    try:
        rows.append(extract_features(row['URL']))
    except:
        rows.append([0] * 30)
        errors += 1
    if i % 50000 == 0:
        print(f"  {i}/{len(df)} processed...")

X = pd.DataFrame(rows, columns=FEATURE_NAMES)
y = df['label']
print(f"Done. Errors skipped: {errors}")

# ── Step 2: Train ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"\nTrain: {len(X_train)} rows | Test: {len(X_test)} rows")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("Training complete!")

# ── Step 3: Evaluate ──────────────────────────────────────────
preds = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, preds):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, preds, target_names=['Legitimate', 'Phishing']))
print("Confusion Matrix:")
print(confusion_matrix(y_test, preds))

# ── Step 4: Save ──────────────────────────────────────────────
joblib.dump(model, os.path.join(os.path.dirname(__file__), 'phishing_model.pkl'))
print("\nModel saved to model/phishing_model.pkl")

importances = pd.Series(model.feature_importances_, index=FEATURE_NAMES)
print("\nTop 10 most important features:")
print(importances.sort_values(ascending=False).head(10))
