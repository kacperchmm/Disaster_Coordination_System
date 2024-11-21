from spade.behaviour import FSMBehaviour, State
from spade.agent import Agent
from spade.message import Message

from shared.logger import logging
from shared.utils import a_star_search, heuristic, parseMessage

import asyncio

"""
@file supplyVehicle.py
@description This file contains the SupplyVehicleAgent class which is responsible for managing the supply vehicle agents in the simulation.
"""

# Defining the states for the supply vehicle agent
STATE_IDLE = "STATE_IDLE"
STATE_RECEIVE_TASKS = "STATE_RECEIVE_TASKS"
STATE_NAVIGATE = "STATE_NAVIGATE"
STATE_DELIVER = "STATE_DELIVER"
STATE_BACK_TO_BASE = "STATE_BACK_TO_BASE"
STATE_FINISH = "STATE_FINISH"

class StateIdle(State):
    async def run(self):
        logging.info("Vehicle> In idle state.")
        self.set_next_state(STATE_RECEIVE_TASKS)


class StateReceiveTasks(State):
    async def run(self):
        if self.agent.priority_queue:
            logging.info(f"Vehicle> Moving to other disaster, left in queue: {self.agent.priority_queue}")
            self.set_next_state(STATE_NAVIGATE)
            return

        logging.info("Vehicle> Checking for tasks.")
        msg = await self.receive(timeout=10)
        if msg and msg.get_metadata("ontology") == "init":
            received_msg = parseMessage(msg.body)
            init_message = received_msg[1]

            for i in range(init_message):
                msg = await self.receive(timeout=10)
                if msg:
                    task = parseMessage(msg.body)
                    self.agent.priority_queue.append(task)
                    logging.info(f"Vehicle> Recieved message {task} :)")

            logging.info(f"Vehicle> Received {self.agent.priority_queue}")
            self.set_next_state(STATE_NAVIGATE)
        else:
            if msg:
                logging.info(f"Vehicle> Received wrong message {msg.body}")
            logging.info("Vehicle> No tasks received, staying idle.")
            self.set_next_state(STATE_IDLE)

class StateNavigate(State):
    async def run(self):
        logging.info("Vehicle> Navigating to task location.")
        if self.agent.priority_queue:
            task = self.agent.priority_queue[0]
            start_position = self.agent.get_pos()
            destination = (task[1], task[2])

            # Find the optimal path
            path = a_star_search(heuristic, start_position, destination, self.agent.environment.board)
            if path:
                prev_status = None
                for step in path:
                    logging.info(f"Vehicle> Moving to position: {step}")

                    status_temp = await self.agent.environment.getTileStatus(step[0], step[1])

                    await self.agent.environment.updatePositionVehicle(self.agent.x_pos, self.agent.y_pos, step[0], step[1], False, prev_status)
                    self.agent.x_pos, self.agent.y_pos = step

                    prev_status = status_temp

                    await asyncio.sleep(1)
                logging.info("Vehicle> Reached destination.")
                self.set_next_state(STATE_DELIVER)
            else:
                logging.info("Vehicle> No path found, returning to idle.")
                self.set_next_state(STATE_IDLE)
        else:
            self.set_next_state(STATE_IDLE)

class StateDeliver(State):
    async def run(self):
        logging.info("Vehicle> Delivering supplies.")
        if self.agent.priority_queue:
            need, x_pos, y_pos = self.agent.priority_queue.pop(0)  # Dequeue the task

            logging.info(f"Vehicle> Supplied help on {x_pos}, {y_pos}")
            shelter_agent = await self.agent.manager.getFirstAvailableHost("shelter")
            
            msg_init = Message(to=shelter_agent)
            msg_init.set_metadata("ontology", "init")
            msg_init.body = f"init,{x_pos},{y_pos}"
            await self.send(msg_init)

            logging.info(f"Vehicle> Send init message")
            
            msg_food = Message(to=shelter_agent)
            msg_food.set_metadata("ontology", "food")
            msg_food.body = str(self.agent.resources["food"])
            await self.send(msg_food)

            logging.info(f"Vehicle> Send food message")

            msg_people = Message(to=shelter_agent)
            msg_people.set_metadata("ontology", "people")
            msg_people.body = str(self.agent.resources["seats"])
            await self.send(msg_people)

            logging.info(f"Vehicle> Send people message")

            msg_medicine = Message(to=shelter_agent)
            msg_medicine.set_metadata("ontology", "medicine")
            msg_medicine.body = str(self.agent.resources["medicine"])
            await self.send(msg_medicine)

            logging.info(f"Vehicle> Send medicine message")
            self.set_next_state(STATE_BACK_TO_BASE)
        


