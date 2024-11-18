from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from agents.utils import parseMessage

from spade.behaviour import OneShotBehaviour

from spade import wait_until_finished
from agents.common import parseMessage

STATE_PEACE = "STATE_PEACE"
STATE_ASK_FOR_HELP = "STATE_ASK_FOR_HELP"
STATE_WAIT_FOR_HELP = "STATE_WAIT_FOR_HELP"
STATE_GOODBYE= "STATE_GOODBYE"


class CivilianBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"Civilian> Starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"Civilian> finished at state {self.current_state}")
        # await self.agent.stop()

class StatePeace(State):
    async def run(self):
        print("Civilian> Civilian in state peace :)")

        msg = await self.receive(timeout=10)

        if msg:
            type, x_pos, y_pos = parseMessage(msg.body)
            if type == "disaster":
                self.agent.x_position = x_pos
                self.agent.y_position = y_pos
                print(f"Civilian> Help needed at [{x_pos}, {y_pos}]")
                self.set_next_state(STATE_ASK_FOR_HELP)
            else:
                print("No disaster detected, staying in STATE_PEACE.")
                self.set_next_state(STATE_PEACE)
        else:
            print("Civilian> Waiting for message.")
            self.set_next_state(STATE_PEACE)

#
# Send help request based on needs
# Priority: 
# medicine > food > rescue people
#

class StateAskForHelp(State):
    async def run(self):
        print("Civilian> Asking for help")
        x_position = self.agent.x_position
        y_position = self.agent.y_position

        #
        # Ask for certain needs
        #

        responder_host = await self.agent.manager.getFirstAvailableHost("responder")

        msg = Message(to=str(responder_host))
        msg.set_metadata("performative", "request")
        msg.body = f"medicine,{x_position},{y_position}"
        await self.send(msg)
        print("Civilian> Help request sent.")
        self.set_next_state(STATE_WAIT_FOR_HELP)


class StateWaitForHelp(State):
    async def run(self):
        print("Civilian> Waiting for help")
        msg = await self.receive(timeout=10)
        if msg:
            print("Civilian> Recieved message = " + msg.body)
            self.set_next_state(STATE_PEACE)


class StateGoodBye(State):
    async def run(self):
        print("Civilian> recieved help.")
        await self.agent.manager.removeAgentInstance(str(self.agent.jid))


class CivilianAgent(Agent):

    def __init__(self, jid, password, env, manager):
        super().__init__(jid, password)
        self.x_position = 0
        self.y_position = 0
        self.env = env
        self.manager = manager
        self.created_behaviours = {}

    async def getState(self):
        return str(self.created_behaviours["state_machine"].current_state)

    async def setup(self):
        behaviour = CivilianBehaviour()
        behaviour.add_state(name=STATE_PEACE, state=StatePeace(), initial=True)
        behaviour.add_state(name=STATE_ASK_FOR_HELP, state=StateAskForHelp())
        behaviour.add_state(name=STATE_WAIT_FOR_HELP, state=StateWaitForHelp())
        behaviour.add_state(name=STATE_GOODBYE, state=StateGoodBye())
        behaviour.add_transition(source=STATE_PEACE, dest=STATE_ASK_FOR_HELP)
        behaviour.add_transition(source=STATE_PEACE, dest=STATE_PEACE)
        behaviour.add_transition(source=STATE_ASK_FOR_HELP, dest=STATE_WAIT_FOR_HELP)
        behaviour.add_transition(source=STATE_WAIT_FOR_HELP, dest=STATE_PEACE)
        self.add_behaviour(behaviour)
        self.created_behaviours["state_machine"] = behaviour
        await self.manager.addCivilian(self)
