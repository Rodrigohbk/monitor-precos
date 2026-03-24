from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.core.database import Base

class SourceCredentials(Base):
    __tablename__ = "source_credentials"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_type = Column(String, nullable=False)   # "mercadolibre", "amazon", etc.
    credentials = Column(JSON, nullable=False)     # armazena tokens, client_id, etc.