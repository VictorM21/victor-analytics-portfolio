"""
Customer Churn Prediction Model
Author: Victor Makanju
Purpose: Train multiple ML models and select the best one
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("CUSTOMER CHURN PREDICTION MODEL TRAINING")
print("="*60)

# =============================================
# 1. LOAD AND PREPARE DATA
# =============================================
print("\n📥 Step 1: Loading data.")
df = pd.read_csv('data/customer_churn_data.csv')
print(f"   Loaded {df.shape[0]} rows, {df.shape[1]} columns")

# Create feature matrix X and target y
# Drop customer_id (not useful) and churn (target)
X = df.drop(['customer_id', 'churn'], axis=1)
y = (df['churn'] == 'Yes').astype(int)  # Convert to 0/1

print(f"   Features: {X.shape[1]} columns")
print(f"   Target distribution: {y.value_counts().to_dict()}")

# =============================================
# 2. ENCODE CATEGORICAL FEATURES
# =============================================
print("\n🔧 Step 2: Encoding categorical features.")

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns
print(f"   Categorical columns: {list(categorical_cols)}")

# Label encode each categorical column
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le
    print(f"   ✓ Encoded {col}")

# =============================================
# 3. SCALE NUMERICAL FEATURES
# =============================================
print("\n📏 Step 3: Scaling numerical features.")

# Identify numerical columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
print(f"   Scaled {len(numerical_cols)} numerical columns")

# =============================================
# 4. SPLIT DATA
# =============================================
print("\n✂️ Step 4: Splitting into train/test sets.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Training set: {X_train.shape[0]} samples")
print(f"   Test set: {X_test.shape[0]} samples")
print(f"   Training churn rate: {y_train.mean():.2%}")
print(f"   Test churn rate: {y_test.mean():.2%}")

# =============================================
# 5. TRAIN MULTIPLE MODELS
# =============================================
print("\n🤖 Step 5: Training multiple models.")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = []

for name, model in models.items():
    print(f"\n   Training {name}.")
    
    # Train model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1,
        'CV Mean F1': cv_scores.mean(),
        'CV Std F1': cv_scores.std(),
        'Model Object': model
    })
    
    print(f"   ✓ Accuracy: {accuracy:.2%}, F1: {f1:.2%}")

# =============================================
# 6. COMPARE MODELS
# =============================================
print("\n📊 Step 6: Model Comparison")

results_df = pd.DataFrame(results)
results_df = results_df.drop('Model Object', axis=1)
print("\n" + results_df.to_string(index=False))

# Find best model
best_model_idx = results_df['F1 Score'].idxmax()
best_model_name = results_df.loc[best_model_idx, 'Model']
best_model = results[best_model_idx]['Model Object']

print(f"\n🏆 Best model: {best_model_name}")
print(f"   F1 Score: {results_df.loc[best_model_idx, 'F1 Score']:.2%}")
print(f"   Accuracy: {results_df.loc[best_model_idx, 'Accuracy']:.2%}")

# =============================================
# 7. CONFUSION MATRIX FOR BEST MODEL
# =============================================
print("\n📈 Step 7: Detailed evaluation of best model")

y_pred_best = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_best)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Churn', 'Churn'],
            yticklabels=['No Churn', 'Churn'])
plt.title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('results/confusion_matrix.png', dpi=100, bbox_inches='tight')
plt.show()

# Classification report
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred_best, 
                          target_names=['No Churn', 'Churn']))

# =============================================
# 8. ROC CURVE
# =============================================
print("\n📉 Step 8: ROC Curve Analysis")

y_pred_proba_best = best_model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba_best)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, 
         label=f'ROC curve (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title(f'ROC Curve - {best_model_name}', fontsize=14, fontweight='bold')
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/roc_curve.png', dpi=100, bbox_inches='tight')
plt.show()

print(f"\n✅ AUC Score: {roc_auc:.3f}")

# =============================================
# 9. FEATURE IMPORTANCE
# =============================================
print("\n🔍 Step 9: Feature Importance Analysis")

if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
    feature_names = X.columns
    
    # Sort features by importance
    indices = np.argsort(importances)[::-1]
    
    # Plot top 15 features
    plt.figure(figsize=(10, 8))
    plt.barh(range(min(15, len(indices))), 
             importances[indices][:15][::-1], 
             color='#3498db')
    plt.yticks(range(min(15, len(indices))), 
               [feature_names[i] for i in indices[:15][::-1]])
    plt.xlabel('Importance', fontsize=12)
    plt.title(f'Top 15 Feature Importances - {best_model_name}', 
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/feature_importance.png', dpi=100, bbox_inches='tight')
    plt.show()
    
    print("\n📊 Top 10 Most Important Features:")
    for i in range(10):
        print(f"   {i+1}. {feature_names[indices[i]]}: {importances[indices[i]]:.3f}")
else:
    print("   Model doesn't provide feature importances")

# =============================================
# 10. SAVE BEST MODEL
# =============================================
print("\n💾 Step 10: Saving model and encoders")

# Save model
model_filename = f'models/churn_model_{best_model_name.replace(" ", "_")}.pkl'
joblib.dump(best_model, model_filename)
print(f"   ✓ Model saved to: {model_filename}")

# Save encoders
joblib.dump(label_encoders, 'models/label_encoders.pkl')
print(f"   ✓ Label encoders saved to: /models/label_encoders.pkl")

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')
print(f"   ✓ Scaler saved to: /models/scaler.pkl")

# Save model comparison results
results_df.to_csv('results/model_comparison.csv', index=False)
print(f"   ✓ Results saved to: results/model_comparison.csv")

# =============================================
# 11. SUMMARY
# =============================================
print("\n" + "="*60)
print("✅ MODEL TRAINING COMPLETE")
print("="*60)
print(f"\nBest Model: {best_model_name}")
print(f"F1 Score: {results_df.loc[best_model_idx, 'F1 Score']:.2%}")
print(f"Accuracy: {results_df.loc[best_model_idx, 'Accuracy']:.2%}")
print(f"AUC: {roc_auc:.3f}")
print("\nFiles saved:")
print("   • models/churn_model_*.pkl - Trained model")
print("   • models/label_encoders.pkl - For encoding categories")
print("   • models/scaler.pkl - For scaling numbers")
print("   • results/confusion_matrix.png - Confusion matrix plot")
print("   • results/roc_curve.png - ROC curve plot")
print("   • results/feature_importance.png - Feature importance plot")
print("   • results/model_comparison.csv - Model comparison table")
print("="*60)