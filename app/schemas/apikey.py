from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class APIKeyCreate(BaseModel): 
    label: str

class APIKeyResponse(BaseModel): 
    id: int
    key: str    
    label: str
    is_active: bool
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)