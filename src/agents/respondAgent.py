from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from shared.logger import logging
from shared.utils import parseMessage

"""
@file respondAgent.py
@description This file contains the ResponderAgent class which is responsible for managing the responder agents in the simulation.
"""

# Defining the states for the responder agent
STATE_RECEIVE_CIVILIAN_REQUEST = "STATE_RECEIVE_CIVILIAN_REQUEST"
STATE_SEND_PRIORITY_QUEUE = "STATE_SEND_PRIORITY_QUEUE"
STATE_PRIORITIZE_REQUESTS = "STATE_PRIORITIZE_REQUESTS"


class ResponderBehaviour(FSMBehaviour):
    async def on_start(self):
        logging.info(f"Responder> Starting at initial state {self.current_state}")

    async def on_end(self):
        logging.info(f"Responder> finished at state {self.current_state}")


class StateReceiveCivilianRequest(State):
    async def run(self):
        logging.info("Responder> Waiting for civilian requests...")
        timeout = 0
        self.agent.civilian_requests = []
        while len(self.agent.civilian_requests) < 3:
            msg = await self.receive(timeout=10)
            if msg:
                data = parseMessage(msg.body)
                logging.info(f"Responder> Received a request: {data}")
                self.agent.civilian_requests.append(data)
            else:
                timeout += 1

            if timeout > 3:
                break

        self.set_next_state(STATE_PRIORITIZE_REQUESTS)

class StatePrioritizeRequests(State):
    async def run(self):
        logging.info("Responder> Prioritizing requests...")
        # Custom prioritization logic
        def priority_key(request):
            logging.info(f"DEBUG> Request = {request}")
            priority = 0
            if request[0] == "medical":
                priority += 4
            if request[0] == "rescue":
                priority += 3
            if request[0] == "shelter":
                priority += 2
            if request[0] == "food":
                priority += 1
            return priority

        self.agent.civilian_requests.sort(key=priority_key, reverse=True)
        logging.info(f"Responder> Prioritized requests: {self.agent.civilian_requests}")
        self.set_next_state(STATE_SEND_PRIORITY_QUEUE)

class StateSendPriorityQueue(State):
    async def run(self):
        logging.info("Responder> Sending priority queue to supply vehicles...")

        vehicle_host = await self.agent.manager.getFirstAvailableHost("vehicle")

        # Send the number of messages first
        num_messages = len(self.agent.civilian_requests)
        init_msg = Message(to=vehicle_host)  # Replace with actual JID
        init_msg.set_metadata("ontology", "init")
        init_msg.body = f"init,{num_messages},0"
        await self.send(init_msg)
        logging.info(f"Responder> Sent init message: {init_msg.body}")

        # Create and send the prioritized messages one by one
        for request in self.agent.civilian_requests:
            logging.info(f"DEBUG> Responder request is {request}")
            help_msg = f"help,{request[1]},{request[2]}"
            msg = Message(to=vehicle_host)  # Replace with actual JID
            msg.set_metadata("ontology", "priority_queue")
            msg.body = help_msg
            await self.send(msg)
            logging.info("Receiver> Message sent do vehicle")
        else:
            logging.info(f"Responder> queue empty")
        
        # After sending, transition to the receive civilian request state again
        self.set_next_state(STATE_RECEIVE_CIVILIAN_REQUEST)

class ResponderAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment  # Shared environment reference
        self.priority_queue = []  # Store tasks prioritized by urgency
        self.manager = manager
        self.created_behaviours = {}
    
    async def getState(self):
        return str(self.created_behaviours["state_machine"].current_state)

    async def setup(self):
        logging.info("Responder> Starting...")

        fsm = ResponderBehaviour()

        fsm.add_state(name=STATE_RECEIVE_CIVILIAN_REQUEST, state=StateReceiveCivilianRequest(), initial=True)
        fsm.add_state(name=STATE_PRIORITIZE_REQUESTS, state=StatePrioritizeRequests())
        fsm.add_state(name=STATE_SEND_PRIORITY_QUEUE, state=StateSendPriorityQueue())

        fsm.add_transition(source=STATE_RECEIVE_CIVILIAN_REQUEST, dest=STATE_PRIORITIZE_REQUESTS)
        fsm.add_transition(source=STATE_PRIORITIZE_REQUESTS, dest=STATE_SEND_PRIORITY_QUEUE)
        fsm.add_transition(source=STATE_SEND_PRIORITY_QUEUE, dest=STATE_RECEIVE_CIVILIAN_REQUEST)

        self.created_behaviours["state_machine"] = fsm
        self.add_behaviour(fsm) 