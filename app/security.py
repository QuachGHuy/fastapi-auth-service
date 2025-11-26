from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from jose import jwt

from app.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_hashed_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """
    Generate a new JSON Web Token (JWT) for Authentication.

    **Process:**
    1. Copy Data: Creates a shallow copy of the input `data` to avoid mutating 
       the original dictionary (side-effect prevention).
    2. Set Expiration: the current UTC time + the configured duration (ACCESS_TOKEN_EXPIRE_MINUTES).
    3. Encode: Signs the payload using the "SECRET_KEY" and "ALGORITHM".

    - **data**: A dictionary containing the token payload ({"sub": "user_id"}).
    - **return**: The encoded JWT as a string.
    """
    # 1. Copy data to avoid side effects
    to_encode = data.copy()

    # 2. Calculate expiration time (Always use UTC) & Add 'exp' claim
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # 3. Sign and Encode
    encoded_jwt = jwt.encode(
        claims=to_encode, 
        key=settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM)
    
    return encoded_jwt


