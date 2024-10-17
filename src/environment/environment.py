from .disaster import Disaster

class Environment:
    def __init__(self):
        self.size = 10
        self.board = [[Disaster(x, y) for y in range(self.size)] for x in range(self.size)]

    def display(self):
        print("\nBoard status is following:")
        for row in self.board:
            print(" ".join(map(str, row)))
        print()

    async def setTile(self, value):
        x = value["x_position"]
        y = value["y_position"]

        if value["emergency_type"] == "Safe":
            await self.board[x][y].removeEmergency()
        else:
            await self.board[x][y].setEmergency(self, value)

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
