# MAS Architecture

## Environment
First concept of map will be 10x10 board with following field types:
- base,
- disaster.
    
### Disaster field
Every disaster field should have a following properties:
- type of emergency,
- number of people to rescue,
- food to provide,
- medicine to provide,
- blockage status - if there is a blockage, food and medicine can be provided, but people can't be rescued,
- communication status - in case of no communication with certain field, priority of rescuing it should be the highest possible.

## Agent Types

General agent properties:
- fuel - agent has to consider if fuel level is enough to finish given task,
- main functionality - certain action is done quicker by this agent,
- rest level - if agent is working too long, the efficiency drops

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
