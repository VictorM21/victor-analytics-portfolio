import pandas as pd

# Load the data
df = pd.read_csv('data/customer_churn_data.csv')

# Check churn distribution
print("Churn counts:")
print(df['churn'].value_counts())

print("\nChurn percentages:")
print(df['churn'].value_counts(normalize=True) * 100)

print(f"\nTotal customers: {len(df)}")