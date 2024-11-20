from shared.logger import logging

from agents.respondAgent import ResponderAgent
from agents.shelterAgent import ShelterAgent
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
        for key, _ in self.agents.items():
            if key.startswith("civilian") and await self.agents[key].getState() == "STATE_PEACE":
                logging.info(f"FOUND {self.agents[key].jid}")
                return str(self.agents[key].jid)

    async def getCivilianFromTile(self, shelter_pos):
        for key, value in self.agents.items():
            if key.startswith("civilian") and value != None and await self.agents[key].getState() == "STATE_WAIT_FOR_HELP":
                if shelter_pos == await self.agents[key].getPos():
                    return key
            

    #
    # Creating Instance of needed hosts ande saving it to the agents dictionary
    #

    async def getAgentInstance(self, agent_name):
        print(f"CORE> Starting prosody client {agent_name}")
        agent_mapping = {
            "responder": ResponderAgent,
            "vehicle": SupplyVehicleAgent,
            "shelter": ShelterAgent
        }

        for agent_prefix, agent_class in agent_mapping.items():
            if agent_name.startswith(agent_prefix):
                if agent_class:
                    logging.info(f"key = {agent_name}, agent = {agent_prefix}")
                    return agent_class(agent_name, agent_prefix, self.env, self)
                else:
                    logging.info(f"CORE> Agent type '{agent_name}' is not implemented.")
                    return ":)"

    async def removeAgentInstance(self, key):
        if key in self.agents:
            logging.info(f"CORE> Removing agent {key}")
            self.agents[key] = None
        else:
            logging.error(f"CORE> Key '{key}' does not exist.") 

    #
    # Looking for empty slot in dictionary by keys "agent_name{i}@localhost"
    # when found key is None create instance of it
    #

    async def responderListening(self, key, agent_name):
        logging.info(f"Agent> looking for {agent_name} on {key}")
        if agent_name.startswith("responder") and key.startswith("responder") and self.agents[key] != None:
            return await self.agents[key].getState() == "STATE_RECEIVE_CIVILIAN_REQUEST"

    async def getFirstAvailableHost(self, agent_name):
        for key, value in self.agents.items():
            if await self.responderListening(key, agent_name):
                return key

            if key.startswith(agent_name) and value is None:
                self.agents[key] = await self.getAgentInstance(key)
                await self.agents[key].start(auto_register=True)
                return key
        logging.error(f"ERROR> No available host found for {agent_name}")
        return None
