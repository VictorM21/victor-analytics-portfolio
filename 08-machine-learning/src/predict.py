"""
Customer Churn Prediction - Make Predictions on New Customers
Author: Victor Makanju
Purpose: Load trained model and predict churn for new customers
"""

import pandas as pd
import numpy as np
import joblib
import glob
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("CUSTOMER CHURN PREDICTION")
print("="*60)

# =============================================
# 1. LOAD MODEL AND PREPROCESSORS
# =============================================
print("\n📥 Loading model and preprocessors...")

# Find the model file
model_files = glob.glob('models/churn_model_*.pkl')

# Prefer Random Forest model if available
rf_files = glob.glob('models/churn_model_Random_*.pkl')
if rf_files:
    model_files = rf_files
    print("✓ Using Random Forest model (best performer)")

if not model_files:
    print("❌ No model found in 'models/' folder.")
    print("   Please run train_model.py first.")
    exit()

model_path = model_files[0]
model = joblib.load(model_path)
label_encoders = joblib.load('models/label_encoders.pkl')
scaler = joblib.load('models/scaler.pkl')

print(f"✓ Loaded model: {model_path}")
print("✓ Loaded label encoders")
print("✓ Loaded scaler")

# =============================================
# 2. DEFINE ALL FEATURE COLUMNS (SAME AS TRAINING)
# =============================================
print("\n🔧 Defining feature columns...")

# These must match EXACTLY what was used in training
all_feature_columns = [
    'gender', 'senior_citizen', 'partner', 'dependents', 'tenure',
    'phone_service', 'multiple_lines', 'internet_service', 'online_security',
    'online_backup', 'device_protection', 'tech_support', 'streaming_tv',
    'streaming_movies', 'contract', 'paperless_billing', 'payment_method',
    'monthly_charges', 'total_charges'
]

print(f"✓ Using {len(all_feature_columns)} features")

# =============================================
# 3. CREATE TEST CUSTOMERS
# =============================================
print("\n🧪 Creating test customers...")

# Create test customers with ALL features
test_customers = [
    {
        'customer_id': 'CUST-HIGH-001',
        'gender': 'Male',
        'senior_citizen': 0,
        'partner': 'No',
        'dependents': 'No',
        'tenure': 2,
        'phone_service': 1,
        'multiple_lines': 'No',
        'internet_service': 'Fiber optic',
        'online_security': 'No',
        'online_backup': 'No',
        'device_protection': 'No',
        'tech_support': 'No',
        'streaming_tv': 'Yes',
        'streaming_movies': 'Yes',
        'contract': 'Month-to-month',
        'paperless_billing': 'Yes',
        'payment_method': 'Electronic check',
        'monthly_charges': 95.50,
        'total_charges': 191.00
    },
    {
        'customer_id': 'CUST-LOW-002',
        'gender': 'Female',
        'senior_citizen': 0,
        'partner': 'Yes',
        'dependents': 'Yes',
        'tenure': 48,
        'phone_service': 1,
        'multiple_lines': 'Yes',
        'internet_service': 'DSL',
        'online_security': 'Yes',
        'online_backup': 'Yes',
        'device_protection': 'Yes',
        'tech_support': 'Yes',
        'streaming_tv': 'No',
        'streaming_movies': 'No',
        'contract': 'Two year',
        'paperless_billing': 'No',
        'payment_method': 'Credit card',
        'monthly_charges': 85.75,
        'total_charges': 4116.00
    }
]

# Convert to DataFrame
df_test = pd.DataFrame(test_customers)
print(f"✓ Created {len(df_test)} test customers")

# =============================================
# 4. PREPROCESS TEST DATA
# =============================================
print("\n🔄 Preprocessing test data...")

# Make a copy for processing
df_processed = df_test.copy()

# Encode ALL categorical columns
categorical_cols = ['gender', 'partner', 'dependents', 'multiple_lines', 
                   'internet_service', 'online_security', 'online_backup', 
                   'device_protection', 'tech_support', 'streaming_tv', 
                   'streaming_movies', 'contract', 'paperless_billing', 'payment_method']

print("\n📝 Encoding categorical features:")
for col in categorical_cols:
    if col in df_processed.columns and col in label_encoders:
        try:
            df_processed[col] = label_encoders[col].transform(df_processed[col])
            print(f"  ✓ {col}: {df_test[col].iloc[0]} → {df_processed[col].iloc[0]}")
        except Exception as e:
            print(f"  ⚠️ Warning encoding {col}: using default")
            # Use first class as default
            df_processed[col] = 0

# phone_service is already numeric (0/1), no encoding needed
print(f"  ✓ phone_service (already numeric)")

# =============================================
# 5. ENSURE CORRECT COLUMN ORDER
# =============================================
print("\n📊 Ensuring correct feature order...")

# Make sure all columns are in the same order as training
df_processed = df_processed[all_feature_columns]

# Scale ALL features (the scaler was trained on all features)
df_scaled = pd.DataFrame(
    scaler.transform(df_processed),
    columns=all_feature_columns,
    index=df_processed.index
)

print("✓ Scaled all features")

# =============================================
# 6. MAKE PREDICTIONS
# =============================================
print("\n🔮 Making predictions...")

# Predict
predictions = model.predict(df_scaled)
probabilities = model.predict_proba(df_scaled)

# =============================================
# 7. DISPLAY RESULTS
# =============================================
print("\n" + "="*60)
print("📊 PREDICTION RESULTS")
print("="*60)

results = []
for i, customer in enumerate(test_customers):
    churn_prob = probabilities[i][1]
    
    # Determine risk level
    if churn_prob > 0.7:
        risk = '🔴 HIGH'
    elif churn_prob > 0.3:
        risk = '🟡 MEDIUM'
    else:
        risk = '🟢 LOW'
    
    # Prediction emoji
    pred_emoji = '⚠️ WILL CHURN' if predictions[i] else '✅ WILL STAY'
    
    print(f"\n{'-'*40}")
    print(f"Customer: {customer['customer_id']}")
    print(f"{'-'*40}")
    print(f"  Contract: {customer['contract']}")
    print(f"  Tenure: {customer['tenure']} months")
    print(f"  Monthly Charges: ${customer['monthly_charges']}")
    print(f"  Internet: {customer['internet_service']}")
    print(f"  Payment: {customer['payment_method']}")
    print(f"{'-'*40}")
    print(f"  Prediction: {pred_emoji}")
    print(f"  Probability: {churn_prob:.1%}")
    print(f"  Risk Level: {risk}")
    
    results.append({
        'customer_id': customer['customer_id'],
        'contract': customer['contract'],
        'tenure': customer['tenure'],
        'monthly_charges': customer['monthly_charges'],
        'internet_service': customer['internet_service'],
        'payment_method': customer['payment_method'],
        'prediction': 'Churn' if predictions[i] else 'Stay',
        'probability': f"{churn_prob:.1%}",
        'risk_level': risk.replace('🔴 ', '').replace('🟡 ', '').replace('🟢 ', '')
    })

# =============================================
# 8. SAVE RESULTS
# =============================================
results_df = pd.DataFrame(results)
results_df.to_csv('results/predictions.csv', index=False)
print(f"\n✅ Results saved to: results/predictions.csv")

print("\n" + "="*60)
print("✅ PREDICTION COMPLETE")
print("="*60)

# Show summary
print("\n📈 Summary:")
churn_count = sum(predictions)
print(f"  Total customers: {len(predictions)}")
print(f"  Predicted to churn: {churn_count}")
print(f"  Predicted to stay: {len(predictions) - churn_count}")
print("="*60)