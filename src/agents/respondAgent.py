from spade.agent import Agent
from spade.message import Message
from agents.common import parseMessage

from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour

from spade import wait_until_finished
from shared.spinningCircle import spinner

import asyncio

"""
The attributes that can be set in a template are:

to: the jid string of the receiver of the message.
sender the jid string of the sender of the message.
body: the body of the message.
thread: the thread id of the conversation.
metadata: a (key, value) dictionary of strings to define metadata of the message. This is useful, 
for example, to include FIPA attributes like ontology, performative, language, etc.

Templates is the method used by SPADE to dispatch received messages to the behaviour that is waiting 
for that message. When adding a behaviour you can set a template for that behaviour, 
which allows the agent to deliver a message received by the agent to that registered behaviour. 
A Template instance has the same attributes of a Message and all the attributes defined 
in the template must be equal in the message for this to match.
"""

class ResponderAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment
        self.manager = manager

    class ResponderResponseBehaviour(CyclicBehaviour):
        def __init__(self, environment):
            super().__init__()
            self.environment = environment

        async def run(self):
            msg = await self.receive(timeout=10)
            print("Responder> Waiting for message")
            if msg:
                print(f"Responder> Received message: {msg.body}")
                emergency_need, x_axis, y_axis = parseMessage(msg.body)

                print(f"Responder> Dispatching {emergency_need} on tile [{x_axis}, {y_axis}]")

                tile_changes = {
                    "x_position": x_axis,
                    "y_position": y_axis,
                    "emergency_type": "Safe"
                }

                # spinner(5)

                await asyncio.sleep(10)

                await self.environment.setTile(tile_changes)

                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "request")
                response.body = f"Sending help"
                await self.send(response)

                await self.agent.manager.removeAgentInstance(str(self.agent.  jid))

    async def setup(self):
        print("Responder> Agent sarting...")
        responder_behaviour = self.ResponderResponseBehaviour(self.environment)
        self.add_behaviour(responder_behaviour)

