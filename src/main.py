# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

from agents.civilianAgent import CivilianAgent
from agents.respondAgent import ResponderAgent
from environment.environment import Environment

import asyncio
import spade
import time
import random

async def main():
    # Create and initiali               ze the environment
    # remember to pass an environment to agents
    # atc_environment = Environment()

    civilian_agent = CivilianAgent("civilian@localhost", "civilian")

    responder_agent = ResponderAgent("responder@localhost", "responder")

    await civilian_agent.start(auto_register=True)
    await responder_agent.start(auto_register=True)


if __name__ == "__main__":
    env = Environment()
    random_iteration = 7
    random_rows = random.sample(range(0, 9), random_iteration)
    random_columns = random.sample(range(0, 9), random_iteration)

    for i in range(random_iteration):
        env.display()
        env.setTile(random_rows[i], random_columns[i], "emergency", "TEST")

        time.sleep(1) 

    spade.run(main())
    