import secrets
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

from app.core.config import settings

class SecurityUtils:
    
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    @staticmethod
    def get_hashed_password(plain_password: str) -> str:
        return SecurityUtils.pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password :str) -> bool:
        return SecurityUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Generate a new JSON Web Token (JWT) for Authentication.
        """
        # 1. Copy data to avoid side effects
        to_encode = data.copy()

        # 2. Calculate expiration time (Always use UTC)
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        # 3. Sign and Encode
        encoded_jwt = jwt.encode(
            claims=to_encode, 
            key=settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def create_api_token(length: int = 32) -> str:
        token = secrets.token_urlsafe(length)
        return token
