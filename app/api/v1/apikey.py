from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserResponse
from app.schemas.apikey import APIKeyCreate, APIKeyResponse, APIKeyCreationResponse, APIKeyUpdate
from app.services.api_service import APIService
from app.api.deps import get_current_user

router = APIRouter()

api_service = APIService()

# 1. Create API Key
@router.post("/create", response_model=APIKeyCreationResponse, status_code=status.HTTP_201_CREATED)
async def create_apikey(
    key_data: APIKeyCreate,
    current_user: UserResponse = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new API key for the authenticated user.
    """
    real_user_id = current_user.user_id 

    key_data_dict = key_data.model_dump(exclude_unset=True)

    return await api_service.create_apikey(
        user_id=real_user_id,
        key_data=key_data_dict,
        db=db, 
    )

# 2. Get all API Keys
@router.get("/", response_model=List[APIKeyResponse], status_code=status.HTTP_200_OK)
async def read_apikey(
    current_user: UserResponse = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all API keys belonging to the current user.
    """
    real_user_id = current_user.user_id 

    api_db = await api_service.get_apikey(
        user_id=real_user_id,
        db=db, 
    )
    
    # Check if the list is empty
    if not api_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No API keys found."
        )
    
    return api_db

# 3. Delete API Key
@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_apikey(
    label: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):  
    """
    Delete an API key by its label.
    """
    real_user_id = current_user.user_id

    return await api_service.delete_apikey(
        label=label,
        user_id=real_user_id,
        db=db
    )

# 4. Update API Key
@router.patch("/update", status_code=status.HTTP_200_OK)
async def update_apikey(
    key_data: APIKeyUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update specific fields (label, description, status) of an existing API key.
    """
    real_user_id = current_user.user_id

    # Convert Pydantic model to dict, excluding unset fields for partial update
    key_data_dict = key_data.model_dump(exclude_unset=True)

    return await api_service.update_apikey(
        update_data=key_data_dict,
        user_id=real_user_id,
        db=db,
    )