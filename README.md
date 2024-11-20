# Assignment 1: Multi-Agent Disaster Response and Relief Coordination System
#### CC3042, Faculdade de Sciencas e Universidade de Porto, 2024/2025

*Contributers:\
 Hanna Kristine Fagrell & Kacper Chmielewski*

### Objective:

Design and implement a decentralized multi-agent system using SPADE or JADE to simulate and optimize the coordination of relief efforts in response to a natural disaster. The system will involve various agents representing emergency responders, supply vehicles, shelters, and affected civilians, all working together to ensure effective resource allocation and assistance delivery.

### Problem Scenario:

In the aftermath of a natural disaster (e.g., earthquake, hurricane, or flood), relief efforts must be organized efficiently to ensure that affected areas receive food, medical supplies, rescue services, and shelter. Traditional centralized disaster management systems often struggle to cope with real-time challenges such as rapidly changing conditions, road blockages, and communication breakdowns. A decentralized system with autonomous agents representing different entities can respond more flexibly and efficiently to changing conditions and resource constraints.

### How to run:

**Make sure you have all the dependecies installed.**

XMPP server set up:

User is supposed to add following user to XMPP server with password corresponding to their agent type\
eg. username : civilian0@localhost, password: "civilian".\
eg. username: responder0@localhost, password: "responder".

List of necessary users:
civilian0@localhost\
civilian1@localhost\
civilian2@localhost\
civilian3@localhost\
civilian4@localhost\
responder0@localhost\
responder1@localhost\
responder2@localhost\
responder3@localhost\
responder4@localhost\
shelter0@localhost\
shelter1@localhost\
shelter2@localhost\
shelter3@localhost\
shelter4@localhost\
vehicle0@localhost\
vehicle1@localhost\
vehicle2@localhost\
vehicle3@localhost\
vehicle4@localhost\


You can run the main script by running the following command:

make run    - Run the main script\
make clean  - Remove .pyc files \
make help   - Show this help message
