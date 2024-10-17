from agents.civilianAgent import CivilianAgent

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
    # "emergency_type": String,
    # "food": Number,
    # "people": Number,
    # "medicine": Number,
    # "blockage": Bool,
    # "communication": Bool
    #

    async def setEmergency(self, env, value):
        self.emergency = value["emergency_type"]
        self.food_to_provide = value["food"]
        self.people_to_rescue = value["people"]
        self.medicine_to_provide = value["medicine"]
        self.blockage_status = value["blockage"]
        self.communication_status = value["communication"]

        civilian_agent = CivilianAgent("civilian@localhost", "civilian", self.x_position, self.y_position, env)
        await civilian_agent.start(auto_register=True)

    async def removeEmergency(self):
        self.emergency = "Safe"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

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
        self.emergency = "Safe"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

    def __repr__(self):
        return '0' if self.emergency ==  "Safe" else "\033[31m#\033[0m"
