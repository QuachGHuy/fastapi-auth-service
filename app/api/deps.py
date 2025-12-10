from datetime import datetime, timezone

from fastapi import Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.db.session import get_db
from app.core.config import settings

from app.models.user import User 
from app.models.apikey import APIKey

from app.services.user_service import UserService 
from app.services.api_service import APIService

# Define the scheme so Swagger UI knows how to send the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/form")


user_service = UserService()

async def get_current_user(
        token: str = Security(oauth2_scheme), 
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


apikey_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)
api_service = APIService()

async def validate_apikey(
        key_sent: str = Security(apikey_header_scheme),
        db: AsyncSession = Depends(get_db)
    ) -> APIKey:
    """
    Dependency to validate and retrieve the APIKey.
    """

    # 1. Check if key_sent is empty
    if not key_sent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed: API Key is missing.",
        )
    
    # 2. Verify and retrive apikey
    api_key_db = await api_service.verify_key_and_get_key(
        key=key_sent,
        db=db
    )

    # 3. Check apikey status
    if not api_key_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key is inactive/revoked.",  
        )
    
    api_key_db.last_used_at = datetime.now(timezone.utc)
    await db.commit()

    return api_key_db