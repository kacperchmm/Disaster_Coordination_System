from .disaster import Disaster
from shared.singletonMeta import SingletonMeta
import random
import os   

"""
@file environment.py
@description This file contains the Environment class which is responsible for managing the environment in the simulation.
"""

class Environment(metaclass=SingletonMeta):

    def __init__(self):
        self.size = 10
        self.board = [[Disaster(x, y) for y in range(self.size)] for x in range(self.size)]
        self.terrain_difficulty = [[random.randint(1, 9) for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        os.system("clear")
        print("\nBoard status is following:")
        for i in range(self.size):
            board_row = " ".join(map(str, self.board[i]))
            terrain_row = " ".join(map(str, self.terrain_difficulty[i]))
            print(f"{board_row}          {terrain_row}")
        print()

    async def setTile(self, value):
        x = value["x_position"]
        y = value["y_position"]

        if value["status"] == "Safe":
            await self.board[x][y].removeEmergency()
        elif value["status"] == "Base" or value["status"] == "Vehicle" or value["status"] == "Shelter" or value["status"] == "Rescued":
            await self.board[x][y].setEmergency(value["status"])

        else:
            await self.board[x][y].setDisaster(value)

        self.display()


    async def getTile(self, x_axis, y_axis):
        return self.board[x_axis][y_axis].getTileData()

    async def updatePositionVehicle(self, x_curr, y_curr, x_next, y_next, init):
        if not init and self.board[x_curr][y_curr].emergency != "Base":
            self.board[x_curr][y_curr].emergency = "Safe"
        else:
            print(f"INIT = {self.board[x_next][y_next].emergency}")
        if self.board[x_next][y_next].emergency != "Base":
            self.board[x_next][y_next].emergency = "Vehicle"

        self.display()