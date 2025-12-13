from typing import Dict, Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.apikey import APIKey
from app.core.security import SecurityUtils
from app.core.config import settings

class APIService:
    """
    Service layer handling business logic for API Key management.
    """

    async def create_apikey(self, db: AsyncSession, user_id: int, key_data: Dict[str, Any]) -> APIKey:
        """
        Create a new API key with a unique label for the user.
        """
        # 1. Check for duplicate label for this user
        key_label = key_data["label"]
        stmt =(
            select(APIKey).
            where(APIKey.user_id==user_id, APIKey.label==key_label)     
            )
        
        label_duplicate = await db.execute(stmt)

        if label_duplicate.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"API key label '{key_label}' already exists."
            )
        
        # 2. Generate secure token
        generated_token = SecurityUtils.create_api_token()

        # 3. Add prefix based on environment
        if settings.ENVIRONMENT == "prod":
            key = f"sk_live_{generated_token}"
        else:
            key = f"sk_test_{generated_token}"
        
        prefix = key[:10]

        hashed_key = SecurityUtils.get_hashed_token(key[10:])
        
        # 4. Save to database
        key_db = APIKey(
            user_id=user_id,
            prefix=prefix,
            key=hashed_key,
            is_active=True,
            **key_data
        )

        db.add(key_db)
        await db.commit()
        await db.refresh(key_db)

        key_db.key = key

        return key_db
    
    async def get_apikey(self, db: AsyncSession, user_id: int):
        """
        Retrieve all API keys for the specified user.
        """
        stmt = (select(APIKey).where(APIKey.user_id==user_id))
        result = await db.execute(stmt)

        return result.scalars().all()
    
    async def delete_apikey(self, db: AsyncSession, label: str, user_id: int) -> Dict:
        """
        Permanently delete an API key by its label.
        """
        # 1. Find the key
        stmt = (
            select(APIKey).
            where(APIKey.user_id==user_id , APIKey.label==label)
            )
        
        result = await db.execute(stmt)
        apikey_db = result.scalar_one_or_none()

        # 2. Handle not found
        if not apikey_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"APIKey with label '{label}' not found."
            )
        
        # 3. Delete record
        await db.delete(apikey_db)
        await db.commit()

        return {"message": "APIkey deleted successfully."}
    
    async def update_apikey(self, db: AsyncSession, user_id:int, key_id: int, update_data: Dict[str, Any]):
        """
        Update API key details (label, description, is_active) dynamically.
        """
        # 1. Check if key exists and belongs to user
        stmt_key_check = (
            select(APIKey).
            where(APIKey.user_id==user_id, APIKey.key_id==key_id)
            
        )

        key_exist = await db.execute(stmt_key_check)

        if not key_exist.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"API key with ID {key_id} not found."
            )
        
        # 2. Ensure data is provided
        if len(update_data)==0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update."
            )
        
        # 3. Check for label duplication (excluding current key)
        if "label" in update_data:
            new_label = update_data["label"]

            stmt_label_check = (
                select(APIKey).
                where(APIKey.user_id==user_id, APIKey.key_id!=key_id, APIKey.label==new_label)
            )

            label_duplicate = await db.execute(stmt_label_check)

            if label_duplicate.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"APIKey with label '{new_label}' is already existed."
                )
        
        # 4. Check status redundancy
        if "is_active" in update_data:
            new_status = update_data["is_active"]

            stmt_status_check = (
                select(APIKey).
                where(APIKey.user_id==user_id, APIKey.key_id==key_id, APIKey.is_active==new_status)
            )

            status_check = await db.execute(stmt_status_check)

            if status_check.scalar_one_or_none():
                status_str = "active" if new_status else "inactive"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"API key is already {status_str}."
                )            

        # 5. Update key
        stmt_update = (
            update(APIKey).
            where(APIKey.user_id==user_id, APIKey.key_id==key_id).
            values(**update_data)
        )

        await db.execute(stmt_update)
        await db.commit()

        return {"message": f"API Key {key_id} updated successfully."}
    
    async def verify_key_and_get_key(self, key: str, db: AsyncSession) -> APIKey:
        """
        Verify API key.
        """
        prefix = key[:10]
        raw_key = key[10:]

        # 1. Check if prefix exists and verify key by raw_key
        stmt = (
            select(APIKey).
            where(APIKey.prefix == prefix)
        )

        res = await db.execute(stmt)
        api_key_db = res.scalar_one_or_none()

        if not api_key_db or not SecurityUtils.verify_token(raw_key,api_key_db.key):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or unauthorized access.",
            )       

        return api_key_db
    
    async def roll_apikey(self, user_id: int, key_id: int, db: AsyncSession) -> dict:
        stmt = (
            select(APIKey).
            where(APIKey.user_id == user_id, APIKey.key_id==key_id)
        )

        res = await db.execute(stmt)

        apikey_db = res.scalar_one_or_none()

        if not apikey_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"APIKey {key_id} not found."
            )
        
        generated_token = SecurityUtils.create_api_token()

        if settings.ENVIRONMENT == "prod":
            key = f"sk_live_{generated_token}"
        else:
            key = f"sk_test_{generated_token}"
        
        prefix = key[:10]
        hashed_key = SecurityUtils.get_hashed_token(key[10:])

        apikey_db.prefix = prefix
        apikey_db.key = hashed_key

        await db.commit()

        return {"key_id": apikey_db.key_id, "key": key, "label": apikey_db.label}
