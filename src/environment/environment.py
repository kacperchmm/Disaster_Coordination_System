# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

import asyncio
import spade
import os
import time
import random

from disaster import Disaster


# Define the Environment class to represent the air traffic control environment
class Environment:
    def __init__(self):
        # Initialize environment variables, e.g., aircraft positions, weather, runways, etc.
        self.size = 10
        self.board = [[Disaster() for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        # Display the board, printing '0' if emergency is None, otherwise the emergency value
        os.system("clear")
        for row in self.board:
            print(" ".join(map(str, row)))


    def setTile(self, x_axis, y_axis, operation, value):
        if operation == "emergency":
            self.board[x_axis][y_axis].setEmergency(value)

        elif operation == "food":
            self.board[x_axis][y_axis].setFoodToProvide(value)

        elif operation == "people":
            self.board[x_axis][y_axis].setPeopleToRescue(value)

        elif operation == "medicine":
            self.board[x_axis][y_axis].setMedicineToProvide(value)

        elif operation == "blockage":
            self.board[x_axis][y_axis].setBlockageStatus(value)

        elif operation == "communication":
            self.board[x_axis][y_axis].setCommunication(value)

    def getTile(self, x_axis, y_axis, operation):
        if operation == "emergency":
            return self.board[x_axis][y_axis].getEmergency()

        elif operation == "food":
            return self.board[x_axis][y_axis].getFoodToProvide()

        elif operation == "people":
            return self.board[x_axis][y_axis].getPeopleToRescue()

        elif operation == "medicine":
            return self.board[x_axis][y_axis].getMedicineToProvide()

        elif operation == "blockage":
            return self.board[x_axis][y_axis].getBlockageStatus()

        elif operation == "communication":
            return self.board[x_axis][y_axis].getCommunication()



class AirTrafficControlAgent(Agent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.environment = environment

    async def setup(self):
        # Define a behavior to perceive and interact with the environment
        class EnvironmentInteraction(CyclicBehaviour):
            async def run(self):
                print("EnvironmentInteraction behavior is running")
                # Perceive environment data - you can use ACL messages or other means
                aircraft_position = self.get_aircraft_position()
                weather_data = self.get_weather_data()
                runway_status = self.get_runway_status()

                # Make decisions based on perceptions and update the environment
                # Example: Check for conflicts and send instructions to aircraft

            def get_aircraft_position(self):
                # Implement logic to retrieve aircraft positions from the environment
                pass

            def get_weather_data(self):
                # Implement logic to retrieve weather data from the environment
                pass

            def get_runway_status(self):
                # Implement logic to retrieve runway status from the environment
                pass

        # Add the behavior to the agent
        self.add_behaviour(EnvironmentInteraction())


class AircraftAgent(Agent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.environment = environment

    async def setup(self):
        # Define a behavior to interact with the environment and air traffic control
        class AircraftInteraction(CyclicBehaviour):
            async def run(self):
                print("AircraftInteraction behavior is running")
                # Perceive environment data
                aircraft_position = self.get_aircraft_position()

                # update aircraft position
                self.agent.environment.update_aircraft_position(100, 3000)

                # Communicate with air traffic control
                await self.send_instruction_to_atc(aircraft_position)

            def get_aircraft_position(self):
                # Access the environment object to retrieve the aircraft's position
                return self.agent.environment.get_aircraft_position()

            async def send_instruction_to_atc(self, position):
                # Create an ACL message to send data to the air traffic control agent
                msg = Message(to="atc_agent@localhost")  # Replace with the correct ATC agent JID
                msg.set_metadata("performative", "inform")
                msg.body = f"Aircraft at position {position} requesting instructions."

                # Send the message
                await self.send(msg)

        # Add the behavior to the agent
        self.add_behaviour(AircraftInteraction())


async def main():
    # Create and initialize the environment
    atc_environment = Environment()

    atc_agent = AirTrafficControlAgent("admin@localhost", "admin", atc_environment)

    aircraft_agent = AircraftAgent("user1@localhost", "user", atc_environment)

    await atc_agent.start(auto_register=True)
    await aircraft_agent.start(auto_register=True)


if __name__ == "__main__":
    # spade.run(main())
    env = Environment()

    random_iteration = 7
    random_rows = random.sample(range(0, 9), random_iteration)
    random_columns = random.sample(range(0, 9), random_iteration)

    for i in range(random_iteration):
        env.display()
        env.setTile(random_rows[i], random_columns[i], "emergency", "TEST")

        time.sleep(1) 


