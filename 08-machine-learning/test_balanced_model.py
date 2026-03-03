"""
Quick test with balanced class weights
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load data
df = pd.read_csv('data/customer_churn_data.csv')

# Prepare data
X = df.drop(['customer_id', 'churn'], axis=1)
y = (df['churn'] == 'Yes').astype(int)

# Encode categorical columns
from sklearn.preprocessing import LabelEncoder
for col in X.select_dtypes(include=['object']).columns:
    X[col] = LabelEncoder().fit_transform(X[col])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train with balanced class weights
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\n" + "="*60)
print("RESULTS WITH BALANCED CLASS WEIGHTS")
print("="*60)
print(classification_report(y_test, y_pred, target_names=['No Churn', 'Churn']))

# Check predictions on your test customers
print("\n" + "="*60)
print("PREDICTIONS ON SAMPLE CUSTOMERS")
print("="*60)

# Create test customers
test_customers = [
    {
        'gender': 'Male', 'senior_citizen': 0, 'partner': 'No', 'dependents': 'No',
        'tenure': 2, 'phone_service': 1, 'multiple_lines': 'No',
        'internet_service': 'Fiber optic', 'online_security': 'No',
        'online_backup': 'No', 'device_protection': 'No', 'tech_support': 'No',
        'streaming_tv': 'Yes', 'streaming_movies': 'Yes', 'contract': 'Month-to-month',
        'paperless_billing': 'Yes', 'payment_method': 'Electronic check',
        'monthly_charges': 95.50, 'total_charges': 191.00
    },
    {
        'gender': 'Female', 'senior_citizen': 0, 'partner': 'Yes', 'dependents': 'Yes',
        'tenure': 48, 'phone_service': 1, 'multiple_lines': 'Yes',
        'internet_service': 'DSL', 'online_security': 'Yes',
        'online_backup': 'Yes', 'device_protection': 'Yes', 'tech_support': 'Yes',
        'streaming_tv': 'No', 'streaming_movies': 'No', 'contract': 'Two year',
        'paperless_billing': 'No', 'payment_method': 'Credit card',
        'monthly_charges': 85.75, 'total_charges': 4116.00
    }
]

# Convert to DataFrame
test_df = pd.DataFrame(test_customers)

# Encode using same method
for col in test_df.select_dtypes(include=['object']).columns:
    if col in X.columns:
        test_df[col] = LabelEncoder().fit_transform(test_df[col])

# Predict
preds = model.predict(test_df)
probs = model.predict_proba(test_df)

for i, customer in enumerate(test_customers):
    print(f"\nCustomer {i+1}: {'Month-to-month' if i==0 else 'Two year'} contract")
    print(f"  Prediction: {'⚠️ WILL CHURN' if preds[i] else '✅ WILL STAY'}")
    print(f"  Churn Probability: {probs[i][1]:.1%}")
    print(f"  Stay Probability: {probs[i][0]:.1%}")