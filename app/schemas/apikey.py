from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class APIKeyCreate(BaseModel): 
    label: str
    description: Optional[str] = None

class APIKeyResponse(BaseModel):
    key: str
    label: str

    model_config = ConfigDict(from_attributes=True)

class APIKeyInfo(BaseModel): 
    key_id: int
    label: str
    description: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class APIKeyUpdate(BaseModel):
    label: Optional[str] = None 
    description: Optional[str] = None
    is_active: Optional[bool] = None