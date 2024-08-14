"""
Phuong Anh Nguyen - Student ID: 220276190
COSC550 - Practical Assignment 1
"""

import random
import re
import numpy as np

from queue import PriorityQueue
from prioritized_item import PrioritizedItem
from une_ai.models import GridMap, GraphNode
from une_ai.assignments.snake_game import DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_SIZE
from snake_agent import SnakeAgent


# 1. We create a model of the environment using a GridMap
w_env = int(DISPLAY_WIDTH / TILE_SIZE)
h_env = int(DISPLAY_HEIGHT / TILE_SIZE)
environment_map = GridMap(w_env, h_env, None)

DIRECTIONS = SnakeAgent.HEAD_DIRECTIONS


def is_food(node_state):
    global environment_map

    # if the environment_map at the coordinates in node_state is the location of the charging dock, return True
    # else, return False
    try:
        map_item_value = environment_map.get_item_value(node_state[0], node_state[1])
    except:
        map_item_value = 'O'

    return True if map_item_value == 'F' else False


def initial_food(environment_map, current_food):
    # Update the environment map with the food locations
    for cur_food in current_food:
        environment_map.set_item_value(cur_food[0], cur_food[1], 'F')


def initial_obstacle(environment_map, obstacles_location):
    # Update the environment map with the obstacle locations
    for obstacle in obstacles_location:
        environment_map.set_item_value(obstacle[0], obstacle[1], 'O')


def is_valid_direction(next_location, next_direction):
    if (next_location[1] not in environment_map.find_value('B') and
        next_location[1] not in environment_map.find_value('O') and
        next_location[0] != 'O' and
        next_direction != get_opposite_direction(cur_direction)):
        return True

    if next_location[0] == 'O':
        return False

    if next_location[1] in environment_map.find_value('B'):
        return False

        # Condition 2: Check if the next location is not an obstacle ('O')
    if next_location[1] in environment_map.find_value('O'):
        return False

        # Condition 3: Check if the next direction is not the opposite of the current direction
    if next_direction == get_opposite_direction(cur_direction):
        return False


def update_food(environment_map, food_location, current_food):
    for cur_food in current_food:
        environment_map.set_item_value(cur_food[0], cur_food[1], None)
    # Check through current food
    for food in food_location:
            environment_map.set_item_value(food[0], food[1], 'F')


def update_body(environment_map, current_body):
    # Remove all body previous locations
    for body in environment_map.find_value('B'):
        environment_map.set_item_value(body[0], body[1], None)

    # Add remaining to map
    for body in current_body:
        environment_map.set_item_value(body[0], body[1], 'B')


# creating a function to determine the future state
# given a current tile and wheels direction
def future_state(model, cur_location, direction):
    offset = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0)
    }
    cur_x, cur_y = cur_location
    new_x, new_y = (cur_x + offset[direction][0], cur_y + offset[direction][1])
    new_location = (new_x, new_y)

    try:
        value = model.get_item_value(new_x, new_y)
    except:
        # if here it means that the next location will be out of bounds
        # so that's a wall
        value = 'O'
        new_location = None

    return value, new_location

def expand(node):
    global environment_map
    actions = {
        'move-left': (-1, 0),
        'move-down': (0, 1),
        'move-right': (1, 0),
        'move-up': (0, -1),
    }

    # potential successors
    successors = []
    # for each action, we must check if the successor is:
    # 1. Within the boundaries of the environment map
    # 2. The environment_map at the successor location was not set as wall yet ('W')
    # If the action lead to any of the two possible scenarios, the successor will not be added to the expansion
    cur_state = node.get_state()
    for action, offset in actions.items():
        new_state = (cur_state[0] + offset[0], cur_state[1] + offset[1])
        try:
            item_in_map = environment_map.get_item_value(new_state[0], new_state[1])
        except:
            # out of bounds, it's a wall
            item_in_map = 'O'

        if (item_in_map == 'O'):

            continue

        # to create an instance of GraphNode:
        # successor = GraphNode(successor_state, node, action, cost)
        # successor_state is the representation of the state of the successor node, e.g. the x,y coordinates
        # the second parameter is the parent node we have as input to this function
        # action is the action that generated the successor via this expansion
        # cost is the cost to be in the state of the successor node, in this scenario all nodes have the same uniform cost (i.e. 1)
        cost = 1
        successor = GraphNode(new_state, node, action, cost)

        # after creating an instance of the successor, add it to the successors list
        successors.append(successor)

    return successors


