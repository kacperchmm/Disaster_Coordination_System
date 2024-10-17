# Import necessary SPADE modules
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

import asyncio
import spade
import os

from .disaster import Disaster

class Environment:
    def __init__(self):
        self.size = 10
        self.board = [[Disaster(x, y) for y in range(self.size)] for x in range(self.size)]

    def display(self):
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
