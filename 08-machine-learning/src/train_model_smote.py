"""
Customer Churn Prediction - WITH SMOTE (Synthetic Minority Oversampling)
Author: Victor Makanju
Purpose: Fix class imbalance by creating synthetic churner examples
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

# Try to import SMOTE
try:
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline
    SMOTE_AVAILABLE = True
    print("✅ SMOTE successfully imported!")
except ImportError:
    SMOTE_AVAILABLE = False
    print("❌ SMOTE not installed. Run: pip install imbalanced-learn")
    exit()

print("="*60)
print("CUSTOMER CHURN PREDICTION - WITH SMOTE")
print("="*60)

# =============================================
# 1. LOAD DATA
# =============================================
print("\n📥 Loading data...")
df = pd.read_csv('data/customer_churn_data.csv')
print(f"   Loaded {df.shape[0]} rows, {df.shape[1]} columns")

# Show original distribution
original_counts = df['churn'].value_counts()
original_pcts = df['churn'].value_counts(normalize=True)

print(f"\n📊 ORIGINAL CLASS DISTRIBUTION:")
print(f"   No Churn:  {original_counts['No']:4d} ({original_pcts['No']:.1%})")
print(f"   Churn:     {original_counts['Yes']:4d} ({original_pcts['Yes']:.1%})")

# =============================================
# 2. PREPARE DATA
# =============================================
print("\n🔧 Preparing data...")
X = df.drop(['customer_id', 'churn'], axis=1)
y = (df['churn'] == 'Yes').astype(int)

# Encode categorical features
categorical_cols = X.select_dtypes(include=['object']).columns
label_encoders = {}

print("   Encoding categorical features:")
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le
    print(f"   ✓ {col}")

# Scale numerical features
scaler = StandardScaler()
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
print(f"   ✓ Scaled {len(numerical_cols)} numerical features")

# =============================================
# 3. SPLIT DATA (BEFORE SMOTE - CRITICAL!)
# =============================================
print("\n✂️ Splitting data (BEFORE SMOTE to avoid data leakage)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Training set: {X_train.shape[0]} samples")
print(f"   Training churn rate: {y_train.mean():.1%}")
print(f"   Test set: {X_test.shape[0]} samples")
print(f"   Test churn rate: {y_test.mean():.1%}")

# =============================================
# 4. APPLY SMOTE TO TRAINING DATA ONLY
# =============================================
print("\n🔄 Applying SMOTE to balance training data...")

# Count before SMOTE
train_churn_count = sum(y_train)
train_no_churn_count = len(y_train) - train_churn_count
print(f"   Before SMOTE - No Churn: {train_no_churn_count}, Churn: {train_churn_count}")

# Apply SMOTE
smote = SMOTE(random_state=42, sampling_strategy='auto')  # 'auto' balances to majority class
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Count after SMOTE
resampled_churn_count = sum(y_train_resampled)
resampled_no_churn_count = len(y_train_resampled) - resampled_churn_count
print(f"   After SMOTE  - No Churn: {resampled_no_churn_count}, Churn: {resampled_churn_count}")
print(f"   ✓ Training data now balanced! ({resampled_churn_count/len(y_train_resampled):.1%} churn)")

# =============================================
# 5. TRAIN MODELS ON BALANCED DATA
# =============================================
print("\n🤖 Training models on SMOTE-balanced data...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = []

for name, model in models.items():
    print(f"\n   Training {name}...")
    
    # Train on SMOTE-balanced data
    model.fit(X_train_resampled, y_train_resampled)
    
    # Predict on original test data (real-world performance)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Store results
    results.append({
        'Model': name,
        'Accuracy': f"{accuracy:.2%}",
        'Precision': f"{precision:.2%}",
        'Recall': f"{recall:.2%}",
        'F1 Score': f"{f1:.2%}"
    })
    
    print(f"   ✓ Accuracy: {accuracy:.2%}, Recall: {recall:.2%}, F1: {f1:.2%}")

# =============================================
# 6. DISPLAY RESULTS
# =============================================
print("\n" + "="*70)
print("📊 RESULTS WITH SMOTE (Synthetic Minority Oversampling)")
print("="*70)
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

# =============================================
# 7. FIND BEST MODEL (by F1 Score)
# =============================================
# Extract F1 scores as numbers
f1_scores = [float(r['F1 Score'].replace('%',''))/100 for r in results]
best_idx = np.argmax(f1_scores)
best_model = models[list(models.keys())[best_idx]]
best_name = list(models.keys())[best_idx]

print(f"\n🏆 Best model with SMOTE: {best_name}")
print(f"   F1 Score: {results[best_idx]['F1 Score']}")

# =============================================
# 8. DETAILED EVALUATION OF BEST MODEL
# =============================================
print("\n📋 Detailed Classification Report:")
y_pred_best = best_model.predict(X_test)
print(classification_report(y_test, y_pred_best, target_names=['No Churn', 'Churn']))

# =============================================
# 9. CONFUSION MATRIX
# =============================================
cm = confusion_matrix(y_test, y_pred_best)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Churn', 'Churn'],
            yticklabels=['No Churn', 'Churn'])
plt.title(f'Confusion Matrix - {best_name} with SMOTE', fontsize=14, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('results/confusion_matrix_smote.png')
plt.show()

# =============================================
# 10. COMPARE WITH ORIGINAL DISTRIBUTION
# =============================================
print("\n" + "="*70)
print("📊 CLASS DISTRIBUTION SUMMARY")
print("="*70)
print(f"Original data:      {original_counts['No']:4d} No Churn, {original_counts['Yes']:4d} Churn ({original_pcts['Yes']:.1%} churn)")
print(f"Training (original): {train_no_churn_count:4d} No Churn, {train_churn_count:4d} Churn ({train_churn_count/len(y_train):.1%} churn)")
print(f"Training (SMOTE):    {resampled_no_churn_count:4d} No Churn, {resampled_churn_count:4d} Churn ({resampled_churn_count/len(y_train_resampled):.1%} churn)")
print(f"Test (original):     {len(y_test)-sum(y_test):4d} No Churn, {sum(y_test):4d} Churn ({y_test.mean():.1%} churn)")

# =============================================
# 11. SAVE MODEL
# =============================================
model_filename = f'models/churn_model_{best_name.replace(" ", "_")}_smote.pkl'
joblib.dump(best_model, model_filename)
joblib.dump(label_encoders, 'models/label_encoders.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print(f"\n✅ Model saved to: {model_filename}")
print("✅ Label encoders saved")
print("✅ Scaler saved")
print("="*70)