import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# URL do banco de testes
TEST_DATABASE_URL = settings.DATABASE_URL.replace("monitor_db", "monitor_test")

# Engine assíncrona para testes (echo=False para logs limpos)
engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Sessão local para testes
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Sobrescreve a dependência get_db para usar a sessão de teste
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Fixture que cria/destroi as tabelas antes/depois de cada teste
@pytest.fixture(autouse=True, scope="function")
async def setup_database():
    """Cria as tabelas antes de cada teste e as remove depois."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Fixture que fornece um cliente HTTP assíncrono usando ASGITransport
@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Retorna um cliente HTTP assíncrono configurado com a app FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac