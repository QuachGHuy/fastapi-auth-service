import pytest
from httpx import AsyncClient

# ----------------------- MOCK DATA (FIXTURES) ----------------------- #
# Sample Data
user_data = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
}

# Data for testing duplicate email
user_data_1 = {
    "email": "test@example.com", # Same email
    "username": "testuser1", # Different username
    "password": "password123"
}

# Data for testing duplicate username
user_data_2 = {
    "email": "test1@example.com", # Different email
    "username": "testuser", # Same username
    "password": "password123"
}

# --------------------------HAPPY PATH TESTS-------------------------- #

@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """
    Scenario: Register a valid new user.
    Expected:
    - Status 201 Created
    - Returns the correct resonse
    - Sensitive data (password) is NOT returned
    """

    # Send registration request
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    # Verify status code
    assert response.status_code == 201

    data = response.json()

    # Verify data integrity
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

    # Verify default values
    assert data["points"] == 0
    assert data["rank"] == "Bronze"
    
    # Security Check: Password must never be returned
    assert "password" not in data
    assert "user_id" in data

@pytest.mark.asyncio
async def test_login_oauth2_success(client: AsyncClient):
    """
    Scenario: Login using OAuth2 Form Data.
    Expected:
    - Status 200 Ok
    - Returns the access token
    """

    # Create a user
    await client.post("/api/v1/auth/register", json=user_data)

    # Prepare the login form
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }

    # Post to login endpoint using 'data=' for Form Data
    response = await client.post("/api/v1/auth/login/form", data=login_data)
    
    # Verify status code
    assert response.status_code == 200, f"Error: {response.text}"

    data = response.json()

    # Verify access token standard
    assert data["token_type"].lower() == "bearer"
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_json_success(client: AsyncClient):
    """
    Scenario: Login using Json.
    Expected:
    - Status 200 Ok
    - Returns the access token
    """

    # Create a user
    await client.post("/api/v1/auth/register", json=user_data)
    
    # Prepare the login form
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }

    # Post to login endpoint using 'json=' for json data
    response = await client.post("/api/v1/auth/login", json=login_data)

    # Verify status code
    assert response.status_code == 200, f"Error: {response.text}"

    data = response.json()

    # Verify access token standard
    assert data["token_type"].lower() == "bearer"
    assert "access_token" in data

@pytest.mark.asyncio
async def test_access_token_protect(client: AsyncClient):
    """
    Scenario: Integration Test (Full Flow)
    Register -> Login -> Get Token -> Access Protected Route (/users/me).

    Expected:
    - Status 200 Ok
    - Returns the correct resonse
    - Sensitive data (password) is NOT returned
    """

    # Create a user
    await client.post("/api/v1/auth/register", json=user_data)

    # Login and retrive Access Token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    log_res = await client.post("/api/v1/auth/login", json=login_data)
    token = log_res.json()["access_token"]

    # Access protected endpoint
    # NOTE: Header must follow "Bearer <token>" format
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users/me", headers=headers)

    # Verify status code
    assert response.status_code == 200, f"Error: {response.text}"

    data = response.json()

    # Verify the identity
    assert data["username"] == login_data["username"]

    # Verify the reponse
    assert "user_id" in data
    assert "email" in data
    assert "points" in data
    assert "rank" in data
    assert "created_at" in data

    # Security check: password is NOT returned
    assert "password" not in data

# -----------------------------EDGE CASES----------------------------- #

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Validation Check: Ensure email uniqueness."""
        
    # Create the first user
    await client.post("/api/v1/auth/register", json=user_data)

    # Create the 2nd user with same email
    response = await client.post("/api/v1/auth/register", json=user_data_1)

    # Verify status code & error handing
    assert response.status_code == 400, f"Error: {response.text}"
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    """Validation Check: Ensure username uniqueness."""
    # Create the first user
    await client.post("/api/v1/auth/register", json=user_data)

    # Create the 2nd user with same username
    response = await client.post("/api/v1/auth/register", json=user_data_2)

    # Verify status code & error handing
    assert response.status_code == 400, f"Error: {response.text}"
    assert response.json()["detail"] == "Username already registered"

@pytest.mark.asyncio
async def test_login_oauth2_wrong_password(client: AsyncClient):
    """Security Check: Reject invalid credentials with wrong password."""
    # Create a user
    await client.post("/api/v1/auth/register", json=user_data)
    
    # Prepare a wrong password login data & login 
    login_data = {
        "username": user_data["username"],
        "password": "password456" # Invalid password
    }

    response = await client.post("/api/v1/auth/login/form", data=login_data)

    # Verify status code & error handing
    assert response.status_code == 401, f"Error: {response.text}"
    assert response.json()["detail"] == "Incorrect username or password"

@pytest.mark.asyncio
async def test_login_json_wrong_username(client: AsyncClient):
    """Security Check: Reject invalid credentials with wrong password."""
    
    # Create a user
    await client.post("/api/v1/auth/register", json=user_data)

    # Prepare a wrong password login data & login
    login_data = {
        "username": "testuser2",
        "password": user_data["password"]
    }

    response = await client.post("/api/v1/auth/login", json=login_data)

    # Verify status code & error handing
    assert response.status_code == 401, f"Error: {response.text}"
    assert response.json()["detail"] == "Incorrect username or password"

@pytest.mark.asyncio
async def test_access_token_invalid(client: AsyncClient):
    """Security Check: Fake tokens must be rejected by the dependency."""

    # Forge a fake token
    invalid_token = "1111111111111111111111111111111"
    headers = {"Authorization": f"Bearer {invalid_token}"}

    # Access protected endpoint with a fake token
    response = await client.get("/api/v1/users/me", headers=headers)

    # Verify status code
    assert response.status_code == 401, f"Error: {response.text}"

