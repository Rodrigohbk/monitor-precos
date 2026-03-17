from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Cria a engine assíncrona
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,          # Exibe queries SQL no log (útil para desenvolvimento)
    future=True,
)

# Fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Classe base para modelos
Base = declarative_base()

# Dependência para obter uma sessão do banco de dados
async def get_db() -> AsyncSession:
    """
    Dependência que fornece uma sessão assíncrona do SQLAlchemy.
    A sessão é aberta no início da requisição e fechada automaticamente ao final.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()