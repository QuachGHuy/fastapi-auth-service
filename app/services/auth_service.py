# app/services/auth_service.py
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserLogin
from app.core.security import SecurityUtils
from app.services.user_service import UserService

class AuthService:
    def __init__(self):
        self.user_service = UserService()

    async def login_oauth2(self, db: AsyncSession, form_data: OAuth2PasswordRequestForm = Depends()):
        """
        Handles login request using Form Data (Standard for Swagger UI).
        """
        # 1. Retrive user by username
        user = await self.user_service.get_by_username(username = form_data.username, db=db)

        # 2. Verify user existence and password hash
        if not user or not SecurityUtils.verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 3. Generate JWT Access Token
        access_token = SecurityUtils.create_access_token(data={"sub": str(user.user_id)})
        
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }

    async def login(self, db: AsyncSession, form_data: UserLogin):
        """
        Handles login request using JSON Body (Standard for Frontend/Mobile).
        """
        # 1. Retrive user by username
        user = await self.user_service.get_by_username(username=form_data.username, db=db)

        # 2. Verify user existence and password hash
        if not user or not SecurityUtils.verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 3. Generate JWT Access Token
        access_token = SecurityUtils.create_access_token(data={"sub": str(user.user_id)})

        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }