from pydantic import BaseModel
from datetime import datetime
from app.models.document import DocumentType, DocumentFormat

class DocumentResponse(BaseModel):
    id: int
    case_id: int
    run_id: Optional[int]
    doc_type: DocumentType
    format: DocumentFormat
    path: str
    created_at: datetime
    
    class Config:
        from_attributes = True

