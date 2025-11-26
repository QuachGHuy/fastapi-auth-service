import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# -------------------------CONFIGURATION------------------------- #

# Use SQLite in-memory database for tests.
# Benefits: 
# 1. Extremely fast (no disk I/O).
# 2. Isolation (data is lost after connection closes).
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create the Async Engine for Testing
engine =  create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Required for SQLite working with AsyncIO
    poolclass=StaticPool, # CRITICAL: Keeps the in-memory DB alive across multiple requests in the same test
    )

# Create a Session Factory 
TestingAsyncSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --------------------- DEPENDENCY OVERRIDE --------------------- #

async def override_get_db():
    """
    Replacement for the real 'get_db' dependency.
    This creates a session connected to the Mock Database (SQLite RAM).
    """
    async with TestingAsyncSession() as session:
        yield session

# --------------------------- FIXTURES --------------------------- #
@pytest.fixture(scope="function")
async def client():
    """
    Main Test Fixture.
    Lifecycle:
    1. SETUP: Create tables, Swap dependencies.
    2. YIELD: Provide the Test Client to the test function.
    3. TEARDOWN: Drop tables, Clear overrides.
    """
    # SETUP: Create the mock DB
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # SWAP: Replace the real DB connection with the mock DB
    app.dependency_overrides[get_db] = override_get_db

    # 2. EXECUTE TEST
    # Use ASGITransport to call the app directly (in-memory), bypassing network layers
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac # <--- The test function runs here

    # 3. TEARDOWN: Clean up after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Restore original dependencies
    app.dependency_overrides.clear()