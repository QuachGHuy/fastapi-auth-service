from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse
from app.schemas.apikey import APIKeyCreate, APIKeyResponse
from app.services.api_service import APIService
from app.api.deps import get_current_user

router = APIRouter()

api_service = APIService()

@router.post("/create-apikey", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
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

@router.get("/", response_model=APIKeyResponse, status_code=status.HTTP_200_OK)
async def read_api_key(
    current_user: UserResponse = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    
    real_user_id = current_user.user_id 

    api_db = await api_service.get_apikey(
        user_id=real_user_id,
        db=db, 
    )
    
    if not api_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="apikey not exists"
        )
    
    return api_db

@router.delete("/delete-api", status_code=status.HTTP_200_OK)
async def delete_api_key(
    label: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):  
    real_user_id = current_user.user_id

    return await api_service.delete_apikey(
        label=label,
        user_id=real_user_id,
        db=db
    )
