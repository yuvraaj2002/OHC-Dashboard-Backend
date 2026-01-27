from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import uuid

class AgentResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    @field_validator('is_active', mode='before')
    @classmethod
    def validate_is_active(cls, v):
        return bool(v) if v is not None else True
    
    class Config:
        from_attributes = True

class AgentCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class AgentUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
