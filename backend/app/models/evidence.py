from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("extraction_runs.id"), nullable=False)
    field_path = Column(String, nullable=False)  # e.g., "workpiece.weight_range"
    segment_idx = Column(Integer)  # Reference to transcript_segments.idx
    snippet = Column(String, nullable=False)  # Text snippet from transcript
    start_char = Column(Integer)
    end_char = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    run = relationship("ExtractionRun", back_populates="evidence")

