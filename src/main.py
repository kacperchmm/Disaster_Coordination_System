# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

from agents.civilianAgent import CivilianAgent
from agents.respondAgent import ResponderAgent
from agents.disasterAgent import DisasterAgent
from agents.agentManager import AgentManager
from environment.environment import Environment

import asyncio
import spade
import time
import random

async def initCivilianHosts(env, manager):
    civilian_agents = []
    for i in range(5):
        civilian_agent = CivilianAgent(f"civilian{i}@localhost", "civilian", env, manager)
        civilian_agents.append(civilian_agent)
        await civilian_agent.start(auto_register=True)
        # civilian_agent.web.start(hostname="127.0.0.1", port=10001 + i)  # Ensure the port is unique for each

async def main():
    env = Environment()
    manager = AgentManager(env)

    await initCivilianHosts(env, manager)

    disaster_agent = DisasterAgent("disaster@localhost", "disaster", env, manager)

    await disaster_agent.start(auto_register=True)

    base_settings = {
        "x_position": 4,
        "y_position": 2,
        "emergency_type": "Base",
    }

    # await env.setTile(base_settings)

    # emergency_settings = {
    #     "x_position": 1,
    #     "y_position": 1,
    #     "emergency_type": "Fire",
    #     "food": 32904,
    #     "people": 92313,
    #     "medicine": 154,
    #     "blockage": False,
    #     "communication": True
    # }

    # await env.setTile(emergency_settings)

if __name__ == "__main__":
    spade.run(main())
    
