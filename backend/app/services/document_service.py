import os
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.case import Case
from app.models.document import Document, DocumentType, DocumentFormat
from app.models.extraction_run import ExtractionRun
from app.core.config import settings

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        os.makedirs(settings.DOCUMENT_PATH, exist_ok=True)
    
    def list_documents(self, case_id: int, run_id: Optional[int] = None) -> List[Document]:
        query = self.db.query(Document).filter(Document.case_id == case_id)
        if run_id:
            query = query.filter(Document.run_id == run_id)
        return query.all()
    
    def get_document_path(self, doc_id: int) -> Optional[str]:
        doc = self.db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return None
        return doc.path

