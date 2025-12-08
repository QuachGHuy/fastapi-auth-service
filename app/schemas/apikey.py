from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class APIKeyCreate(BaseModel): 
    label: str
    description: Optional[str] = None

class APIKeyResponse(BaseModel): 
    key_id: int
    key: str
    label: str
    description: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class APIKeyUpdate(BaseModel):
    label: Optional[str] = None 
    description: Optional[str] = None
    is_active: Optional[bool] = None