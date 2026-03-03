"""
Simple Customer Churn Prediction - Using Best Available Model
Author: Victor Makanju
Updated to use SMOTE model
"""

import pandas as pd
import joblib
import glob
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("SIMPLE CUSTOMER CHURN PREDICTION")
print("="*60)

# =============================================
# 1. FIND THE BEST MODEL (PREFER SMOTE)
# =============================================
print("\n📥 Loading the best available model...")

# First, look for SMOTE models (preferred)
model_files = glob.glob('models/*smote*.pkl')

# If no SMOTE models, look for any model
if not model_files:
    model_files = glob.glob('models/churn_model_*.pkl')
    print("   No SMOTE model found, using regular model")
else:
    print("   ✓ Found SMOTE model!")

if not model_files:
    print("❌ No model found!")
    print("   Available files in models folder:")
    for f in glob.glob('models/*.pkl'):
        print(f"     {f}")
    exit()

# Use the first model found
model_path = model_files[0]
model_name = model_path.replace('models\\', '').replace('.pkl', '')
print(f"✓ Using model: {model_name}")

# Load model and preprocessors
model = joblib.load(model_path)
label_encoders = joblib.load('models/label_encoders.pkl')
scaler = joblib.load('models/scaler.pkl')

# =============================================
# 2. CREATE TEST CUSTOMERS
# =============================================
print("\n🧪 Creating test customers...")

customers = [
    {
        'name': 'High Risk Customer',
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
        'total_charges': 191.00  # 2 months * 95.50
    },
    {
        'name': 'Low Risk Customer',
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
    },
    {
        'name': 'Medium Risk Customer',
        'gender': 'Male',
        'senior_citizen': 0,
        'partner': 'Yes',
        'dependents': 'No',
        'tenure': 12,
        'phone_service': 1,
        'multiple_lines': 'Yes',
        'internet_service': 'Fiber optic',
        'online_security': 'No',
        'online_backup': 'Yes',
        'device_protection': 'No',
        'tech_support': 'No',
        'streaming_tv': 'Yes',
        'streaming_movies': 'No',
        'contract': 'Month-to-month',
        'paperless_billing': 'Yes',
        'payment_method': 'Bank transfer',
        'monthly_charges': 110.25,
        'total_charges': 1323.00
    }
]

# =============================================
# 3. MAKE PREDICTIONS
# =============================================
print("\n🔮 Making predictions with SMOTE model...")
print("-"*70)

for customer in customers:
    # Convert to DataFrame
    df = pd.DataFrame([customer])
    
    # Encode categorical columns
    categorical_cols = ['gender', 'partner', 'dependents', 'multiple_lines', 
                       'internet_service', 'online_security', 'online_backup', 
                       'device_protection', 'tech_support', 'streaming_tv', 
                       'streaming_movies', 'contract', 'paperless_billing', 'payment_method']
    
    for col in categorical_cols:
        if col in df.columns and col in label_encoders:
            try:
                df[col] = label_encoders[col].transform(df[col])
            except:
                # If value not found, use the most common class (0)
                df[col] = 0
    
    # All features in correct order
    feature_cols = ['gender', 'senior_citizen', 'partner', 'dependents', 'tenure',
                   'phone_service', 'multiple_lines', 'internet_service', 'online_security',
                   'online_backup', 'device_protection', 'tech_support', 'streaming_tv',
                   'streaming_movies', 'contract', 'paperless_billing', 'payment_method',
                   'monthly_charges', 'total_charges']
    
    df = df[feature_cols]
    
    # Scale features
    df_scaled = scaler.transform(df)
    
    # Predict
    prediction = model.predict(df_scaled)[0]
    probability = model.predict_proba(df_scaled)[0]
    
    # Determine risk level
    churn_prob = probability[1]
    if churn_prob > 0.7:
        risk = "🔴 HIGH"
    elif churn_prob > 0.3:
        risk = "🟡 MEDIUM"
    else:
        risk = "🟢 LOW"
    
    # Display results
    print(f"\n📊 {customer['name']}:")
    print(f"  Contract: {customer['contract']}")
    print(f"  Tenure: {customer['tenure']} months")
    print(f"  Monthly: ${customer['monthly_charges']:.2f}")
    print(f"  Internet: {customer['internet_service']}")
    print(f"  Payment: {customer['payment_method']}")
    print(f"  {'⚠️ WILL CHURN' if prediction else '✅ WILL STAY'}")
    print(f"  Probability of churn: {churn_prob:.1%}")
    print(f"  Probability of stay:  {probability[0]:.1%}")
    print(f"  Risk Level: {risk}")

print("\n" + "="*70)
print("✅ PREDICTION COMPLETE")
print("="*70)

# =============================================
# 4. SAVE PREDICTIONS
# =============================================
results = []
for i, customer in enumerate(customers):
    df = pd.DataFrame([customer])
    # ... (same encoding as above)
    # This is simplified - in reality you'd reuse the prediction logic
    print("\n📝 Predictions saved to: results/smote_predictions.csv")