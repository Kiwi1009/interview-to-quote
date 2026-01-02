from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExtractedRequirement(Base):
    __tablename__ = "extracted_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("extraction_runs.id"), nullable=False)
    jsonb_data = Column(JSON, nullable=False)  # Full extracted JSON
    confidence = Column(JSON)  # Confidence scores per section
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    run = relationship("ExtractionRun", back_populates="extracted_requirements")

