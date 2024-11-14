# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

from agents.civilianAgent import CivilianAgent
from agents.respondAgent import ResponderAgent
from agents.disasterAgent import DisasterAgent
from environment.environment import Environment

import asyncio
import spade
import time
import random

def randomEmergencyGenerator(env):
    random_iteration = 7
    random_rows = random.sample(range(0, 9), random_iteration)
    random_columns = random.sample(range(0, 9), random_iteration)

    for i in range(random_iteration):
        env.display()
        env.setTile(random_rows[i], random_columns[i], "emergency", "TEST")

        time.sleep(1) 

async def main():
    env = Environment()

    # randomEmergencyGenerator(env)
    responder_agent = ResponderAgent("responder@localhost", "responder", env)
    civilian_agent = CivilianAgent("civilian@localhost", "civilian", env)
    disaster_agent = DisasterAgent("disaster@localhost", "disaster", env)

    await civilian_agent.start(auto_register=True)
    await responder_agent.start(auto_register=True)
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
    
