from .utils import parseMessage

from spade import wait_until_finished
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from shared.spinningCircle import spinner
from agents.common import parseMessage

import asyncio
import heapq

class ResponderAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment  # Shared environment reference
        self.priority_queue = []  # Store tasks prioritized by urgency
        self.environment = environment
        self.manager = manager

    async def send_priority_queue(self):
        if self.priority_queue:
            sorted_queue = sorted(self.priority_queue, key=lambda x: x['priority'])
            msg = Message(to="supplyvehicleagent@domain")  # Replace with actual JID
            msg.set_metadata("ontology", "priority_queue")
            msg.body = str(sorted_queue)
            await self.send(msg)
            print(f"Sent sorted priority queue: {sorted_queue}")

    class ReceiveCivilianRequests(CyclicBehaviour):
        async def run(self):
            # Wait for a message from civilian agents
            msg = await self.receive(timeout=10)
            if msg:
                # Parse the incoming message
                try:
                    data = parseMessage(msg.body)
                    print(f"Responder received a request: {data}")
                    
                    # Add the request to the priority queue
                    self.agent.priority_queue.append((data["priority"], data))
                    self.agent.priority_queue.sort(reverse=True)  # Sort by priority
                    
                except Exception as exc:
                    print(f"Error parsing message: {exc}")

    class ResponderResponseBehaviour(CyclicBehaviour):
        def __init__(self, environment):
            super().__init__()
            self.environment = environment

        async def run(self):
            # Process tasks from the priority queue
            if self.agent.priority_queue:

                _, task = self.agent.priority_queue.pop(0)
                print(f"Responder handling task: {task}")

                # Extract task details
                emergency_need = task.get("emergency_need", "unknown")
                x_axis = task.get("x_position", 0)
                y_axis = task.get("y_position", 0)

                msg = Message(to="supplyvehicleagent@domain")  # Replace with actual JID
                msg.set_metadata("ontology", "priority_queue")
                msg.body = str(self.agent.priority_queue)
                await self.send(msg)
                print(f"Sent sorted priority queue: {self.agent.priority_queue}")

                # Update the environment (mark the task location as safe)
                tile_changes = {
                    "x_position": x_axis,
                    "y_position": y_axis,
                    "emergency_type": "Safe"
                }

                await self.environment.setTile(tile_changes)
                print(f"Updated environment tile: {tile_changes}")

    class SendPriorityQueueBehaviour(CyclicBehaviour):
        async def run(self):
            await self.agent.send_priority_queue()

    async def setup(self):
        print("Responder agent starting...")

        # Add the behavior to receive civilian requests
        receive_civilian_requests = self.ReceiveCivilianRequests()
        self.add_behaviour(receive_civilian_requests)

        b = self.SendPriorityQueueBehaviour()
        self.add_behaviour(b)
        
        # Add the behavior to process and respond to tasks
        responder_response = self.ResponderResponseBehaviour(self.environment)
        self.add_behaviour(responder_response)

