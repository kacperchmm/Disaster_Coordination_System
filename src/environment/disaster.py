class Disaster:
    def __init__(self):
        self.emergency = "Safe"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

    def setEmergency(self, value):
        self.emergency = value
    
    def getEmergency(self):
        return self.emergency
    
    def setFoodToProvide(self, value):
        self.food_to_provide = value
    
    def getFoodToProvide(self):
        return self.food_to_provide

    def setPeopleToRescue(self, value):
        self.people_to_rescue = value
    
    def getPeopleToRescue(self):
        return self.people_to_rescue
    
    def setMedicineToProvide(self, value):
        self.medicine_to_provide = value
    
    def getMedicineToProvide(self):
        return self.medicine_to_provide

    def setBlockageStatus(self, value):
        self.blockage_status = value
    
    def getBlockageStatus(self):
        return self.blockage_status
    
    def setCommunication(self, value):
        self.communication_status = value
    
    def getCommunication(self):
        return self.communication_status

    def removeDisaster(self):
        self.emergency = "Safe"
        self.food_to_provide  = 0
        self.people_to_rescue = 0
        self.medicine_to_provide = 0
        self.blockage_status = False
        self.communication_status = True

    def __repr__(self):
        return '0' if self.emergency is "Safe" else "\033[31m#\033[0m"
