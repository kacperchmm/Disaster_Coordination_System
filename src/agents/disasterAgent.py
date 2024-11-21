from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from shared.logger import logging
from shared.utils import generate_needs

import asyncio
import random

"""
@file disasterAgent.py
@description This file contains the DisasterAgent class which is responsible for creating disasters in the simulation.
"""

class DisasterAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.env = environment
        self.manager = manager
        logging.info("TEST 1")


    class NewDisasterBehaviour(CyclicBehaviour):
        def __init__(self, environment):
            super().__init__()
            self.env = environment

        async def sendMessage(self, recipient_id, x_pos, y_pos):
            msg = Message(to=recipient_id)
            msg.set_metadata("performative", "request")
            msg.body = f"disaster,{x_pos},{y_pos}"
            await self.send(msg)
            logging.info(f"Disaster> Message sent to {recipient_id}: disaster at [{x_pos}, {y_pos}]")

        async def run(self):

            x_pos = random.randint(0, self.env.size - 1)
            y_pos = random.randint(0, self.env.size - 1)
            logging.info(f"Creating disaster on [{x_pos}, {y_pos}]")

            emergency_settings = {
                "x_position": x_pos,
                "y_position": y_pos,
                "status": generate_needs(),
                "food": random.randint(1, 1234567),
                "people": random.randint(1, 1234567),
                "medicine": random.randint(1, 1234567),
                "blockage": False,
                "communication": True,
            }

            try:
                changed_tile = await self.env.setTile(emergency_settings)

                if changed_tile:

                    civilian_host = await self.agent.manager.getCivilianJid()
                    if civilian_host is None:
                        raise ValueError("Disaster> No civilian host found.")

                    logging.info(f"Disaster> Setting emergency at [{x_pos}, {y_pos}]")

                    await self.sendMessage(str(civilian_host), x_pos, y_pos)
                else:
                    logging.info("Disaster> Cannot place disaster in Base tile,")

            except Exception as e:
                logging.info(f"ERROR> Could not create disaster or send message: {e}")
                logging.info("Disaster> Retrying in the next cycle...")
                await asyncio.sleep(20)

            delay = random.uniform(1,6)
            await asyncio.sleep(delay)

    async def initBlockage(self):
        for i in range(5):
            x_pos = random.randint(0, self.env.size - 1)
            y_pos = random.randint(0, self.env.size - 1)

            logging.info(f"Disaster> Setting blockage on ({x_pos}, {y_pos})")

            await self.env.setBlockageTile(x_pos, y_pos)

    async def setup(self):
        logging.info("Disaster> Creating disasters.")
        await self.initBlockage()
        disaster_behaviour = self.NewDisasterBehaviour(self.env)
        self.add_behaviour(disaster_behaviour)


