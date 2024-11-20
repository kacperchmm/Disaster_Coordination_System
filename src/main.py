from agents.civilianAgent import CivilianAgent
from agents.disasterAgent import DisasterAgent
from agents.agentManager import AgentManager
from environment.environment import Environment

import spade

"""
@file main.py
@description This file contains the main function which is responsible for starting the simulation.
"""

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
        "status": "Base",
    }

    await env.setTile(base_settings)

if __name__ == "__main__":
    spade.run(main())
    
