from shared.logger import logging
import heapq
import random

"""
@file utils.py
@description This file contains utility functions that are used across the simulation.
"""

def parseMessage(message):
    parts = message.split(',')

    if len(parts) != 3:
        error_message = "Wrong format of message!\n Expected: '<str>,<number>,<number>'"
        logging.error(f"ValueError: {error_message}")
        raise ValueError(error_message)

    string_value = parts[0]
    try:
        number1 = int(parts[1])
        number2 = int(parts[2])
    except ValueError:
        error_message = "The second and third values must be valid integers."
        logging.error(f"ValueError: {error_message}")
        raise ValueError(error_message)

    return string_value, number1, number2

def generate_needs():
    return random.choice(["medical", "food", "shelter", "rescue"])

# A* Search Algorithm
def a_star_search(heuristic_func, start, goal, board):
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    # init dicts to track best path and cost
    came_from = {}
    g_costs = {start: 0}
    
    while open_list:
        # pop pos with lowest cost
        _, current = heapq.heappop(open_list)
        
        # if goal reached, return the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        # explore neighbours
        neighbors = get_neighbors(current, board)
        for neighbor in neighbors:
            # calculate cost for neighbour
            terrain_cost = heuristic_func(neighbor, goal)
            # heuristic for obsticles
            new_g_cost = g_costs[current] + terrain_cost
            
            # if new path is better
            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic_func(neighbor, goal)  # Total cost (g + h)
                heapq.heappush(open_list, (f_cost, neighbor))
                came_from[neighbor] = current
    
    return []  # return empty if no path is found

def get_neighbors(position, board):
    x, y = position
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # check if the neighbor is within bounds and accessible
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] != 'obstacle':
            neighbors.append((nx, ny))
    return neighbors

# Manhattan distance bc it's a grid
def heuristic(position, goal):
    x1, y1 = position
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)


