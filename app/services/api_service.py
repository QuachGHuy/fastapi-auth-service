from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.apikey import APIKey
from app.core.security import SecurityUtils
from app.core.config import settings

class APIService:
    async def create_apikey(self, db: AsyncSession, label: str, user_id: int):
        generated_token = SecurityUtils.create_api_token()

        if settings.ENVIRONMENT == "prod":
            api_key = f"sk_live_{generated_token}"
        else:
            api_key = f"sk_test_{generated_token}"
        
        api_key_db = APIKey(
            label=label,
            user_id=user_id,
            key=api_key,
            is_active=True,
        )

        db.add(api_key_db)
        await db.commit()
        await db.refresh(api_key_db)

        return api_key_db
    
    async def get_apikey(self, db: AsyncSession, user_id: int):
        result =  await db.execute(select(APIKey).where(APIKey.user_id==user_id))
        return result.scalar_one_or_none()
    
    async def delete_apikey(self, db: AsyncSession, label: str, user_id: int):
        result = await db.execute(select(APIKey).where(APIKey.user_id==user_id , APIKey.label==label))
        apikey_db = result.scalar_one_or_none()


        if not apikey_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API Key with label '{label}' not found."
            )
        

        await db.delete(apikey_db)
        await db.commit()

        return {"message": "API key deleted successfully"}
