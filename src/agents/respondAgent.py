
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


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
    class ResponderResponseBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for incoming messages
            if msg:
                print(f"Responder received message: {msg.body}")
                
                response = Message(to=msg.sender)  
                response.set_metadata("performative", "inform")
                response.body = "Acknowledging request. Help is on the way."
                await self.send(response)

        async def setup(self):
            print("Responder agent on job")
            responder_behaviour = self.ResponderBehaviour()
            self.add_behaviour(responder_behaviour)

