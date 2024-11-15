from spade.agent import Agent
from spade.message import Message
from .utils import parseMessage

from spade.behaviour import OneShotBehaviour, CyclicBehaviour

from spade import wait_until_finished
from simulation import spinningCircle

import heapq


"""
They need to communicate with supply agents to request 
resources and with responder agents to coordinate the 
transportation of civilians to shelters.
"""

# request resource FROM supply
# request coordinates FROM responder
# supply bidding, lowest cost (distance)
# fix msg.body

class ShelterAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    
    class RequestResourceBehaviour(CyclicBehaviour):
        async def run(self):
            print("Sending request to Supply Agent...")
            supply_msg = Message(to="supplyagent@localhost")
            supply_msg.set_metadata("ontology", "resource_request")
            supply_msg.set_metadata("performative", "request")
            supply_msg.set_metadata("language", "English")
            supply_msg.body = ""  # Adjust with specific needs
            await self.send(supply_msg)

            print("Resource request sent to Supply Agent.")

            # Wait for a response
            response = await self.receive(timeout=10)
            if response:
                print(f"Received resources response: {response.body}")
                # Process the response or update inventory as needed

    class CoordinateTransportBehaviour(CyclicBehaviour):
        async def run(self):
            # Prepare and send a request to the responder agent for transport coordination
            responder_msg = Message(to="responderagent@localhost")
            responder_msg.set_metadata("ontology", "transport_request")
            responder_msg.set_metadata("performative", "request")
            responder_msg.set_metadata("language", "English")
            responder_msg.body = "" 

            await self.send(responder_msg)
            print("Transport request sent to Responder Agent.")

            # Wait for an update or confirmation from responder agent
            confirmation = await self.receive(timeout=10)
            if confirmation:
                print(f"Transport coordination confirmed: {confirmation.body}")
    
    def update_shelter_status():
        # number need transport
        # resources
        pass

    
    async def setup(self):
        pass
