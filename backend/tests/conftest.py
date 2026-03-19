import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Configuração do banco de dados de teste
# Usa a mesma URL do banco principal, mas com nome diferente (ex: monitor_test)
# Se você não criou um banco de teste, pode comentar a linha do engine e usar SQLite em memória
TEST_DATABASE_URL = settings.DATABASE_URL.replace("monitor_db", "monitor_test")

# Engine assíncrono para o banco de teste
engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Sessão de teste
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Sobrescreve a dependência get_db para usar o banco de teste
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Fixture que cria e dropa as tabelas antes/depois de cada teste
@pytest.fixture(autouse=True)
async def setup_database():
    # Cria as tabelas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Dropa as tabelas (opcional, pode deixar comentado se quiser preservar entre testes)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Fixture que fornece um cliente HTTP assíncrono para testar os endpoints
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac