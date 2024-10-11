
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade import wait_until_finished

class CivilianAgent(Agent):

    class RequestBehaviour(OneShotBehaviour):
        async def run(self):
            print("Sending help request to responder...")
            msg = Message(to="responder@localhost")  # Responder agent's JID
            msg.set_metadata("performative", "request")
            msg.body = "Need rescue and medical aid at location X"
            await self.send(msg)
            print("Help request sent.")

    async def setup(self):
        print("Civilian agent starting...")
        help_request_behaviour = self.RequestBehaviour()
        self.add_behaviour(help_request_behaviour)
        


