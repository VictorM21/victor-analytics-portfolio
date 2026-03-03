&nbsp;Customer Churn Prediction - Machine Learning Pipeline



&nbsp;📊 Project Overview

This project builds a machine learning model to predict customer churn for a telecom company. The goal is to identify customers likely to cancel their service so the business can take proactive retention measures.



&nbsp;🎯 Business Problem

Customer churn costs businesses millions in lost revenue. By predicting which customers are at risk, companies can:

\- Offer targeted discounts

\- Provide proactive customer support

\- Improve retention strategies

\- Reduce customer acquisition costs



&nbsp;📁 Dataset

\- 5000 customer records

\- 21 features including:

&nbsp; - Demographics (gender, age, dependents)

&nbsp; - Account info (tenure, contract type)

&nbsp; - Services (internet, phone, streaming)

&nbsp; - Billing (monthly charges, payment method)

\- Target: Churn (Yes/No)



&nbsp;🛠️ Tech Stack

\- Python (pandas, numpy, scikit-learn)

\- Visualization (matplotlib, seaborn)

\- Jupyter Notebooks for EDA

\- Model Persistence (joblib)



&nbsp;📈 Key Findings



&nbsp;Top Risk Factors

1\. Month-to-month contracts - 3x higher churn rate

2\. Short tenure (< 6 months)

3\. Fiber optic internet (competition offers better deals)

4\. Electronic check payment (less automated)



&nbsp;Protective Factors

\- Long-term contracts (1-2 years)

\- Having dependents/family

\- Longer tenure (> 2 years)

\- Credit card/automatic payments



&nbsp;🤖 Model Performance



| Model | Accuracy | Precision | Recall | F1 Score |

|-------|----------|-----------|--------|----------|

| Random Forest | 82% | 81% | 79% | 80% |

| Gradient Boosting | 81% | 80% | 78% | 79% |

| Logistic Regression | 78% | 76% | 74% | 75% |

| Decision Tree | 74% | 72% | 71% | 71% |



Best Model: Random Forest

\- AUC Score: 0.85

\- F1 Score: 80%



&nbsp;📊 Visualizations



&nbsp;Confusion Matrix

!\[Confusion Matrix](results/confusion\_matrix.png)



&nbsp;ROC Curve

!\[ROC Curve](results/roc\_curve.png)



&nbsp;Feature Importance

!\[Feature Importance](results/feature\_importance.png)



&nbsp;🚀 How to Run



&nbsp;1. Generate Data

```bash

python data/generate\_customer\_data.py

