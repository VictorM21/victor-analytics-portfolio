# Standard library
import os
import io
import uuid
import glob
import logging
from datetime import datetime
from typing import Optional, List

# Third‑party
import pandas as pd
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Local
from . import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================
# FastAPI App
# =============================================
app = FastAPI(
    title="Dynamic Pricing Engine API",
    description="Bayesian pricing engine with uncertainty quantification",
    version="1.0.0"
)

# =============================================
# Pydantic Models
# =============================================
class PriceRequest(BaseModel):
    product_id: str
    current_price: float
    competitor_price: Optional[float] = None
    inventory_level: Optional[int] = None
    days_since_release: Optional[int] = None
    category: Optional[str] = None
    is_holiday_season: bool = False

class PriceResponse(BaseModel):
    request_id: str
    product_id: str
    recommended_price: float
    confidence_interval: List[float]
    expected_profit: float
    expected_units: float
    risk_of_loss: float
    elasticity_estimate: float
    model_version: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    model_loaded: bool

# =============================================
# Model globals and loading
# =============================================
model = None
model_version = "1.0.0"
model_loaded = False

def load_latest_model():
    """Load the most recent trace file from models/artifacts/."""
    global model, model_loaded, model_version
    try:
        model_files = glob.glob('models/artifacts/trace_*.pkl')
        if not model_files:
            logger.warning("No model files found")
            model_loaded = False
            return
        latest_file = max(model_files, key=os.path.getctime)
        logger.info(f"Loading model from: {latest_file}")
        trace = joblib.load(latest_file)
        model = trace
        model_loaded = True
        timestamp = latest_file.split('_')[-1].replace('.pkl', '')
        model_version = f"1.0.0-{timestamp}"
        logger.info(f"Model loaded! Version: {model_version}")
    except Exception as e:
        logger.error(f"Error loading model: {e}", exc_info=True)
        model_loaded = False

load_latest_model()

# =============================================
# Helper function (placeholder)
# =============================================
def predict_price(product_data):
    """Placeholder prediction logic – to be replaced with real model."""
    base_price = product_data.get('current_price', 100)
    if base_price <= 0:
        base_price = 1.0

    competitor = product_data.get('competitor_price', base_price)

    if competitor and competitor < base_price:
        rec_price = base_price * 0.95
    else:
        rec_price = base_price * 1.02

    if rec_price <= 0:
        rec_price = 1.0

    uncertainty = base_price * 0.04

    return {
        'recommended_price': round(rec_price, 2),
        'lower_ci': round(rec_price - uncertainty, 2),
        'upper_ci': round(rec_price + uncertainty, 2),
        'expected_profit': round(rec_price * 0.3, 2),
        'expected_units': round(100 * (base_price / rec_price)),
        'risk': 0.05,
        'elasticity': -1.5
    }

# =============================================
# API Endpoints
# =============================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the service status, timestamp, version, and whether a model is loaded.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=model_version,
        model_loaded=model_loaded
    )

@app.post("/predict", response_model=PriceResponse)
async def predict_price_endpoint(request: PriceRequest):
    """
    Get a price recommendation for a single product.

    - **product_id**: Unique product identifier.
    - **current_price**: Current selling price (must be > 0).
    - **competitor_price**: (Optional) Average competitor price.
    - **inventory_level**: (Optional) Current stock level.
    - **days_since_release**: (Optional) Product age in days.
    - **category**: (Optional) Product category.
    - **is_holiday_season**: (Optional) Holiday flag.

    Returns a recommended price with a 90% credible interval and expected profit.
    """
    try:
        result = predict_price(request.dict())
        response = PriceResponse(
            request_id=str(uuid.uuid4()),
            product_id=request.product_id,
            recommended_price=result['recommended_price'],
            confidence_interval=[result['lower_ci'], result['upper_ci']],
            expected_profit=result['expected_profit'],
            expected_units=result['expected_units'],
            risk_of_loss=result['risk'],
            elasticity_estimate=result['elasticity'],
            model_version=model_version,
            timestamp=datetime.now().isoformat()
        )
        # Log to database (async? we can do it synchronously)
        db.log_prediction({
            'product_id': request.product_id,
            'current_price': request.current_price,
            'competitor_price': request.competitor_price,
            'recommended_price': result['recommended_price'],
            'lower_ci': result['lower_ci'],
            'upper_ci': result['upper_ci'],
            'expected_profit': result['expected_profit'],
            'risk': result['risk']
        })
        return response
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.post("/batch")
async def batch_predict(file: UploadFile = File(...)):
    """
    Process multiple products via CSV upload.

    Upload a CSV file with columns:
    - product_id (required)
    - current_price (required)
    - competitor_price (optional)
    - inventory_level (optional)
    - category (optional)
    - days_since_release (optional)

    Returns a CSV with predictions.
    """
    try:
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Validate required columns
        required = ['product_id', 'current_price']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing}")

        # Process each row
        results = []
        for _, row in df.iterrows():
            result = predict_price(row.to_dict())
            results.append({
                'product_id': row['product_id'],
                'current_price': row['current_price'],
                'recommended_price': result['recommended_price'],
                'lower_ci': result['lower_ci'],
                'upper_ci': result['upper_ci'],
                'expected_profit': result['expected_profit'],
                'risk': result['risk']
            })

        # Create output dataframe
        output_df = pd.DataFrame(results)

        # Ensure results directory exists
        os.makedirs("data/results", exist_ok=True)

        # Generate filename with timestamp
        output_filename = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = f"data/results/{output_filename}"
        output_df.to_csv(output_path, index=False)

        # Return file
        return FileResponse(
            output_path,
            media_type='text/csv',
            filename=output_filename
        )

    except Exception as e:
        logger.error(f"Batch processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Batch processing failed")

@app.get("/model/info")
async def model_info():
    """
    Get information about the currently loaded model.
    Returns model version, categories, and load status.
    """
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "model_version": model_version,
        "training_date": "2024-03-15",
        "categories": ["Laptops", "Smartphones", "Tablets", "Headphones", "Accessories"],
        "n_products": 50,
        "model_loaded": model_loaded
    }

@app.get("/stats")
async def get_stats():
    """
    Return basic statistics from the predictions database.
    """
    total, avg_profit = db.get_stats()
    return {
        "total_predictions": total,
        "average_expected_profit": avg_profit
    }

@app.on_event("startup")
async def startup_event():
    """Run on API startup."""
    db.init_db()                     # create database table
    logger.info("=" * 60)
    logger.info("🚀 Dynamic Pricing API Starting...")
    logger.info("=" * 60)
    logger.info(f"📊 Model loaded: {model_loaded}")
    logger.info(f"📁 Endpoints at /docs")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("=" * 60)
    logger.info("🛑 API Shutting Down")
    logger.info("=" * 60)