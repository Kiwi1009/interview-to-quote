from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class PlanCode(str, enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    run_id = Column(Integer, ForeignKey("extraction_runs.id"))
    plan_code = Column(Enum(PlanCode), nullable=False)
    name = Column(String, nullable=False)
    assumptions_jsonb = Column(JSON)  # Plan-specific assumptions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="plans")
    quote_items = relationship("QuoteItem", back_populates="plan", cascade="all, delete-orphan")

