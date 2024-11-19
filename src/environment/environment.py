from .disaster import Disaster
from shared.singletonMeta import SingletonMeta
import random
class Environment(metaclass=SingletonMeta):
    def __init__(self):
        self.size = 10
        self.board = [[Disaster(x, y) for y in range(self.size)] for x in range(self.size)]
        self.terrain_difficulty = [[random.randint(1, 9) for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        print("\nBoard status is following:")
        for i in range(self.size):
            board_row = " ".join(map(str, self.board[i]))
            terrain_row = " ".join(map(str, self.terrain_difficulty[i]))
            print(f"{board_row}          {terrain_row}")
        print()

    async def setTile(self, value):
        x = value["x_position"]
        y = value["y_position"]

        if value["emergency_type"] == "Safe":
            await self.board[x][y].removeEmergency()
        elif value["emergency_type"] == "Base" or value["emergency_type"] == "Vehicle":
            await self.board[x][y].setEmergency(value["emergency_type"])

        else:
            await self.board[x][y].setDisaster(self, value)

        self.display()


    async def getTile(self, x_axis, y_axis, operation):
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

    async def updatePositionVehicle(self, x_axis, y_axis):
        self.board[x_axis][y_axis].emergency = "Vehicle"