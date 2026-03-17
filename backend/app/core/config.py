from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configurações gerais da aplicação
    PROJECT_NAME: str = "Monitor de Preços"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Segurança
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Banco de dados
    DATABASE_URL: str
    REDIS_URL: Optional[str] = None  # Opcional para Celery

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignora variáveis extras no .env

settings = Settings()