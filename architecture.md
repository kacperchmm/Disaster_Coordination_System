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
### Supply Vehicle Agents
### Shelter Agents
### Civilian Agents
### Environment



