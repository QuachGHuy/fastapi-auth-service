import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import UserCreate
from app.security import get_hashed_password

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Retrieve a user from the database by their email address.
    
    - **db**: Database session.
    - **email**: The email to search for.
    
    Returns:
    - User object if found, otherwise None.
    """
    # Execute a SELECT query filtering by email
    result = await db.execute(select(User).where(User.email == email))

    # Return the single scalar result or None if no rows found
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    """
    Retrieve a user from the database by their username.
    
    - **db**: Database session.
    - **username**: The username to search for.
    
    Returns:
    - User object if found, otherwise None.
    """
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_user_id(db: AsyncSession, user_id: int):
    """
    Retrieve a user by their user_id (Primary Key).
    Used mainly by dependencies (e.g., get_current_user) to verify user existence.
    """
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate):
    """
    Create a new user in the database.

    **Logic:**
    1. Hash the plain password (CPU-bound task).
    2. Create a User model instance.
    3. Add to session and commit to save changes.
    4. Refresh to get the generated ID and default values (e.g., created_at).

    - **user**: Pydantic schema containing registration data.
    """

    # 1. Hash Password
    # NOTE: Password hashing is a CPU-intensive operation (blocking).
    # We use `asyncio.to_thread` to run it in a separate thread, 
    # preventing it from blocking the main Async event loop.
    hashed_password = await asyncio.to_thread(get_hashed_password, user.password)
    
    # 2. Create DB Model
    db_user = User(
        email = user.email,
        username = user.username,
        password = hashed_password
    )

    # 3. Save to DB
    db.add(db_user)
    await db.commit()

    # 4. Refresh to retrieve auto-generated fields (id, created_at)
    await db.refresh(db_user)
    
    return db_user



    