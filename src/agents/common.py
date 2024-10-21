from spade.message import Message


"""
emergency_need = what supplies, food, medicine etc.

"""

def parseMessage(message):
    parts = message.split(',')

    if len(parts) != 3:
        raise ValueError("Wrong format of message!\n Expected: '<str>,<number>,<number>'")

    string_value = parts[0]
    try:
        number1 = int(parts[1])
        number2 = int(parts[2])
    except ValueError:
        raise ValueError("The second and third values must be valid integers.")

    return string_value, number1, number2


"""
def a_star_search(tower):
    stack = [tower]
    visited = set()

    while stack:
        current_node = stack.pop(0)

        if current_node.check_cube():
            current_node.visualize_path()
            return current_node.get_path()

        visited.add(tuple(current_node.configuration))

        actions = current_node.find_actions()
        for action in actions:
            if tuple(action.configuration) not in visited:
                stack.append(action)
                visited.add(tuple(action.configuration))

        stack.sort(key=lambda action: action.heuristic())
    return None
"""

def a_star_search(h,x,y):
    stack = [(x,y)]
    visited = set()

    # heuristic = terrain difficulty
    # board from env
    # supply vehicle p

