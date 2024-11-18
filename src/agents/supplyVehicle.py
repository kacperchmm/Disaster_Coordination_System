from .utils import parseMessage, a_star_search, heuristic

from spade import wait_until_finished
from spade.behaviour import CyclicBehaviour
from spade.agent import Agent
from spade.message import Message

from agents.common import parseMessage

import heapq

class SupplyVehicleAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment  # Shared environment reference
        self.manager = manager # Manager of created agent hosts
        self.x_pos = 0  # Current X position of the vehicle
        self.y_pos = 0  # Current Y position of the vehicle
        self.priority_queue = []  # Priority queue for tasks (min-heap)
        self.resources = {
            "fuel": 100,
            "medical_supplies": 50,
            "food": 100,
            "seats": 6
        }

    def get_pos(self):
        """Get the current position of the supply vehicle."""
        return self.x_pos, self.y_pos

    def move_to(self, x, y):
        """Move the vehicle to the specified position."""
        self.x_pos = x
        self.y_pos = y
        print(f"Moved to position: ({self.x_pos}, {self.y_pos})")

    def deliver_resources(self, task):
        """Deliver resources based on the task requirements."""
        # Example logic for delivering resources
        if self.resources["fuel"] >= task["fuel_needed"]:
            self.resources["fuel"] -= task["fuel_needed"]
        if self.resources["medical_supplies"] >= task["medical_supplies_needed"]:
            self.resources["medical_supplies"] -= task["medical_supplies_needed"]
        if self.resources["food"] >= task["food_needed"]:
            self.resources["food"] -= task["food_needed"]
        if self.resources["seats"] >= task["seats_needed"]:
            self.resources["seats"] -= task["seats_needed"]
        print(f"Delivered resources for task: {task}")

    def prioritize_tasks(self):
        """Re-prioritize tasks based on location and fuel resources."""
        def task_priority(task):
            distance = abs(self.x_pos - task["x_position"]) + abs(self.y_pos - task["y_position"])
            fuel_needed = task["fuel_needed"]
            return distance + fuel_needed

        self.priority_queue = sorted(self.priority_queue, key=task_priority)
        print(f"Re-prioritized queue: {self.priority_queue}")

    class ReceivePriorityQueueBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.get_metadata("ontology") == "priority_queue":
                self.agent.priority_queue = eval(msg.body)  # Assume body contains a list
                print(f"Received sorted priority queue: {self.agent.priority_queue}")
                self.agent.prioritize_tasks()

    class SupplyVehicleResponseBehaviour(CyclicBehaviour):
        async def run(self):
            # Process new messages or tasks in the priority queue
            if self.agent.priority_queue:
                task = self.agent.priority_queue.pop(0)
                x_axis, y_axis, emergency_need = task["x_position"], task["y_position"], task["emergency_need"]

                print(f"Processing task: {emergency_need} at ({x_axis}, {y_axis})")

                # Start delivering supplies
                destination = (x_axis, y_axis)
                start_position = self.agent.get_pos()

                # Find the optimal path to the destination
                path = a_star_search(heuristic, start_position, destination, self.agent.environment.board)
                if path:
                    print(f"Path found: {path}")
                    for step in path:
                        self.agent.x_pos, self.agent.y_pos = step
                        print(f"Moving to position: {step}")
                        # Update environment
                        await self.agent.environment.update_position(self.agent.x_pos, self.agent.y_pos)

                # Deliver supplies at the destination
                self.agent.deliver_resources(task)
                tile_changes = {
                    "x_position": x_axis,
                    "y_position": y_axis,
                    "status": "Supplied"
                }
                await self.agent.environment.setTile(tile_changes)
                print(f"Supply delivered to tile: {x_axis}, {y_axis}")

    async def setup(self):
        receive_behaviour = self.ReceivePriorityQueueBehaviour()
        self.add_behaviour(receive_behaviour)

        response_behaviour = self.SupplyVehicleResponseBehaviour()
        self.add_behaviour(response_behaviour)


