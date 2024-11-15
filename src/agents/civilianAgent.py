from spade.agent import Agent
from spade.message import Message
from agents.utils import parseMessage

from spade.behaviour import OneShotBehaviour

from spade import wait_until_finished
from simulation import spinningCircle

class CivilianAgent(Agent):

    def __init__(self, jid, password, x_axis, y_axis, environment):
        super().__init__(jid, password)
        self.x_position = x_axis
        self.y_position = y_axis
        self.environment = environment
    
    class RequestBehaviour(OneShotBehaviour):
        async def run(self):
            print("Sending help request to responder...")
            msg = Message(to="responder@localhost")  # Responder agent's JID
            msg.set_metadata("performative", "request")
            msg.body = "medicine,1,1"
            await self.send(msg)
            print("Help request sent.")

    async def setup(self):
        print(f"[{self.x_position}, {self.y_position}] Civilian agent starting...")
        help_request_behaviour = self.RequestBehaviour()
        self.add_behaviour(help_request_behaviour)
