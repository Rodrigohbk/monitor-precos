import pytest
from httpx import AsyncClient
from app.main import app

async def test_create_product(client: AsyncClient, auth_token):
    response = await client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "source_type": "web_scraping",
            "url": "https://example.com",
            "price_selector": ".price"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"