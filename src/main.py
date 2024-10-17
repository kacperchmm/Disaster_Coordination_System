# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

import asyncio
import spade

if __name__ == "__main__":
    # Create agents here ...

    async def main():
    # Create and initialize the environment
    atc_environment = Environment()

    atc_agent = AirTrafficControlAgent("admin@localhost", "admin", atc_environment)

    aircraft_agent = AircraftAgent("user1@localhost", "user", atc_environment)

    await atc_agent.start(auto_register=True)
    await aircraft_agent.start(auto_register=True)


if __name__ == "__main__":
    spade.run(main())
    