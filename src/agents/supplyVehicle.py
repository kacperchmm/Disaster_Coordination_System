from spade.agent import Agent
from spade.message import Message
from common import parseMessage

from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour

from spade import wait_until_finished
from simulation import spinningCircle

class SupplyVehicleAgent(Agent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.environment = environment
        self.x_pos = 0
        self.y_pos = 0

    def get_pos(self):
        pass

    class SupplyVehicleResponseBehaviour(CyclicBehaviour):
        def __init__(self, environment):
            super().__init__()

        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for incoming messages
            if msg:
                print(f"Suplly Vehicle received message: {msg.body}")
                emergency_need, x_axis, y_axis = parseMessage(msg.body)

                print(f"Supplying {emergency_need} on tile [{x_axis}, {y_axis}]")



                # spinningCircle.spinner(5)





