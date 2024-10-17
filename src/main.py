# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

from agents.civilianAgent import CivilianAgent
from agents.respondAgent import ResponderAgent

import asyncio
import spade

async def main():
    # Create and initiali               ze the environment
    # remember to pass an environment to agents
    # atc_environment = Environment()

    civilian_agent = CivilianAgent("civilian@localhost", "civilian")

    responder_agent = ResponderAgent("responder@localhost", "responder")

    await civilian_agent.start(auto_register=True)
    await responder_agent.start(auto_register=True)


if __name__ == "__main__":
    spade.run(main())
    