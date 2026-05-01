import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load cleaned data
df = pd.read_csv('../data/cleaned.csv')
X  = df.drop('label', axis=1)
y  = df['label']

# 80/20 split, stratify keeps class ratio equal in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows")

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,   # 100 decision trees
    max_depth=None,      # trees grow until pure
    random_state=42,
    n_jobs=-1            # use all CPU cores
)
model.fit(X_train, y_train)
print("Training complete!")

# Evaluate
preds = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, preds):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, preds,
      target_names=['Legitimate', 'Phishing']))
print("Confusion Matrix:")
print(confusion_matrix(y_test, preds))

# Save the trained model
joblib.dump(model, 'phishing_model.pkl')
print("\nModel saved to model/phishing_model.pkl")

import pandas as pd
importances = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)
print("\nTop 10 most important features:")
print(importances.head(10))