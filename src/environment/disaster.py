"""
@file disaster.py
@description This file contains the Disaster class which is responsible for managing the disaster tiles in the simulation.
"""
class Disaster:
    def __init__(self, x_arg, y_arg):
        self.x_position = x_arg
        self.y_position = y_arg
        self.emergency = "Safe"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

    #
    # Value argument is a dictionary with following keys:
    # "x_position": Number,
    # "y_position": Number,
    # "status": String,
    # "food": Number,
    # "people": Number,
    # "medicine": Number,
    # "blockage": Bool,
    # "communication": Bool
    #

    async def setDisaster(self, value):
        self.emergency = value["status"]
        self.food_to_provide = value["food"]
        self.people_to_rescue = value["people"]
        self.medicine_to_provide = value["medicine"]
        self.blockage_status = value["blockage"]
        self.communication_status = value["communication"]

    async def getTileData(self):
        result = {
            "status": self.emergency,
            "food": self.food_to_provide,
            "medicine": self.medicine_to_provide,
            "people": self.people_to_rescue
        }

        return result


    async def removeEmergency(self):
        self.emergency = "Safe"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

    async def setEmergency(self, value):
        self.emergency = value

    async def getEmergency(self):
        return self.emergency
    
    async def setFoodToProvide(self, value):
        self.food_to_provide = value
    
    async def getFoodToProvide(self):
        return self.food_to_provide

    async def setPeopleToRescue(self, value):
        self.people_to_rescue = value
    
    async def getPeopleToRescue(self):
        return self.people_to_rescue
    
    async def setMedicineToProvide(self, value):
        self.medicine_to_provide = value
    
    async def getMedicineToProvide(self):
        return self.medicine_to_provide

    async def setBlockageStatus(self, value):
        self.blockage_status = value
    
    async def getBlockageStatus(self):
        return self.blockage_status
    
    async def setCommunication(self, value):
        self.communication_status = value
    
    async def getCommunication(self):
        return self.communication_status

    async def removeDisaster(self):
        self.emergency = "Rescued"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

    def __repr__(self):
        if self.emergency == "Safe":
            if self.blockage_status == True:
                return '\033[31m0\033[0m'   # Red color for Blockage
            else:
                return '0'
        elif self.emergency == "Base":
            return '\033[32mB\033[0m'       # Green color for Base tile
        elif self.emergency == "Vehicle":
            return '\033[33mV\033[0m'       # Yellow color for SupplyVehicle
        elif self.emergency == "Shelter":
            return '\033[36mS\033[0m'       # Cyan color for Shelter
        elif self.emergency == "Rescued":
            return '\033[35mR\033[0m'       # Magenta color for Rescued
        else:
            return "\033[31m#\033[0m"       # Red color for Disaster tile
