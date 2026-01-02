from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.extraction_run import ExtractionStatus

class ExtractionRunResponse(BaseModel):
    id: int
    case_id: int
    version: int
    model: Optional[str]
    prompt_hash: Optional[str]
    status: ExtractionStatus
    created_at: datetime
    finished_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class EvidenceResponse(BaseModel):
    field_path: str
    segment_idx: Optional[int]
    snippet: str
    start_char: Optional[int]
    end_char: Optional[int]

class RequirementsResponse(BaseModel):
    run_id: int
    jsonb_data: Dict[str, Any]
    confidence: Optional[Dict[str, float]]
    evidence: List[EvidenceResponse]
    created_at: datetime

