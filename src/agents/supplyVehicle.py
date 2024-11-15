from .utils import parseMessage, a_star_search, heuristic

from spade.agent import Agent
from spade.message import Message

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
        return self.x_pos, self.y_pos

    class SupplyVehicleResponseBehaviour(CyclicBehaviour):
        def __init__(self, environment):
            super().__init__()

        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for incoming messages
            if msg:
                print(f"Suplly Vehicle received message: {msg.body}")
                emergency_need, x_axis, y_axis = parseMessage(msg.body)
                destination = (x_axis, y_axis)

                print(f"Supplying {emergency_need} on tile [{x_axis}, {y_axis}]")
                
                self.x_pos = x_axis
                self.y_pos = y_axis

                print(f"Supply vehicle moving to position: ({self.x_pos}, {self.y_pos})")

                start_position = self.get_pos()
                path = a_star_search(heuristic, start_position, destination, self.environment.board)

                if path:
                    print(f"Path found: {path}")
                    for step in path:
                        self.x_pos, self.y_pos = step
                        print(f"Moving to position: {step}")
                        # update env
                        await self.environment.update_position(self.x_pos, self.y_pos)

                tile_changes = {
                    "x_position": x_axis,
                    "y_position": y_axis,
                }
                await self.environment.setTile(tile_changes)
                print("Supply delivered.")


                # spinningCircle.spinner(5)


# cost = path
# sv 1, cost 3
# sv 2, cost 2
# sv 3, cost,6

# shelter 1 gives bives bid to sv 2


