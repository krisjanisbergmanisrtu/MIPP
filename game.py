# This file is to control all modules
from alpha_beta import *

computer_turn_time = []


def gen_winning_path(optimal_node):
    winning_path.append(optimal_node)
    push_node_into_winning_path(tree[getattr(optimal_node, 'parent_indx')])


def push_node_into_winning_path(optimal_node):
    winning_path.append(optimal_node)
    if getattr(optimal_node, 'parent_indx') >= 0:
        push_node_into_winning_path(tree[getattr(optimal_node, 'parent_indx')])


def calculate_average_time():
    total = 0
    for num in computer_turn_time:
        total += num
    average = total / len(computer_turn_time)
    return average
