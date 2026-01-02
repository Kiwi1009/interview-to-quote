from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class QuoteItem(Base):
    __tablename__ = "quote_items"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    category = Column(String, nullable=False)  # e.g., "Main equipment", "EOAT & fixtures"
    item_name = Column(String, nullable=False)
    spec = Column(String)
    qty = Column(Float, default=1.0)
    unit = Column(String, default="set")
    unit_price_low = Column(Float, nullable=False)
    unit_price_high = Column(Float, nullable=False)
    subtotal_low = Column(Float)
    subtotal_high = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    plan = relationship("Plan", back_populates="quote_items")

