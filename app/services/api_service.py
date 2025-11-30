from sqlalchemy.ext.asyncio import AsyncSession 

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