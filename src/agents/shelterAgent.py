from spade.agent import Agent
from spade.message import Message
from spade.behaviour import OneShotBehaviour, CyclicBehaviour

from ..shared.utils import parseMessage, fill_resource_inventory, update_resource_inventory
from ..shared.logger import logging


"""
They need to communicate with supply agents to request 
resources and with responder agents to coordinate the 
transportation of civilians to shelters.
"""

# request resource FROM supply
# request coordinates FROM responder (the queue)
# supply bidding, lowest cost (distance)
# fix msg.body

class ShelterAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.inventory = {
            "water": 100,  # Available units
            "food": 50,
            "medicine": 20,
            "beds": 10,    # Available capacity
            }

        self.needs = {
            "water": 0,  # Additional units needed
            "food": 0,
            "medicine": 0,
            "beds": 0,
            }

    
    class RequestResourceBehaviour(CyclicBehaviour):
        async def run(self):
            logging.info("Sending request to Supply Agent...")
            supply_msg = Message(to="supplyagent@localhost")
            supply_msg.set_metadata("ontology", "resource_request")
            supply_msg.set_metadata("performative", "request")
            supply_msg.set_metadata("language", "English")
            supply_msg.body = ""  # Adjust with specific needs
            await self.send(supply_msg)

            logging.info("Resource request sent to Supply Agent.")

            # Wait for a response
            response = await self.receive(timeout=10)
            if response:
                logging.info(f"Received resources response: {response.body}")
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
            logging.info("Transport request sent to Responder Agent.")

            # Wait for an update or confirmation from responder agent
            confirmation = await self.receive(timeout=10)
            if confirmation:
                logging.info(f"Transport coordination confirmed: {confirmation.body}")
        
    class InventoryCheckBehaviour(CyclicBehaviour):
        async def run(self):
            for item, available in self.agent.inventory.items():
                if available < 10:  # Threshold
                    self.agent.needs[item] = 10 - available
            
            if self.agent.needs:
                request_msg = Message(to="vehicle0@localhost")
                request_msg.set_metadata("ontology", "resource_request")
                request_msg.set_metadata("performative", "request")
                request_msg.body = str(self.agent.needs)  # Send needs as JSON
                await self.send(request_msg)
                logging.info(f"Requested resources: {self.agent.needs}")
    
    class ReceiveSupplyBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("ontology") == "resource_response":
                delivered_resources = eval(msg.body)  # Assume body contains a dictionary
                for item, quantity in delivered_resources.items():
                    fill_resource_inventory(self.agent.inventory, item, quantity)


    class ReportInventoryBehaviour(CyclicBehaviour):
        async def run(self):
            logging.info(f"Current Inventory for {self.agent.name}: {self.agent.inventory}")
            logging.info(f"Current Needs for {self.agent.name}: {self.agent.needs}")

    
    async def setup(self):
        inventory_check_behaviour = self.InventoryCheckBehaviour()
        request_supply_behaviour = self.RequestResourceBehaviour()
        recieve_supply_behaviour = self.ReceiveSupplyBehaviour()
        report_inventory_behaviour = self.ReportInventoryBehaviour()
        
        self.add_behaviour(inventory_check_behaviour())
        self.add_behaviour(request_supply_behaviour())
        self.add_behaviour(recieve_supply_behaviour())
        self.add_behaviour(report_inventory_behaviour())
