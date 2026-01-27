"""
Script to add sample agents to the database.
Run this script from the project root directory.
"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.helper.agent_helper import AgentHelper

# Agent data: name and email
AGENTS = [
    {"name": "Albert", "email": "sample1@gmail.com"},
    {"name": "Allan", "email": "sample2@gmail.com"},
    {"name": "Carmela", "email": "sample3@gmail.com"},
    {"name": "Jessa", "email": "sample4@gmail.com"},
    {"name": "Danica", "email": "sample5@gmail.com"},
    {"name": "Nino", "email": "sample6@gmail.com"},
    {"name": "Elaine", "email": "sample7@gmail.com"},
]

async def add_sample_agents():
    """Add sample agents to the database."""
    agent_helper = AgentHelper()
    
    async with SessionLocal() as db_session:
        print("Starting to add sample agents...\n")
        
        for agent_data in AGENTS:
            try:
                # Check if agent already exists
                existing_agent = await agent_helper.get_agent_by_email(agent_data["email"], db_session)
                
                if existing_agent:
                    print(f"⚠️  Agent with email {agent_data['email']} already exists. Skipping...")
                    continue
                
                # Create the agent
                new_agent = await agent_helper.create_agent(agent_data, db_session)
                
                if new_agent:
                    print(f"✅ Successfully added agent: {new_agent.name} ({new_agent.email})")
                else:
                    print(f"❌ Failed to add agent: {agent_data['name']} ({agent_data['email']})")
                    
            except Exception as e:
                print(f"❌ Error adding agent {agent_data['name']}: {str(e)}")
        
        print("\n✅ Finished adding sample agents!")

if __name__ == "__main__":
    asyncio.run(add_sample_agents())