class StateBackToBase(State):
    async def run(self):
        logging.info("Vehicle> On way back to base.")
        start_position = (self.agent.x_pos, self.agent.y_pos)
        destination = (4, 2)
        path = a_star_search(heuristic, start_position, destination, self.agent.environment.board)
        if path:
            prev_status = await self.agent.environment.getTileStatus(start_position[0], start_position[1])
            for step in path:
                logging.info(f"Vehicle> Moving to position: {step}")

                status_temp = await self.agent.environment.getTileStatus(step[0], step[1])

                await self.agent.environment.updatePositionVehicle(self.agent.x_pos, self.agent.y_pos, step[0], step[1], False, prev_status)
                self.agent.x_pos, self.agent.y_pos = step

                prev_status = status_temp

                await asyncio.sleep(1)
            logging.info("Vehicle> Back in base.")
            self.set_next_state(STATE_IDLE)


class SupplyVehicleAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment  # Shared environment reference
        self.manager = manager # Manager of created agent hosts
        self.x_pos = 4  # Current X position of the vehicle
        self.y_pos = 2  # Current Y position of the vehicle
        self.priority_queue = []  # Priority queue for tasks (min-heap)
        self.resources = {
            "fuel": 9999999,
            "medicine": 9999999,
            "food": 99999999,
            "seats": 99999999
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
        logging.info(f"Moved to position: ({self.x_pos}, {self.y_pos})")

    async def supply(self, resource, tile_data):
        tile_resource = tile_data[resource]
        vehicle_resource = self.resources[resource]

        result_change = 0

        if vehicle_resource >= tile_resource:
            self.resources[resource] -= tile_resource
        else:
            result_change = tile_resource - vehicle_resource
            self.resources[resource] = 0

        return result_change


    async def deliver_resources(self):
        tile_data = await self.environment.getTile(self.x_pos, self.y_pos)

        medicine_res = await self.supply("medicine", tile_data)
        people_res   = await self.supply("people", tile_data)
        food_res     = await self.supply("food", tile_data)

        is_safe = medicine_res + people_res + food_res

        tile_changes = {
            "status": is_safe == 0 if "Safe" else tile_data["status"],
            "x_position": self.x_pos,
            "y_position": self.y_pos,
            "medicine": medicine_res,
            "people": people_res,
            "food": food_res
        }

        await self.environment.setTile(tile_changes)

    def prioritize_tasks(self):
        """Re-prioritize tasks based on location and fuel resources."""
        def task_priority(task):
            distance = abs(self.x_pos - task["x_position"]) + abs(self.y_pos - task["y_position"])
            fuel_needed = task["fuel_needed"]
            return distance + fuel_needed

        self.priority_queue = sorted(self.priority_queue, key=task_priority)
        logging.info(f"Re-prioritized queue: {self.priority_queue}")

    async def setup(self):
        await self.environment.updatePositionVehicle(0, 0, self.x_pos, self.y_pos, True, "")

        behaviour = FSMBehaviour()
        behaviour.add_state(name=STATE_IDLE, state=StateIdle(), initial=True)
        behaviour.add_state(name=STATE_RECEIVE_TASKS, state=StateReceiveTasks())
        behaviour.add_state(name=STATE_NAVIGATE, state=StateNavigate())
        behaviour.add_state(name=STATE_DELIVER, state=StateDeliver())
        behaviour.add_state(name=STATE_BACK_TO_BASE, state=StateBackToBase())

        behaviour.add_transition(source=STATE_IDLE, dest=STATE_RECEIVE_TASKS)
        behaviour.add_transition(source=STATE_RECEIVE_TASKS, dest=STATE_NAVIGATE)
        behaviour.add_transition(source=STATE_NAVIGATE, dest=STATE_DELIVER)
        behaviour.add_transition(source=STATE_DELIVER, dest=STATE_IDLE)
        behaviour.add_transition(source=STATE_RECEIVE_TASKS, dest=STATE_IDLE)
        behaviour.add_transition(source=STATE_DELIVER, dest=STATE_BACK_TO_BASE)
        behaviour.add_transition(source=STATE_BACK_TO_BASE, dest=STATE_IDLE)

        logging.info(f"Vehicle> Set up with JID {self.jid}, state = {behaviour.current_state}.")

        self.add_behaviour(behaviour)
