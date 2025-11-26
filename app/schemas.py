from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=8, max_length=50)

class UserLogin(BaseModel):
    username: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=8, max_length=50)

class UserResponse(BaseModel):
    email: EmailStr
    user_id: int
    username: str
    points: int
    rank: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)