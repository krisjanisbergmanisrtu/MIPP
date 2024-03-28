# This file is to control all modules
from tree import *
from alpha_beta import *


def gen_winning_path(optimal_node):
    winning_path.append(optimal_node)
    push_node_into_winning_path(tree[getattr(optimal_node, 'parent_indx')])


def push_node_into_winning_path(optimal_node):
    winning_path.append(optimal_node)
    if getattr(optimal_node, 'parent_indx') >= 0:
        push_node_into_winning_path(tree[getattr(optimal_node, 'parent_indx')])


# init_tree('1010')  # This is used for testing
# gen_node(tree[0], MAX_VISIBILITY)  # This is used for testing
# Perform alpha-beta pruning and print each step
# print("Alpha-Beta steps:")  # This is used for testing
# print(f"Initial Alpha: {alpha}, Initial Beta: {beta}")  # This is used for testing
# result = alpha_beta(tree[0], alpha, beta, MAX_VISIBILITY)  # This is used for testing
# print(f"Optimal Value: {result}")  # This is used for testing

# gen_winning_path(result)  # This is used for testing
# print(winning_path)  # This is used for testing
