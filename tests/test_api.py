import pytest
from httpx import AsyncClient

# --- MOCK DATA ---
user_data = {
    "email": "test@example.com",
    "username": "tester01",
    "password": "password123",
}

# --- FIXTURE: Auto login & return header ---
@pytest.fixture
async def auth_headers(client: AsyncClient):
    # 1. Register
    await client.post("/api/v1/auth/register", json=user_data)
    
    # 2. Login
    login_res = await client.post("/api/v1/auth/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- TEST CASE ---
@pytest.mark.asyncio
async def test_create_apikey_success(client: AsyncClient, auth_headers): 

    apikey_payload = {
        "label": "test01",
    }
    
    # Send post request 
    response = await client.post(
        "/api/v1/api/create-apikey", 
        json=apikey_payload, 
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 201, f"Error: {response.text}"

    data = response.json()
    
    # Verify response structure
    assert data["label"] == apikey_payload["label"]
    assert "key" in data
    assert data["is_active"] is True

@pytest.mark.asyncio
async def test_read_apikey_success(client: AsyncClient, auth_headers):

    apikey_payload = {
        "label": "test01",
    }
    
    # Create a new apikey
    await client.post(
        "/api/v1/api/create-apikey", 
        json=apikey_payload, 
        headers=auth_headers
    )

    # Retrive apikey
    response = await client.get(
        "/api/v1/api/",
         headers=auth_headers
        )
    
    # Verify status code
    assert response.status_code == 200, f"Error: {response.text}"

    data = response.json()

     # Verify response structure
    assert data["label"] == apikey_payload["label"]
    assert "key" in data
    assert data["is_active"] is True