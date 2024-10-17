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



async def main():
    # Create and initialize the environment
    atc_environment = Environment()


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


