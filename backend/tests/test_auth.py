import pytest
from httpx import AsyncClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "secret123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    # Primeiro registro
    await client.post("/api/v1/auth/register", json={
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "secret123"
    })
    # Segundo com mesmo email
    response = await client.post("/api/v1/auth/register", json={
        "email": "duplicate@example.com",
        "username": "user2",
        "password": "secret123"
    })
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    # Registrar
    await client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "secret123"
    })
    # Login
    response = await client.post("/api/v1/auth/login", data={
        "username": "loginuser",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_products_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/products/")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_products_authorized(client: AsyncClient):
    # Registrar e logar
    await client.post("/api/v1/auth/register", json={
        "email": "prod@example.com",
        "username": "produser",
        "password": "secret123"
    })
    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "produser",
        "password": "secret123"
    })
    token = login_resp.json()["access_token"]
    
    # Acessar produtos com token
    response = await client.get(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 3
    assert products[0]["name"] == "Notebook Gamer"