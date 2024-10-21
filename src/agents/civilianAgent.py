
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade import wait_until_finished

STATE_PEACE = "STATE_PEACE"
STATE_ASK_FOR_HELP = "STATE_ASK_FOR_HELP"
STATE_WAIT_FOR_HELP = "STATE_WAIT_FOR_HELP"
STATE_GOODBYE= "STATE_GOODBYE"


class CivilianBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"Civilian> Starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"Civilian> finished at state {self.current_state}")
        await self.agent.stop()

class StatePeace(State):
    async def run(self):
        print("Everything's fine :)")

        self.set_next_state(STATE_ASK_FOR_HELP)
        #
        # Add behaviour for changes on tile
        #

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

        msg = Message(to="responder@localhost")
        msg.set_metadata("performative", "request")
        msg.body = f"medicine,{x_position},{y_position}"
        await self.send(msg)
        print("Help request sent.")
        self.set_next_state(STATE_WAIT_FOR_HELP)


class StateWaitForHelp(State):
    async def run(self):
        print("Civilian> Waiting for help")
        msg = await self.receive(timeout=10)
        if msg:
            self.set_next_state(STATE_GOODBYE)


class StateGoodBye(State):
    async def run(self):
        print("Civilian> recieved help.")


class CivilianAgent(Agent):

    def __init__(self, jid, password, x_axis, y_axis, environment):
        super().__init__(jid, password)
        self.x_position = x_axis
        self.y_position = y_axis
        self.environment = environment

    async def setup(self):
        behaviour = CivilianBehaviour()
        behaviour.add_state(name=STATE_PEACE, state=StatePeace(), initial=True)
        behaviour.add_state(name=STATE_ASK_FOR_HELP, state=StateAskForHelp())
        behaviour.add_state(name=STATE_WAIT_FOR_HELP, state=StateWaitForHelp())
        behaviour.add_state(name=STATE_GOODBYE, state=StateGoodBye())
        behaviour.add_transition(source=STATE_PEACE, dest=STATE_ASK_FOR_HELP)
        behaviour.add_transition(source=STATE_ASK_FOR_HELP, dest=STATE_WAIT_FOR_HELP)
        behaviour.add_transition(source=STATE_WAIT_FOR_HELP, dest=STATE_GOODBYE)
        self.add_behaviour(behaviour)
