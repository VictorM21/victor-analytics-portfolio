"""
Exploratory Data Analysis (EDA) Template
Author: Victor Makanju
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("EDA Template Started")
print("=" * 50)

# Load the data
df = pd.read_csv('sample_sales_data.csv')
print(f"\n Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Basic info
print("\n First 5 rows:")
print(df.head())

print("\n Data Types:")
print(df.dtypes)

# Summary statistics
print("\n Summary Statistics:")
print(df.describe())

# Check for missing values
print("\n Missing Values:")
print(df.isnull().sum())

# Create output directory
output_dir = "eda_output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create correlation plot if there are numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation.png'))
    plt.show()
    print(f"\n Saved correlation plot to {output_dir}/correlation.png")

print("\n" + "=" * 50)
print(" EDA Complete!")
print("=" * 50)