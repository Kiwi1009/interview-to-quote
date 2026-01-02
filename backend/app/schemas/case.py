from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.case import CaseStatus

class CaseCreate(BaseModel):
    title: str
    industry: Optional[str] = None
    user_id: int = 1  # TODO: Get from auth

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[CaseStatus] = None

class CaseResponse(BaseModel):
    id: int
    user_id: int
    title: str
    industry: Optional[str]
    status: CaseStatus
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

