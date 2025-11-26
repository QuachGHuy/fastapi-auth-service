from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserResponse
from app.deps import get_current_user

router = APIRouter(tags=["Users"])

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retrieve the currently authenticated User's profile.

    **Authentication:**
    - Requires a valid "Bearer <token>" in the Authorization header.
    
    **Returns:**
    - User profile information (id, username, email, etc.).
    - Sensitive data like password is automatically filtered out by UserResponse.
    """
    # We don't need to query the DB here.
    # The "get_current_user" dependency in has already validated the token,
    # fetched the user from the DB, and injected it into "current_user".
    return current_user

    