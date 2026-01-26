
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User
from sqlalchemy.sql import func
from sqlalchemy import select, update
from app.core.jwt_management import create_access_token
from app.core.password_management import PasswordManagement

class UserHelper:
    def __init__(self):
        self.password_management = PasswordManagement()
    
    async def get_or_create(self, user_data: dict, db_session: AsyncSession):
        try:
            google_sub = user_data['sub']  
            result = await db_session.execute(select(User).where(User.id == google_sub))
            user = result.scalar_one_or_none()
            
            if user:
                # Check if user is active
                if not user.is_active:
                    return "DEACTIVATED"
                
                # User exists so its login attempt, update last_login
                user.last_login = func.now()
                await db_session.commit()

                # Creating access token
                data = {"id":user.id,"email":user.email}
                access_token = await create_access_token(data)
                return access_token
            else:
                # Signup attempt, create new user
                new_user = User(
                    id=google_sub,
                    email=user_data['email'],
                    name=user_data['name'],
                    profile_picture=None
                )
                db_session.add(new_user)
                await db_session.commit()
                await db_session.refresh(new_user)

                 # Creating access token
                data = {"id":new_user.id,"email":new_user.email}
                access_token =await create_access_token(data)
                return access_token
        
        except Exception as e:
            print(f"Error in get_or_create: {e}")
            await db_session.rollback()
            return None

    async def get_user(self, user_id: str, db_session: AsyncSession):
        try:
            result = await db_session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def verify_password_generate_token(self,email:str,login_attempt_password:str,db_session:AsyncSession):
        try:
            # Getting the user object (not just hashed_password) to access id and email
            result = await db_session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            # Check if user exists
            if user is None:
                return None
            
            # Verify the password
            if self.password_management.verify_password(login_attempt_password, user.hashed_password):
                # Check if user is active
                if not user.is_active:
                    return "DEACTIVATED"
                
                # Update last_login timestamp
                user.last_login = func.now()
                await db_session.commit()
                
                # Creating the jwt token with user data
                data = {"id": user.id, "email": user.email}
                access_token = await create_access_token(data)
                return access_token
            else:
                # Password verification failed
                return None
        except Exception as e:
            print(f"Error in verify_password_generate_token: {e}")
            await db_session.rollback()
            return None
    
    async def update_user(self, user_id: str, update_data: dict, db_session: AsyncSession):
        try:
            await db_session.execute(
                update(User).where(User.id == user_id).values(**update_data)
            )
            await db_session.commit()
            return await self.get_user(user_id, db_session)
        except Exception as e:
            print(f"Error updating user: {e}")
            await db_session.rollback()
            return None

    async def get_all_users_except_admin(self, admin_id: str, db_session: AsyncSession):
        try:
            result = await db_session.execute(
                select(User).where(User.id != admin_id)
            )
            return result.scalars().all()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []