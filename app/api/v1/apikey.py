from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse
from app.schemas.apikey import APIKeyCreate, APIKeyResponse
from app.services.apikey_service import create_api_key
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_new_api_key(
    key_data: APIKeyCreate,
    current_user: UserResponse = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    
    real_user_id = current_user.user_id 

    return await create_api_key(
        db=db, 
        user_id=real_user_id,
        api_label=key_data,
    )