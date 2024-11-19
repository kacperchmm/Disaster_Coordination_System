from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from shared.utils import parseMessage

STATE_RECEIVE_CIVILIAN_REQUEST = "STATE_RECEIVE_CIVILIAN_REQUEST"
STATE_SEND_PRIORITY_QUEUE = "STATE_SEND_PRIORITY_QUEUE"
STATE_PRIORITIZE_REQUESTS = "STATE_PRIORITIZE_REQUESTS"


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
        print("Responder> Waiting for civilian requests...")

        self.agent.civilian_requests = []
        while len(self.agent.civilian_requests) < 3:
            msg = await self.receive(timeout=10)
            if msg:
                data = parseMessage(msg.body)
                print(f"Responder> Received a request: {data}")
                self.agent.civilian_requests.append(data)

        self.set_next_state(STATE_PRIORITIZE_REQUESTS)

class StatePrioritizeRequests(State):
    async def run(self):
        print("Responder> Prioritizing requests...")
        # Custom prioritization logic
        def priority_key(request):
            print(f"DEBUG> Request = {request}")
            priority = 0
            if request[0] == "medical":
                priority += 4
            if request[0] == "rescue":
                priority += 3
            if request[0] == "shelter":
                priority += 2
            if request[0] == "food":
                priority += 1
            return priority

        self.agent.civilian_requests.sort(key=priority_key, reverse=True)
        print(f"Responder> Prioritized requests: {self.agent.civilian_requests}")
        self.set_next_state(STATE_SEND_PRIORITY_QUEUE)

class StateSendPriorityQueue(State):
    async def run(self):
        print("Responder> Sending priority queue to supply vehicles...")

        vehicle_host = await self.agent.manager.getFirstAvailableHost("vehicle")

        # Send the number of messages first
        num_messages = len(self.agent.civilian_requests)
        init_msg = Message(to=vehicle_host)  # Replace with actual JID
        init_msg.set_metadata("ontology", "init")
        init_msg.body = f"init,{num_messages},0"
        await self.send(init_msg)
        print(f"Responder> Sent init message: {init_msg.body}")

        # Create and send the prioritized messages one by one
        for request in self.agent.civilian_requests:
            print(f"DEBUG> Responder request is {request}")
            help_msg = f"help,{request[1]},{request[2]}"
            msg = Message(to=vehicle_host)  # Replace with actual JID
            msg.set_metadata("ontology", "priority_queue")
            msg.body = help_msg
            await self.send(msg)
            print(f"Responder> Sent prioritized request: {msg.body}")

        self.set_next_state(STATE_RECEIVE_CIVILIAN_REQUEST)


class ResponderAgent(Agent):
    def __init__(self, jid, password, environment, manager):
        super().__init__(jid, password)
        self.environment = environment  # Shared environment reference
        self.priority_queue = []  # Store tasks prioritized by urgency
        self.manager = manager
        self.created_behaviours = {}
    
    async def getState(self):
        return str(self.created_behaviours["state_machine"].current_state)

    async def setup(self):
        print("Responder> Starting...")

        fsm = ResponderBehaviour()

        fsm.add_state(name=STATE_RECEIVE_CIVILIAN_REQUEST, state=StateReceiveCivilianRequest(), initial=True)
        fsm.add_state(name=STATE_PRIORITIZE_REQUESTS, state=StatePrioritizeRequests())
        fsm.add_state(name=STATE_SEND_PRIORITY_QUEUE, state=StateSendPriorityQueue())

        fsm.add_transition(source=STATE_RECEIVE_CIVILIAN_REQUEST, dest=STATE_PRIORITIZE_REQUESTS)
        fsm.add_transition(source=STATE_PRIORITIZE_REQUESTS, dest=STATE_SEND_PRIORITY_QUEUE)
        fsm.add_transition(source=STATE_SEND_PRIORITY_QUEUE, dest=STATE_RECEIVE_CIVILIAN_REQUEST)

        self.created_behaviours["state_machine"] = fsm
        self.add_behaviour(fsm) 