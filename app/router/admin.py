from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.schema.user_schema import UserResponse, UserStatusUpdate
from app.schema.agent_schema import AgentResponse, AgentCreate, AgentUpdate
from app.helper.user_helper import UserHelper
from app.helper.agent_helper import AgentHelper
from app.models.user_model import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)]
)

user_helper = UserHelper()
agent_helper = AgentHelper()

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all users except the current admin.
    """
    users = await user_helper.get_all_users_except_admin(current_admin.id, db)
    return users

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_status(
    user_id: str,
    status_update: UserStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Activate or deactivate a user.
    """
    updated_user = await user_helper.update_user(user_id, status_update.model_dump(), db)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or update failed"
        )
    return updated_user

# Agent endpoints
@router.get("/agents", response_model=List[AgentResponse])
async def get_all_agents(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all agents. Admin only.
    """
    agents = await agent_helper.get_all_agents(db)
    return agents

@router.post("/agents", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new agent. Admin only.
    """
    new_agent = await agent_helper.create_agent(agent_data.model_dump(), db)
    if not new_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agent with this email already exists or creation failed"
        )
    return new_agent

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an agent's name or email. Admin only.
    """
    updated_agent = await agent_helper.update_agent(agent_id, agent_update.model_dump(), db)
    if not updated_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found, email already exists, or update failed"
        )
    return updated_agent
