from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ExtractionStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionRun(Base):
    __tablename__ = "extraction_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    version = Column(Integer, default=1)  # Version number for this case
    model = Column(String)  # LLM model used
    prompt_hash = Column(String)  # Hash of prompt for reproducibility
    status = Column(Enum(ExtractionStatus), default=ExtractionStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True))
    
    # Relationships
    case = relationship("Case", back_populates="extraction_runs")
    extracted_requirements = relationship("ExtractedRequirement", back_populates="run", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="run", cascade="all, delete-orphan")

