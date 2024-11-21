from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from shared.logger import logging
from shared.utils import parseMessage, generate_needs

"""
@file civilianAgent.py
@description This file contains the CivilianAgent class which is responsible for managing the civilian agents in the simulation.
"""

# Defining the states for the civilian agent
STATE_PEACE = "STATE_PEACE"
STATE_ASK_FOR_HELP = "STATE_ASK_FOR_HELP"
STATE_WAIT_FOR_HELP = "STATE_WAIT_FOR_HELP"
STATE_GOODBYE= "STATE_GOODBYE"


class CivilianBehaviour(FSMBehaviour):
    async def on_start(self):
        logging.info(f"Civilian> Starting at initial state {self.current_state}")

    async def on_end(self):
        logging.info(f"Civilian> finished at state {self.current_state}")
        # await self.agent.stop()

class StatePeace(State):
    async def run(self):
        logging.info("Civilian> Civilian in state peace :)")

        msg = await self.receive(timeout=10)

        if msg:
            type, x_pos, y_pos = parseMessage(msg.body)
            if type == "disaster":
                self.agent.x_position = x_pos
                self.agent.y_position = y_pos
                logging.info(f"Civilian> Help needed at [{x_pos}, {y_pos}]")
                self.set_next_state(STATE_ASK_FOR_HELP)
            else:
                logging.info("No disaster detected, staying in STATE_PEACE.")
                self.set_next_state(STATE_PEACE)
        else:
            logging.info("Civilian> Waiting for message.")
            self.set_next_state(STATE_PEACE)


class StateAskForHelp(State):
    async def run(self):
        logging.info("Civilian> Asking for help")
        x_position = self.agent.x_position
        y_position = self.agent.y_position

        responder_host = await self.agent.manager.getFirstAvailableHost("responder")

        msg = Message(to=str(responder_host))
        msg.set_metadata("performative", "request")
        msg.body = f"{generate_needs()},{x_position},{y_position}"
        await self.send(msg)
        logging.info("Civilian> Help request sent.")
        self.set_next_state(STATE_WAIT_FOR_HELP)


class StateWaitForHelp(State):
    async def run(self):
        logging.info("Civilian> Waiting for help")
        msg = await self.receive(timeout=60)
        if msg and msg.get_metadata("ontology") == "rescued":
            logging.info(f"Civilian> Recieved message = {msg.body}")
            self.set_next_state(STATE_PEACE)
        else:
            self.set_next_state(STATE_WAIT_FOR_HELP)


class StateGoodBye(State):
    async def run(self):
        logging.info("Civilian> recieved help.")
        await self.agent.manager.removeAgentInstance(str(self.agent.jid))


class CivilianAgent(Agent):

    def __init__(self, jid, password, env, manager):
        super().__init__(jid, password)
        self.x_position = 0
        self.y_position = 0
        self.env = env
        self.manager = manager
        self.created_behaviours = {}

    async def getState(self):
        return str(self.created_behaviours["state_machine"].current_state)
    
    async def getPos(self):
        res = (self.x_position, self.y_position)
        return res

    async def setup(self):
  
        behaviour = CivilianBehaviour()
        
        behaviour.add_state(name=STATE_PEACE, state=StatePeace(), initial=True)
        behaviour.add_state(name=STATE_ASK_FOR_HELP, state=StateAskForHelp())
        behaviour.add_state(name=STATE_WAIT_FOR_HELP, state=StateWaitForHelp())
        behaviour.add_state(name=STATE_GOODBYE, state=StateGoodBye())

        behaviour.add_transition(source=STATE_PEACE, dest=STATE_ASK_FOR_HELP)
        behaviour.add_transition(source=STATE_PEACE, dest=STATE_PEACE)
        behaviour.add_transition(source=STATE_ASK_FOR_HELP, dest=STATE_WAIT_FOR_HELP)
        behaviour.add_transition(source=STATE_WAIT_FOR_HELP, dest=STATE_WAIT_FOR_HELP)
        behaviour.add_transition(source=STATE_WAIT_FOR_HELP, dest=STATE_PEACE)

        self.created_behaviours["state_machine"] = behaviour
        self.add_behaviour(behaviour)

        await self.manager.addCivilian(self)
