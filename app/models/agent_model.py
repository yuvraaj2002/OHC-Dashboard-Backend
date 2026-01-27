from sqlalchemy import Column, String, DateTime, Boolean
from app.core.database import Base
from sqlalchemy.sql import func

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String(255), primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
