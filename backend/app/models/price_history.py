from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="BRL")
    collected_at = Column(DateTime(timezone=True), server_default=func.now())