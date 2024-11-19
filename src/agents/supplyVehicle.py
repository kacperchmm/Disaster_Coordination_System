from spade import wait_until_finished
from spade.behaviour import CyclicBehaviour, FSMBehaviour, State
from spade.agent import Agent
from spade.message import Message

from shared.logger import logging
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
        logging.info("Vehicle> In idle state.")
        self.set_next_state(STATE_RECEIVE_TASKS)


class StateReceiveTasks(State):
    async def run(self):
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
                # else:
                #     print("Vehicle> No tasks received.")
                #     self.set_next_state(STATE_IDLE)
                #     return

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
            # task = self.agent.prioritize_tasks()
            task = self.agent.priority_queue[0]  # Peek at the next task
            start_position = self.agent.get_pos()
            destination = (task[1], task[2])

            # Find the optimal path
            path = a_star_search(heuristic, start_position, destination, self.agent.environment.board)
            if path:
                for step in path:
                    logging.info(f"Vehicle> Moving to position: {step}")

                    await self.agent.environment.updatePositionVehicle(self.agent.x_pos, self.agent.y_pos, step[0], step[1], False)
                    self.agent.x_pos, self.agent.y_pos = step

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
            #
            # TODO: repair reprioritizing tasks
            # task = self.agent.prioritize_tasks()
            #
            task = self.agent.priority_queue.pop(0)  # Dequeue the task

            await self.agent.deliver_resources()
            logging.info(f"Vehicle> Supplied help on {task[1]}, {task[2]}")

            #
            # set up a shelter agent, who will tell the civilian help is provided
            #
            # check supplies, go to base if needed or go to other disaster  
            #

            shelter_agent = self.agent.manager.getFirstAvailableHost("shelter")
            
            #
            # send message to shelter, maybe in the same format as to responder
            # like init, then message or just a message to set up a shelter
            #


            #
            # new state needed for going back to base
            #

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

        medicine_res = self.supply("medicine", tile_data)
        people_res   = self.supply("people", tile_data)
        food_res     = self.supply("food", tile_data)

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
        logging.info(f"Vehicle> Set up with JID {self.jid}.")
        await self.environment.updatePositionVehicle(0, 0, self.x_pos, self.y_pos, True)

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
