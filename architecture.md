# MAS Architecture

## Agent Types

### Responder Agents
Role: These agents represent emergency response teams responsible for rescuing civilians, delivering medical aid, and assessing damage in affected areas. Responder agents must decide which locations to prioritize based on the urgency of needs and available resources.

Communication: Interact with civilians, respond to emergency and send status updates.
Decision-making: Prioritize help based on urgency.

### Supply Vehicle Agents
Role: These agents manage the delivery of resources (food, water, medical supplies) from centralized depots to affected regions or shelters. They should optimize routes, taking into account road conditions, traffic, and time-sensitive needs in various locations.

Communication: Communicate with the response agent, what and where should things be delivered. 

### Shelter Agents
Role: Shelter agents represent temporary shelters set up to house displaced civilians. They need to communicate with supply agents to request resources and with responder agents to coordinate the transportation of civilians to shelters.

Communication: Coordinate transportation of civilians to shelter with responder. Request recources from supply vehicle.

### Civilian Agents
Role: Represent people in emergency.
Communication: Signalize to responder agents that they need help.

### Environment

## Interactions

### Civilian to responder:
- Signalize that they need help to emergency responders.

### Responder to Civilian:
- Recieves emergency signal from civilian, prioritize based on urgency.
- Sends updates for when help is dispatched, or an unexpected event occurs (e.g. delay)

### Responder to Supply Vehicle:
- Recieves task from response agent

### Shelter to Supply Vehicle:
- Request supplies

### Shelter to Responder:
- Coordinate the transportation of civilians to shelters


## IDEAS
- Allocate free recources if necessary, e.g. supply vehicle agents could transport civilians.
