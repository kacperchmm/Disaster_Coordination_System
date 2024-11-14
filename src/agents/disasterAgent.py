from spade.agent import Agent
from spade.message import Message
from spade.behaviour import OneShotBehaviour

from agents.common import parseMessage

import asyncio
import random

class DisasterAgent(Agent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.env = environment

    class NewDisasterBehaviour(OneShotBehaviour):
        def __init__(self, environment):
            super().__init__()
            self.env = environment

        async def chooseCivilianHost(self):
            return "civilian@localhost"

        async def sendMessage(self, recipient_id):
            print(f"Agent {self.agent_id} sends message to Agent {recipient_id} at {self.position}")

        async def run(self):
            for _ in range(2):
                x_pos = random.randint(0, self.env.size - 1)
                y_pos = random.randint(0, self.env.size - 1)

                print(f"Creating disaster on [{x_pos}, {y_pos}]")
                emergency_settings = {
                    "x_position": x_pos,
                    "y_position": y_pos,
                    "emergency_type": "Fire",
                    "food": 32904,
                    "people": 92313,
                    "medicine": 154,
                    "blockage": False,
                    "communication": True
                }

                await self.env.setTile(emergency_settings)
                
                civilian_host = await self.chooseCivilianHost()
                msg = Message(to=str(civilian_host))
                msg.set_metadata("perfomative", "request")
                msg.body = f"disaster,{x_pos},{y_pos}"
                await self.send(msg)

                print(f"Disaster> New {emergency_settings['emergency_type']} on [{x_pos}, {y_pos}] ")


                delay = random.uniform(1, 5)
                # await asyncio.sleep(6)
        

    async def setup(self):
        print("Disaster> Creating disasters.")
        disaster_behaviour = self.NewDisasterBehaviour(self.env)
        self.add_behaviour(disaster_behaviour)


