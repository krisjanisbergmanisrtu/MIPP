from tree import *

def alpha_beta(node, alpha, beta, max_visibility, path=[]):
    if len(node.children_indxs) == 0 or node.level == max_visibility:
        return [node.indx], node.heuristic_val

    best_path = []
    if node.level % 2 == 0:  # Maximizing player's turn
        best_value = float('-inf')
        for child_idx in node.children_indxs:
            child = tree[child_idx]
            temp_path, value = alpha_beta(child, alpha, beta, max_visibility, path + [child.indx])
            if value > best_value:
                best_value = value
                best_path = temp_path
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
    else:  # Minimizing player's turn
        best_value = float('inf')
        for child_idx in node.children_indxs:
            child = tree[child_idx]
            temp_path, value = alpha_beta(child, alpha, beta, max_visibility, path + [child.indx])
            if value < best_value:
                best_value = value
                best_path = temp_path
            beta = min(beta, best_value)
            if beta <= alpha:
                break

    if best_path:
        return [node.indx] + best_path, best_value
    else:
        return [node.indx], best_value


# Initialize the tree
# init_tree("1010")
# gen_node(tree[0], MAX_VISIBILITY)

# Perform alpha-beta pruning
# best_path, best_value = alpha_beta(tree[0], float('-inf'), float('inf'), MAX_VISIBILITY)

# TESTING
# print("Best path:", best_path)
# print("Best heuristic value:", best_value)
# print("Number of nodes in the tree:", len(tree))

# Extract the game state representation from each node in the best path
# game_states = [tree[idx].value for idx in best_path]
# print("Path through game states:", " -> ".join(game_states))

# if best_path:
#     # Get the index of the last node in the best path
#     last_node_index = best_path[-1]
#     # Access the node from the tree using this index
#     last_node = tree[last_node_index]

    # Print the details of the last node
    # print(f"Node(value='{last_node.value}', p1_points={last_node.p1_points}, p2_points={last_node.p2_points}, level={last_node.level}, indx={last_node.indx}, parent_indx={last_node.parent_indx}, children_indxs={last_node.children_indxs}, heuristic_val={last_node.heuristic_val})")
# TESTING
#
# print(len(tree))
# print(tree)


# alpha = Node(value="", p1_points=0, p2_points=0, level=0, indx=0, parent_indx=-1,
#              children_indxs=[], heuristic_val=float('-inf'))
# beta = Node(value="", p1_points=0, p2_points=0, level=0, indx=0, parent_indx=-1,
#             children_indxs=[], heuristic_val=float('inf'))

# init_tree('1010')  # This is used for testing
# gen_node(tree[0], MAX_VISIBILITY)  # This is used for testing
# # Perform alpha-beta pruning and print each step
# print("Alpha-Beta steps:")  # This is used for testing
# print(f"Initial Alpha: {alpha}, Initial Beta: {beta}")  # This is used for testing
# result = alpha_beta(tree[0], alpha, beta, MAX_VISIBILITY)  # This is used for testing
# print(f"Optimal Value: {result}")  # This is used for testing
