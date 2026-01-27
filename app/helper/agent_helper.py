import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.agent_model import Agent
from sqlalchemy import select, update

class AgentHelper:
    async def get_all_agents(self, db_session: AsyncSession):
        """Get all agents from the database."""
        try:
            result = await db_session.execute(select(Agent))
            return result.scalars().all()
        except Exception as e:
            print(f"Error getting all agents: {e}")
            return []

    async def get_agent(self, agent_id: str, db_session: AsyncSession):
        """Get a single agent by ID."""
        try:
            result = await db_session.execute(select(Agent).where(Agent.id == agent_id))
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting agent: {e}")
            return None

    async def get_agent_by_email(self, email: str, db_session: AsyncSession):
        """Get an agent by email."""
        try:
            result = await db_session.execute(select(Agent).where(Agent.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting agent by email: {e}")
            return None

    async def create_agent(self, agent_data: dict, db_session: AsyncSession):
        """Create a new agent."""
        try:
            # Check if agent with this email already exists
            existing_agent = await self.get_agent_by_email(agent_data['email'], db_session)
            if existing_agent:
                return None  # Agent with this email already exists
            
            # Generate a unique ID for the agent
            agent_id = str(uuid.uuid4())
            
            new_agent = Agent(
                id=agent_id,
                email=agent_data['email'],
                name=agent_data.get('name')
            )
            db_session.add(new_agent)
            await db_session.commit()
            await db_session.refresh(new_agent)
            return new_agent
        except Exception as e:
            print(f"Error creating agent: {e}")
            await db_session.rollback()
            return None

    async def update_agent(self, agent_id: str, update_data: dict, db_session: AsyncSession):
        """Update an agent's information."""
        try:
            # Check if email is being updated and if it already exists
            if 'email' in update_data and update_data['email']:
                existing_agent = await self.get_agent_by_email(update_data['email'], db_session)
                if existing_agent and existing_agent.id != agent_id:
                    return None  # Email already exists for another agent
            
            # Remove None values from update_data
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not update_data:
                # No valid fields to update, just return the agent
                return await self.get_agent(agent_id, db_session)
            
            await db_session.execute(
                update(Agent).where(Agent.id == agent_id).values(**update_data)
            )
            await db_session.commit()
            return await self.get_agent(agent_id, db_session)
        except Exception as e:
            print(f"Error updating agent: {e}")
            await db_session.rollback()
            return None
