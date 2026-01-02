from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.plan import PlanCode

class QuoteItemResponse(BaseModel):
    id: int
    category: str
    item_name: str
    spec: Optional[str]
    qty: float
    unit: str
    unit_price_low: float
    unit_price_high: float
    subtotal_low: Optional[float]
    subtotal_high: Optional[float]
    
    class Config:
        from_attributes = True

class PlanResponse(BaseModel):
    id: int
    case_id: int
    run_id: Optional[int]
    plan_code: PlanCode
    name: str
    assumptions_jsonb: Optional[Dict[str, Any]]
    quote_items: List[QuoteItemResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PlanUpdate(BaseModel):
    assumptions_jsonb: Optional[Dict[str, Any]] = None
    # Pricing overrides handled separately via quote_items

