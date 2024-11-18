import logging

from agents.respondAgent import ResponderAgent
from agents.civilianAgent import CivilianAgent
from agents.supplyVehicle import SupplyVehicleAgent
from shared.singletonMeta import SingletonMeta
from asyncio import Lock
import asyncio

class AgentManager(metaclass=SingletonMeta):
    def __init__(self, env):
        self.numberOfAgents = 5
        self.agents = {}
        self.env = env
        self.locks = {name: Lock() for name in ['responder', 'civilian', 'vehicle', 'shelter']}

        #
        # Agent object instances
        #

        for i in range(self.numberOfAgents):
            self.agents[f"responder{i}@localhost"] = None
            self.agents[f"civilian{i}@localhost"] = None
            self.agents[f"vehicle{i}@localhost"] = None
            self.agents[f"shelter{i}@localhost"] = None


    #
    # Civilian hosts are started on the beggining of main
    #

    async def addCivilian(self, agent_instance):
        for i in range (self.numberOfAgents):
            if self.agents[f"civilian{i}@localhost"] is None:
                self.agents[f"civilian{i}@localhost"] = agent_instance
                return
            
    async def getCivilianJid(self):
        for key, _ in self.agents.items()   :
            if key.startswith("civilian") and await self.agents[key].getState() == "STATE_PEACE":
                print(f"FOUND {self.agents[key].jid}")
                return str(self.agents[key].jid)
            

    #
    # Creating Instance of needed hosts ande saving it to the agents dictionary
    #

    async def getAgentInstance(self, agent_name):
        print(f"CORE> Starting prosody client {agent_name}")
        agent_mapping = {
            "responder": ResponderAgent,
            "vehicle": SupplyVehicleAgent,
            "shelter": None,  # TODO: Replace with ShelterAgent
        }

        for agent_prefix, agent_class in agent_mapping.items():
            if agent_name.startswith(agent_prefix):
                if agent_class:
                    print(f"key = {agent_name}, agent = {agent_prefix}")
                    return agent_class(agent_name, agent_prefix, self.env, self)
                else:
                    print(f"CORE> Agent type '{agent_name}' is not implemented.")
                    return ":)"

    async def removeAgentInstance(self, key):
        if key in self.agents:
            print(f"CORE> Removing agent {key}")
            self.agents[key] = None
        else:
            print(f"CORE> Key '{key}' does not exist.") 

    #
    # Looking for empty slot in dictionary by keys "agent_name{i}@localhost"
    # when found key is None create instance of it
    #

    async def getFirstAvailableHost(self, agent_name):
        for key, value in self.agents.items():
            if key.startswith(agent_name) and value is None:
                self.agents[key] = await self.getAgentInstance(key)
                await self.agents[key].start(auto_register=True)
                return key
        print(f"ERROR> No available host found for {agent_name}")
        return None
