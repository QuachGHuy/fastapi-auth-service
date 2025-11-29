from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.apikey import APIKey
from app.schemas.apikey import APIKeyCreate
from app.core.security import SecurityUtils
from app.core.config import Settings

async def create_api_key(
        db: AsyncSession, 
        user_id :int,
        api_label : APIKeyCreate):
    
    if Settings.ENVIRONMENT == "prod":
        api_key = f"sk_live_{SecurityUtils.create_api_key()}"
    else:
        api_key = f"sk_test_{SecurityUtils.create_api_key()}"

    db_api_key = APIKey(
        key=api_key,           # Chuỗi sk_...
        label=api_label.label,     # Tên gợi nhớ user đặt
        user_id=user_id,         # Gắn với user đang đăng nhập
        is_active=True
    )

    db.add(db_api_key)
    await db.commit()
    await db.refresh(db_api_key)

    return db_api_key

