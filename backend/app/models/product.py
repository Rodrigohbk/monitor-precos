from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)  # "mercadolibre", "amazon", "shopee", "web_scraping"
    source_id = Column(String, nullable=True)     # ID do produto na fonte (ex.: MLB123456)
    url = Column(String, nullable=True)           # URL para scraping ou endpoint da API
    price_selector = Column(String, nullable=True) # seletor CSS para scraping
    interval_minutes = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    last_collected_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())