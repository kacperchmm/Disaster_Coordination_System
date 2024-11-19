from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from shared.utils import parseMessage

STATE_RECEIVE_CIVILIAN_REQUEST = "STATE_RECEIVE_CIVILIAN_REQUEST"
STATE_SEND_PRIORITY_QUEUE = "STATE_SEND_PRIORITY_QUEUE"

# Responder has to collect few messages from civilians
# Responder has to send the messages to supply:
#   - first send string with number of messages. eg. "init,{number_of_messages},0"
#   - take string_format_msg from priority queue and send them to vehicles
#           

class ResponderBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"Responder> Starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"Responder> finished at state {self.current_state}")

class StateReceiveCivilianRequest(State):
    async def run(self):
        print("Responder> Waiting for civilian request...")

        msg = await self.receive(timeout=10)
        if msg:
            try:
                #
                # Collect few messages from civilians, less than 3
                #

                data = parseMessage(msg.body)
                print(f"Responder> Received a request: {data}")

                self.agent.priority_queue.append((6, data))

                self.set_next_state(STATE_SEND_PRIORITY_QUEUE)
            except Exception as exc:
                print(f"Error parsing message: {exc}")
                self.set_next_state(STATE_RECEIVE_CIVILIAN_REQUEST)  # Stay in the same state

        else:
            print("Responder> Waiting for message.")
            self.set_next_state(STATE_RECEIVE_CIVILIAN_REQUEST)

class StateSendPriorityQueue(State):
    async def run(self):
        print("Responder> Sending priority queue...")
        if self.agent.priority_queue:

            #
            # Get a length of needs list, and send it in format eg. "init,{number_of_messages},0"
            #
            # Create a list of string in our message format <help,x_pos,y_pos>
            # send them one by one to supply,
            #

            sorted_queue = sorted(self.agent.priority_queue, key=lambda x: x[0])
            print(f"Responder> sorted queye{str(sorted_queue)}")

            vehicle_host = await self.agent.manager.getFirstAvailableHost("vehicle")

            print(f"Responder> Connected to {vehicle_host}")

            _, task = sorted_queue.pop(0)

            task_str = ','.join(map(str, task))

            msg = Message(to=str(vehicle_host)) 
            msg.set_metadata("ontology", "priority_queue")
            msg.body = task_str
            await self.send(msg)
            print("Receiver> Message sent do vehicle")
        else:
            print(f"Responder> queue empty")
        
        # After sending, transition to the receive civilian request state again
        self.set_next_state(STATE_RECEIVE_CIVILIAN_REQUEST)

class ResponderAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment  # Shared environment reference
        self.priority_queue = []  # Store tasks prioritized by urgency
        self.manager = manager

    async def setup(self):
        print("Responder> Starting...")

        behaviour = ResponderBehaviour()

        #
        # Add states to the FSM 
        #

        behaviour.add_state(name=STATE_RECEIVE_CIVILIAN_REQUEST, state=StateReceiveCivilianRequest(), initial=True)
        behaviour.add_state(name=STATE_SEND_PRIORITY_QUEUE, state=StateSendPriorityQueue())

        #
        # Define transitions between states
        #

        behaviour.add_transition(source=STATE_RECEIVE_CIVILIAN_REQUEST, dest=STATE_SEND_PRIORITY_QUEUE)
        behaviour.add_transition(source=STATE_SEND_PRIORITY_QUEUE, dest=STATE_RECEIVE_CIVILIAN_REQUEST)
        behaviour.add_transition(source=STATE_RECEIVE_CIVILIAN_REQUEST, dest=STATE_RECEIVE_CIVILIAN_REQUEST)

        #
        # Add the FSM behaviour to the agent
        #
        self.add_behaviour(behaviour)
