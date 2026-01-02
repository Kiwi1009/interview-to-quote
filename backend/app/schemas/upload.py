from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.upload import UploadType

class UploadResponse(BaseModel):
    id: int
    case_id: int
    type: UploadType
    filename: str
    path: str
    sha256: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

