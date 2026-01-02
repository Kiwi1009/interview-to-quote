from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class UploadType(str, enum.Enum):
    TRANSCRIPT = "transcript"
    PHOTO = "photo"

class Upload(Base):
    __tablename__ = "uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    type = Column(Enum(UploadType), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    sha256 = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="uploads")