def get_opposite_direction(current_direction):
    OPPOSITE_DIRECTIONS = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }
    return OPPOSITE_DIRECTIONS.get(current_direction, None)

# Feuristic Function
def heuristic_cost(current_node, is_food):
    food_list = []
    for x in range(0, w_env):
        for y in range(0, h_env):
            if is_food((x, y)):
                # Manhattan distance
                cur_dist = abs(current_node[0] - x) + abs(current_node[1] - y)
                food_list.append(cur_dist)

    # return the minimum cost among the computed distances
    return np.min(food_list)


def astar(start_node, is_food):
    initial_state = GraphNode(start_node, None, None, 0)

    frontier = PriorityQueue()

    _, g = initial_state.get_path()
    h = heuristic_cost(initial_state.get_state(), is_food)
    # Sum of actual path cost and cost provided by h cost
    # Add wrapped node "initial_state" to priority queue

    # put start node to open list
    frontier.put(PrioritizedItem(g + h, initial_state))

    reached = []
    while not frontier.empty():
        # unwrap node from the frontier queue; cur_node is the node with lowest f value
        cur_item = frontier.get()
        cur_node = cur_item.item

        successors = expand(cur_node)  # get neighbour of current node

        for successor in successors:
            # loop in successors list:
            if is_food(successor.get_state()):
            # Search function return successor is food
                return successor

        # using successor is food to create list suc_state???
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)

            # calculate g, h value
                _, g = successor.get_path()
                h = heuristic_cost(successor.get_state(), is_food)

            # add successor to the open list
                frontier.put(PrioritizedItem(g + h, successor))

    return False


def snake_agent_program(percepts, actuators):

    global environment_map, food_location, next_location, cur_direction, next_direction

    actions = []
    path_to_food = []

    current_body = percepts['body-sensor']
    current_state = current_body[0]
    obstacles_location = percepts['obstacles-sensor']
    current_food = percepts['food-sensor']
    cur_direction = actuators['head']

    initial_food(environment_map, current_food)
    initial_obstacle(environment_map, obstacles_location)
    for body in current_body:
        environment_map.set_item_value(body[0], body[1], 'B')

    #
    if len(path_to_food) == 0:
        goal_node = astar(current_state, is_food)

        if goal_node != False:
            path_to_food, _ = goal_node.get_path()

        if len(path_to_food) > 0:
            next_action = path_to_food.pop(0)

    if next_action is not None:
        next_direction = re.findall('move-(.*)', next_action)[0]
        directions = DIRECTIONS.copy()
        next_location = future_state(environment_map, current_state, next_direction)

        if is_valid_direction(next_location, next_direction) == False:
            while True:
                directions.remove(next_direction)
                try:
                    next_direction = random.choice(directions)
                except IndexError:
                    print('No valid direction')
                next_location = future_state(environment_map, current_state, next_direction)
                if is_valid_direction(next_location, next_direction):
                    break

            next_action = 'move-{}'.format(next_direction)
            actions.append(next_action)

        else:
            actions.append(next_action)

        update_body(environment_map, current_body)


    if is_food(next_location[1]):
        actions.append('open-mouth')
        # refresh food once food has been eaten
        food_location = percepts['food-sensor']
        update_food(environment_map, food_location, current_food)
    elif actuators['mouth'] == 'open':
        actions.append('close-mouth')

    return actions
