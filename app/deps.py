from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.database import get_db
from app.schemas import UserLogin
from app.config import settings
from app.crud import get_user_by_user_id

# Define the scheme so Swagger UI knows how to send the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/form")

async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: AsyncSession = Depends(get_db)
        ):
    """
    Dependency to authenticate and retrieve the current user.

    **Process**
    1. Extract: Pulls the Bearer Token from the "Authorization" header.
    2. Decode: Validates the token signature and expiration using "SECRET_KEY".
    3. Parse: Extracts the "user_id" from the "sub" (subject) claim.
    4. Verify: Checks if the user actually exists in the database.

    **Raises:**
    - "HTTP 401 Unauthorized": If the token is invalid, expired, malformed, 
      or if the user is not found in the database.

    **Returns:**
    - "User": The user object corresponding to the token.
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
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        
        # 3. Convert to Integer (Critical Step)
        # If 'sub' is not a number (e.g. hacked token), this raises ValueError
        user_id = int(user_id)

    except JWTError: # <--- NOTE: Catch ValueError to prevent 500 Error
        raise credentials_exception 
    
    # 4. Check if the user actually exists 
    user = await get_user_by_user_id(user_id = user_id, db=db)
    
    if not user: 
        raise credentials_exception
    
    return user
    
