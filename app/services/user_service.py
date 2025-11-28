from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import SecurityUtils

class UserService:
    async def get_by_username(self, db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        
        # 1. Check if duplicate email/username
        if await self.get_by_email(db, user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
                )
        
        if await self.get_by_username(db, user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already registered"
                )

        # 2. Get hashed password
        hashed_pw = SecurityUtils.get_hashed_password(user_in.password)

        # 3. Create a new user db
        new_user = User(
            email=user_in.email,
            username=user_in.username,
            password=hashed_pw
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user