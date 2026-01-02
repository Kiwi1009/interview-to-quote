from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class CaseStatus(str, enum.Enum):
    DRAFT = "draft"
    EXTRACTING = "extracting"
    REVIEWING = "reviewing"
    QUOTED = "quoted"
    ARCHIVED = "archived"

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    industry = Column(String)
    status = Column(Enum(CaseStatus), default=CaseStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="cases")
    uploads = relationship("Upload", back_populates="case", cascade="all, delete-orphan")
    transcript_segments = relationship("TranscriptSegment", back_populates="case", cascade="all, delete-orphan")
    extraction_runs = relationship("ExtractionRun", back_populates="case", cascade="all, delete-orphan")
    plans = relationship("Plan", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")

