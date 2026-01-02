from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DocumentType(str, enum.Enum):
    SPEC = "spec"
    REPORT = "report"
    QUOTE = "quote"

class DocumentFormat(str, enum.Enum):
    DOCX = "docx"
    PDF = "pdf"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    run_id = Column(Integer, ForeignKey("extraction_runs.id"))
    doc_type = Column(Enum(DocumentType), nullable=False)
    format = Column(Enum(DocumentFormat), nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="documents")

