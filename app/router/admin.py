from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.schema.user_schema import UserResponse, UserStatusUpdate
from app.helper.user_helper import UserHelper
from app.models.user_model import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)]
)

user_helper = UserHelper()

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
