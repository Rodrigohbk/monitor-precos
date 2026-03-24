import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

TEST_DATABASE_URL = settings.DATABASE_URL.replace("monitor_db", "monitor_test")

# Engine sem pool para evitar conexões compartilhadas
engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_size=0,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# ----------------------------------------------------------------------
# Fixture de setup/teardown das tabelas (executada antes/depois de cada teste)
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True, scope="function")
async def setup_database():
    # Cria as tabelas
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        # Fecha explicitamente a conexão para liberar recursos
        await conn.close()

    yield

    # Remove as tabelas
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()
        await conn.close()

    # Pequena pausa para permitir que tarefas assíncronas sejam finalizadas
    await asyncio.sleep(0.05)

# ----------------------------------------------------------------------
# Fixture do cliente HTTP (escopo function)
# ----------------------------------------------------------------------
@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# ----------------------------------------------------------------------
# Fixture de sessão para descartar o engine após todos os testes
# ----------------------------------------------------------------------
@pytest.fixture(scope="function", autouse=True)
async def dispose_engine():
    """Garante que o engine seja descartado após todos os testes."""
    yield
    await engine.dispose()