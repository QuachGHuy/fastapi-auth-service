from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse
from app.schemas.apikey import APIKeyCreate, APIKeyResponse
from app.services.api_service import APIService
from app.api.deps import get_current_user

router = APIRouter()

api_service = APIService()

@router.post("/", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_new_api_key(
    key_data: APIKeyCreate,
    current_user: UserResponse = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    
    real_user_id = current_user.user_id 

    return await api_service.create_apikey(
        user_id=real_user_id,
        label=key_data.label,
        db=db, 
    )