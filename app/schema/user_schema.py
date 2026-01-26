from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    last_login: Optional[datetime] = None
    is_admin: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    @field_validator('is_admin', mode='before')
    @classmethod
    def validate_is_admin(cls, v):
        return bool(v) if v is not None else False

    @field_validator('is_active', mode='before')
    @classmethod
    def validate_is_active(cls, v):
        return bool(v) if v is not None else True
    
    class Config:
        from_attributes = True

class UserStatusUpdate(BaseModel):
    is_active: bool