from spade import wait_until_finished
from spade.behaviour import CyclicBehaviour, FSMBehaviour, State
from spade.agent import Agent
from spade.message import Message

from shared.utils import a_star_search, heuristic, parseMessage

import heapq
import asyncio
import json

STATE_IDLE = "STATE_IDLE"
STATE_RECEIVE_TASKS = "STATE_RECEIVE_TASKS"
STATE_NAVIGATE = "STATE_NAVIGATE"
STATE_DELIVER = "STATE_DELIVER"
STATE_PEACE= "STATE_PEACE"

class StateIdle(State):
    async def run(self):
        print("Vehicle> In idle state.")
        self.set_next_state(STATE_RECEIVE_TASKS)


class StateReceiveTasks(State):
    async def run(self):
        print("Vehicle> Checking for tasks.")
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("ontology") == "priority_queue":
            received_msg = parseMessage(msg.body)
            init_message = received_msg[1]

            for i in range(init_message):
                msg = await self.receive(timeout=10)
                if msg:
                    task = parseMessage(msg.body)
                    self.agent.priority_queue.append(task)
                else:
                    print("Vehicle> No tasks received.")
                    self.set_next_state(STATE_IDLE)
                    return

            print(f"Vehicle> Received {init_message} tasks.")
        else:
            print("Vehicle> No tasks received, staying idle.")
            self.set_next_state(STATE_IDLE)

class StateNavigate(State):
    async def run(self):
        print("Vehicle> Navigating to task location.")
        if self.agent.priority_queue:
            task = self.agent.prioritize_tasks()
            task = self.agent.priority_queue[0]  # Peek at the next task
            start_position = self.agent.get_pos()
            destination = (task["x_position"], task["y_position"])

            # Find the optimal path
            path = a_star_search(heuristic, start_position, destination, self.agent.environment.board)
            if path:
                for step in path:
                    print(f"Vehicle> Moving to position: {step}")
                    self.agent.x_pos, self.agent.y_pos = step
                    await self.agent.environment.updatePositionVehicle(self.agent.x_pos, self.agent.y_pos)
                    await asyncio.sleep(1)
                print("Vehicle> Reached destination.")
                self.set_next_state(STATE_DELIVER)
            else:
                print("Vehicle> No path found, returning to idle.")
                self.set_next_state(STATE_IDLE)
        else:
            self.set_next_state(STATE_IDLE)

class StateDeliver(State):
    async def run(self):
        print("Vehicle> Delivering supplies.")
        if self.agent.priority_queue:
            task = self.agent.prioritize_tasks()
            task = self.agent.priority_queue.pop(0)  # Dequeue the task
            self.agent.deliver_resources(task)
            tile_changes = {
                "x_position": task["x_position"],
                "y_position": task["y_position"],
                "status": "Supplied"
            }
            await self.agent.environment.setTile(tile_changes)
            print(f"Vehicle> Supplies delivered to ({tile_changes['x_position']}, {tile_changes['y_position']}).")
        self.set_next_state(STATE_IDLE)


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
    
    def read_init_message(self, msg):
        """Read the initial message and update the number of expected messages."""
        message = parseMessage(msg.body)
        num_messages = message[1]
        return num_messages
    
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

    
    
    def deliver_resources(self, task):
        """Deliver resources based on the task requirements."""
        if self.resources["fuel"] >= task["fuel_needed"]:
            self.resources["fuel"] -= task["fuel_needed"]
        if self.resources["medical_supplies"] >= task["medical_supplies_needed"]:
            self.resources["medical_supplies"] -= task["medical_supplies_needed"]
        if self.resources["food"] >= task["food_needed"]:
            self.resources["food"] -= task["food_needed"]
        if self.resources["seats"] >= task["seats_needed"]:
            self.resources["seats"] -= task["seats_needed"]
        print(f"Vehicle> Delivered resources for task: {task}")

    async def setup(self):
        print(f"Vehicle> Set up with JID {self.jid}.")
        await self.environment.updatePositionVehicle(self.x_pos, self.y_pos)

        behaviour = FSMBehaviour()
        behaviour.add_state(name=STATE_IDLE, state=StateIdle(), initial=True)
        behaviour.add_state(name=STATE_RECEIVE_TASKS, state=StateReceiveTasks())
        behaviour.add_state(name=STATE_NAVIGATE, state=StateNavigate())
        behaviour.add_state(name=STATE_DELIVER, state=StateDeliver())
        behaviour.add_transition(source=STATE_IDLE, dest=STATE_RECEIVE_TASKS)
        behaviour.add_transition(source=STATE_RECEIVE_TASKS, dest=STATE_NAVIGATE)
        behaviour.add_transition(source=STATE_NAVIGATE, dest=STATE_DELIVER)
        behaviour.add_transition(source=STATE_DELIVER, dest=STATE_IDLE)
        behaviour.add_transition(source=STATE_RECEIVE_TASKS, dest=STATE_IDLE)

        self.add_behaviour(behaviour)
