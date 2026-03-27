"""
Pydantic schemas for Dynamic Pricing API
Author: Victor Makanju
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PriceRequest(BaseModel):
    """Request model for single product prediction"""
    product_id: str = Field(..., description="Unique product identifier")
    current_price: float = Field(..., gt=0, description="Current selling price")
    competitor_price: Optional[float] = Field(None, gt=0, description="Average competitor price")
    inventory_level: Optional[int] = Field(None, ge=0, description="Current stock level")
    days_since_release: Optional[int] = Field(None, ge=0, description="Product age in days")
    category: Optional[str] = Field(None, description="Product category")
    is_holiday_season: bool = Field(False, description="Holiday flag")

class PriceResponse(BaseModel):
    """Response model for single product prediction"""
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
    """Health check response"""
    status: str
    timestamp: str
    version: str
    model_loaded: bool