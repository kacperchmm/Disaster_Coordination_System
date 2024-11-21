from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from shared.logger import logging
from shared.utils import parseMessage

import asyncio

"""
@file shelterAgent.py
@description This file contains the ShelterAgent class which is responsible for managing the shelter agents in the simulation.
"""

STATE_REQUEST_RESOURCES = "STATE_REQUEST_RESOURCES"
STATE_RECEIVE_SUPPLIES = "STATE_RECEIVE_SUPPLIES"
STATE_RESCUE = "STATE_RESCUE"
STATE_CLOSE = "STATE_CLOSE"

class ShelterBehaviour(FSMBehaviour):
    async def on_start(self):
        logging.info(f"Shelter> Starting at initial state {self.current_state}")

    async def on_end(self):
        logging.info(f"Shelter> Finished at state {self.current_state}")


class StateRequestResources(State):
    async def run(self):
        logging.info("Shelter> Checking for tasks.")
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("ontology") == "init":
            _, x_pos, y_pos = parseMessage(msg.body)

            await self.agent.setShelter(x_pos, y_pos)

            self.set_next_state(STATE_RECEIVE_SUPPLIES)
        else:
            self.set_next_state(STATE_REQUEST_RESOURCES)

class StateReceiveSupplies(State):
    async def run(self):
        for i in range(3):
            msg = await self.receive(timeout=10)

            if msg:
                need = ""
                logging.info(f"Shelter> Received {msg.body}")
                if msg.get_metadata("ontology") == "food":
                    need = "food"
                if msg.get_metadata("ontology") == "medicine":
                    need =  "medicine"
                if msg and msg.get_metadata("ontology") == "people":
                    need = "beds"

                await self.agent.setInventory(need, int(msg.body))
        
        self.set_next_state(STATE_RESCUE)


class StateRescue(State):
    async def run(self):
        logging.info(f"Shelter> Current inventory: {self.agent.inventory}")
        logging.info(f"Shelter> Current needs: {self.agent.needs}")
        
        await asyncio.sleep(5)

        await self.agent.setRescued()

        shelter_pos = (self.agent.x_pos, self.agent.y_pos)
        civilian_host = await self.agent.manager.getCivilianFromTile(shelter_pos)

        rescue_msg = f"Rescued from {str(self.agent.jid)}"
        logging.info(f"Shelter> sending {rescue_msg} message to {civilian_host}")

        msg_rescued = Message(to=civilian_host)
        msg_rescued.set_metadata("ontology", "rescued")
        msg_rescued.body = rescue_msg
        await self.send(msg_rescued)

        self.set_next_state(STATE_CLOSE)

class StateClose(State):
    async def run(self):
        agent_jid = str(self.agent.jid)

        logging.info(f"Shelter> Closing shelter agent {agent_jid}")

        await self.agent.manager.removeAgentInstance(agent_jid)

class ShelterAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.inventory = {
            "water": 0,
            "food": 0,
            "medicine": 0,
            "beds": 0,
        }
        self.needs = {}
        self.environment = environment
        self.manager = manager
        self.x_pos = -1
        self.y_pos = -1

    async def setRescued(self):
        tile_changes = {
            "x_position": self.x_pos,
            "y_position": self.y_pos,
            "status": "Rescued"
        }

        await self.environment.setTile(tile_changes)

    async def setInventory(self, need, value):
        logging.info(f"Shelter> Setting {need} to {value}.")
        self.inventory[need] = value

    async def setShelter(self, x_position, y_position):
        logging.info(f"Shelter> Set up shelter on ({x_position}, {y_position}).")
        self.x_pos = x_position
        self.y_pos = y_position

        tile_changes = {
            "x_position": x_position,
            "y_position": y_position,
            "status": "Shelter"
        }

        await self.environment.setTile(tile_changes)


    async def setup(self):
        logging.info(f"Shelter> Starting setup")
        behaviour = ShelterBehaviour()

        # Adding states to the FSM
        behaviour.add_state(name=STATE_REQUEST_RESOURCES, state=StateRequestResources(), initial=True)
        behaviour.add_state(name=STATE_RECEIVE_SUPPLIES, state=StateReceiveSupplies())
        behaviour.add_state(name=STATE_RESCUE, state=StateRescue())
        behaviour.add_state(name=STATE_CLOSE, state=StateClose())


        # Define transitions between states
        behaviour.add_transition(source=STATE_REQUEST_RESOURCES, dest=STATE_RECEIVE_SUPPLIES)
        behaviour.add_transition(source=STATE_RECEIVE_SUPPLIES, dest=STATE_RESCUE)
        behaviour.add_transition(source=STATE_REQUEST_RESOURCES, dest=STATE_REQUEST_RESOURCES)
        behaviour.add_transition(source=STATE_RESCUE, dest=STATE_CLOSE)

        # Add behaviour to agent and register
        self.add_behaviour(behaviour)
        await self.manager.addCivilian(self)  # Adjust to a corresponding manager method for shelters
