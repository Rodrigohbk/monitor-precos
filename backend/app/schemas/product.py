from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    source_type: str  # "mercadolibre", "amazon", "shopee", "web_scraping"
    source_id: Optional[str] = None
    url: Optional[str] = None
    price_selector: Optional[str] = None
    interval_minutes: int = 60

class ProductOut(BaseModel):
    id: int
    name: str
    source_type: str
    source_id: Optional[str]
    url: Optional[str]
    interval_minutes: int
    is_active: bool
    last_collected_at: Optional[datetime]

    class Config:
        from_attributes = True   # permite converter do modelo SQLAlchemy