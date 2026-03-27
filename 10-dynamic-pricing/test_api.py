"""
Test script for Dynamic Pricing API
Author: Victor Makanju
Demonstrates how to call the /predict and /batch endpoints.
"""

import requests
import pandas as pd
import json
from datetime import datetime

# Base URL of your API (adjust if different)
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print("🔍 Health Check:")
    print(response.json())
    print("-" * 50)

def test_predict_single():
    """Test single prediction with a sample product."""
    payload = {
        "product_id": "P001",
        "current_price": 100.0,
        "competitor_price": 95.0
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print("📦 Single Prediction:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_batch():
    """Test batch prediction by uploading a CSV."""
    # Create a sample CSV file on the fly
    df = pd.DataFrame({
        "product_id": ["P001", "P002", "P003"],
        "current_price": [100.0, 150.0, 200.0],
        "competitor_price": [95.0, None, 210.0]
    })
    csv_file = "temp_batch.csv"
    df.to_csv(csv_file, index=False)

    # Upload and get results
    with open(csv_file, "rb") as f:
        files = {"file": (csv_file, f, "text/csv")}
        response = requests.post(f"{BASE_URL}/batch", files=files)

    if response.status_code == 200:
        # Save the returned CSV
        out_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(out_file, "wb") as out:
            out.write(response.content)
        print(f"📁 Batch results saved to {out_file}")
        # Show first few lines
        df_result = pd.read_csv(out_file)
        print(df_result.to_string())
    else:
        print(f"❌ Batch failed: {response.text}")
    print("-" * 50)

def test_model_info():
    """Test the model info endpoint."""
    response = requests.get(f"{BASE_URL}/model/info")
    if response.status_code == 200:
        print("📊 Model Info:")
        print(response.json())
    else:
        print(f"ℹ️ Model info not available (status {response.status_code}): {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Testing Dynamic Pricing API")
    print("=" * 60)

    test_health()
    test_predict_single()
    test_batch()
    test_model_info()