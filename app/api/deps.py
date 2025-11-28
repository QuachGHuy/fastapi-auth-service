from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.db.session import get_db
from app.core.config import settings

from app.models.user import User 

from app.services.user_service import UserService 

# Define the scheme so Swagger UI knows how to send the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/form")


user_service = UserService()

async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: AsyncSession = Depends(get_db)
        ) -> User:
    """
    Dependency to authenticate and retrieve the current user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Decode the token
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # 2. Get the Subject (User ID)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
        
        # 3. Convert to Integer
        user_id = int(user_id_str)

    except (JWTError, ValueError): 
        raise credentials_exception 

    user = await user_service.get_by_user_id(db=db, user_id=user_id)
    
    if not user: 
        raise credentials_exception
    
    return user