import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.cluster import KMeans
import joblib

# =========================
# LOAD ONLY SYNTHETIC DATA
# =========================
df = pd.read_csv("data/synthetic/business_master_dataset.csv")
print("Synthetic dataset shape:", df.shape)

# =========================
# FEATURE SELECTION
# =========================
numeric_cols = [
    "investment_required_lakhs",
    "monthly_revenue_lakhs",
    "monthly_expense_lakhs",
    "market_demand",
    "competition_level",
    "risk_score",
    "opportunity_score",
    "growth_rate_percent"
]

categorical_cols = ["business_sector", "city"]

# =========================
# CLEAN DATA
# =========================
df = df.dropna(subset=["monthly_profit_lakhs", "business_success_probability"])
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Encode categorical columns
encoder = LabelEncoder()
for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col].astype(str))

# =========================
# MODEL 1 — PROFIT REGRESSION
# =========================
X = df[numeric_cols + categorical_cols]
y_profit = df["monthly_profit_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_profit, test_size=0.2, random_state=42
)

profit_model = RandomForestRegressor(
    n_estimators=50,
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)

profit_model.fit(X_train, y_train)
joblib.dump(profit_model, "backend/ml_models/model_profit.pkl")

print("✅ Profit model saved")

# =========================
# MODEL 2 — SUCCESS CLASSIFICATION
# =========================
y_success = (df["business_success_probability"] > 0.5).astype(int)

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X, y_success, test_size=0.2, random_state=42
)

success_model = RandomForestClassifier(
    n_estimators=50,
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42
)

success_model.fit(X_train2, y_train2)
joblib.dump(success_model, "backend/ml_models/model_success.pkl")

print("✅ Success model saved")

# =========================
# MODEL 3 — RECOMMENDATION (CLUSTERING)
# =========================
recommend_cols = [
    "investment_required_lakhs",
    "monthly_profit_lakhs",
    "market_demand",
    "competition_level",
    "risk_score"
]

X_rec = df[recommend_cols]

kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(X_rec)

joblib.dump(kmeans, "backend/ml_models/model_recommend.pkl")

print("✅ Recommendation model saved")
