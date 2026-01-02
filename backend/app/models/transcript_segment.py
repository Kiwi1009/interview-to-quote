from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    idx = Column(Integer, nullable=False)  # Order in transcript
    speaker = Column(String)  # Optional speaker name
    text = Column(String, nullable=False)
    start_char = Column(Integer, nullable=False)  # Character position in full transcript
    end_char = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="transcript_segments")

