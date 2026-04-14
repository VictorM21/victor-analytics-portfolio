import os
import time
import statistics
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.classifier import classify_product
from app.database import init_db, log_prediction, get_recent_predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="LLM Product Classifier",
    description="Few-shot product classification with uncertainty scoring and human-in-the-loop routing.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------- Request / Response models ----------

class ClassifyRequest(BaseModel):
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Wireless noise-cancelling over-ear headphones with 30-hour battery life and foldable design"
            }
        }
    }


class ClassifyResponse(BaseModel):
    description: str
    category: str
    confidence: float
    flagged_for_review: bool
    reasoning: str
    latency_ms: float
    timestamp: str


class MetricsResponse(BaseModel):
    total_predictions: int
    flag_rate: float
    avg_confidence: float
    avg_latency_ms: float
    category_distribution: dict
    window_hours: int


# ---------- Routes ----------

@app.post("/classify", response_model=ClassifyResponse)
async def classify(request: ClassifyRequest):
    """Classify a product description using few-shot prompting."""
    if not request.description.strip():
        raise HTTPException(status_code=422, detail="Description cannot be empty.")

    start = time.time()
    result = classify_product(request.description)   # No await – it's a regular function
    latency_ms = round((time.time() - start) * 1000, 1)

    confidence_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))
    flagged = result["confidence"] < confidence_threshold

    response = ClassifyResponse(
        description=request.description,
        category=result["category"],
        confidence=result["confidence"],
        flagged_for_review=flagged,
        reasoning=result["reasoning"],
        latency_ms=latency_ms,
        timestamp=datetime.utcnow().isoformat(),
    )

    log_prediction(response.model_dump())
    return response


@app.get("/metrics", response_model=MetricsResponse)
async def metrics(hours: int = 24):
    """Rolling metrics over the last N hours."""
    rows = get_recent_predictions(hours)

    if not rows:
        return MetricsResponse(
            total_predictions=0,
            flag_rate=0.0,
            avg_confidence=0.0,
            avg_latency_ms=0.0,
            category_distribution={},
            window_hours=hours,
        )

    confidences = [r["confidence"] for r in rows]
    latencies = [r["latency_ms"] for r in rows]
    flagged = [r for r in rows if r["flagged_for_review"]]

    category_dist: dict = {}
    for r in rows:
        category_dist[r["category"]] = category_dist.get(r["category"], 0) + 1

    return MetricsResponse(
        total_predictions=len(rows),
        flag_rate=round(len(flagged) / len(rows), 3),
        avg_confidence=round(statistics.mean(confidences), 3),
        avg_latency_ms=round(statistics.mean(latencies), 1),
        category_distribution=category_dist,
        window_hours=hours,
    )


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}