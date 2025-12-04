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

# --- HAPPY CASE ---
@pytest.mark.asyncio
async def test_create_apikey_success(client: AsyncClient, auth_headers): 

    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Send post request 
    response = await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 201, f"Error: {response.text}"

    # Verify response structure
    data = response.json()
    assert data["label"] == apikey_payload["label"]
    assert data["description"] == apikey_payload["description"]

    assert "key" in data
    assert data["key"].startswith("sk_")

    assert data["is_active"] is True
    assert "key_id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_read_apikey_success(client: AsyncClient, auth_headers):

    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create a new apikey
    await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    # Retrive apikey
    response = await client.get(
        "/api/v1/keys/",
         headers=auth_headers
        )
    
    # Verify status code
    assert response.status_code == 200, f"Error: {response.text}"

    # Verify response structure
    data = response.json()
    assert data[0]["label"] == apikey_payload["label"]
    assert data[0]["description"] == apikey_payload["description"]
    assert data[0]["is_active"] is True
    assert "key_id" in data[0]
    assert "created_at" in data[0]
    assert "key" not in data[0]
    
@pytest.mark.asyncio
async def test_delete_apikey_success(client: AsyncClient, auth_headers):

    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create a new apikey
    await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    # Delete apikey
    apikey_delete = {
        "label": apikey_payload["label"]
    }
    
    response = await client.delete(
        "/api/v1/keys/delete",
        params=apikey_delete,
        headers=auth_headers,
        )
    
    # Verify status code
    assert response.status_code == 200, f"Error: {response.text}"

    # Check responese message
    data = response.json()
    assert data["message"] == "APIkey deleted successfully."

@pytest.mark.asyncio
async def test_update_apikey_label_description_success(client: AsyncClient, auth_headers):
    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create a new apikey and get key_id
    res = await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    key_data = res.json()
    key_id = key_data["key_id"]

    # Update apikey data
    apikey_data = {
        "key_id": key_id,
        "label": "changed_label",
        "description": "changed_label"
    }

    response = await client.patch(
        "/api/v1/keys/update",
        json=apikey_data,
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 200, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["message"] == f"API Key {apikey_data["key_id"]} updated successfully."

@pytest.mark.asyncio
async def test_update_apikey_status_success(client: AsyncClient, auth_headers):
    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create a new apikey and get key_id
    res = await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    key_data = res.json()
    key_id = key_data["key_id"]

    # Update apikey data
    apikey_data = {
        "key_id": key_id,
        "is_active": False
    }

    response = await client.patch(
        "/api/v1/keys/update",
        json=apikey_data,
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 200, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["message"] == f"API Key {apikey_data["key_id"]} updated successfully."

# --- EDGE CASE ---
@pytest.mark.asyncio
async def test_create_apikey_duplicate_label(client: AsyncClient, auth_headers):  
    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create apikey
    await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    apikey_duplicate_label = {
        "label": apikey_payload["label"],
        "description": "this key is duplicated"
    }

    # Create duplicated apikey
    response = await client.post(
        "/api/v1/keys/create", 
        json=apikey_duplicate_label, 
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 400, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["detail"] == f"API key label '{apikey_payload["label"]}' already exists."

@pytest.mark.asyncio
async def test_read_aipkey_empty(client: AsyncClient, auth_headers):
    # Retrive all apikey
    response = await client.get(
        "/api/v1/keys/",
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 404, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["detail"] == "No API keys found."

@pytest.mark.asyncio
async def test_delete_apikey_wrong_label(client: AsyncClient, auth_headers):
    
    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create apikey
    await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    # Delete apikey with wrong label
    apikey_wrong_label = {
        "label": "wrong_label"
    }

    response = await client.delete(
        "/api/v1/keys/delete",
        params=apikey_wrong_label,
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code==404, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["detail"] == f"APIKey with label '{apikey_wrong_label["label"]}' not found."

@pytest.mark.asyncio
async def test_update_apikey_no_field_input(client: AsyncClient, auth_headers):
    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
    
    # Create a new apikey and get key_id
    res = await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    key_data = res.json()
    key_id = key_data["key_id"]

    # Update apikey data
    apikey_data = {
        "key_id": key_id,
    }

    response = await client.patch(
        "/api/v1/keys/update",
        json=apikey_data,
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 400, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["detail"] == "No fields provided for update."

@pytest.mark.asyncio
async def test_update_apikey_label_duplicate(client: AsyncClient, auth_headers):
    apikey_1 = {
        "label": "test01",
        "description": "this key is used for testing"
    }

    apikey_2 = {
        "label": "test02",
        "description": "this key is used for testing"
    }
    
    # Create 2 apikeys and get key_id of apikey_2
    await client.post("/api/v1/keys/create",json=apikey_1, headers=auth_headers)

    res = await client.post(
        "/api/v1/keys/create", 
        json=apikey_2, 
        headers=auth_headers
    )

    key_data = res.json()
    key_id_2 = key_data["key_id"]

    # Update apikey_2's label by the same label of apikey_1
    apikey_data = {
        "key_id": key_id_2,
        "label": apikey_1["label"],
    }

    response = await client.patch(
        "/api/v1/keys/update",
        json=apikey_data,
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 400, f"Error:{response.text}"

    # Check response message
    data = response.json()
    assert data["detail"] == f"APIKey with label '{apikey_1["label"]}' is already existed."

@pytest.mark.asyncio
async def test_update_apikey_status_redundant(client: AsyncClient, auth_headers):
    apikey_payload = {
        "label": "test01",
        "description": "this key is used for testing"
    }
 
    # Create apikeys and get key_id 
    res = await client.post(
        "/api/v1/keys/create", 
        json=apikey_payload, 
        headers=auth_headers
    )

    key_data = res.json()
    key_id = key_data["key_id"]

    # Update status by True -- default is True
    apikey_data = {
        "key_id": key_id,
        "is_active": True,
    }

    response = await client.patch(
        "/api/v1/keys/update",
        json=apikey_data,
        headers=auth_headers
    )

    # Verify status code
    assert response.status_code == 400, f"Error:{response.text}"

    # Check response message
    data = response.json()
    status_str = "active" if apikey_data["is_active"] else "inactive"
    assert data["detail"] == f"API key is already {status_str}."