from tree import *


def minimax(node, depth, is_max, path=[]):
    if depth == MAX_VISIBILITY or not node.children_indxs:
        return [node.indx], node.heuristic_val

    best_path = []
    best_value = float('-inf') if is_max else float('inf')

    for child_idx in node.children_indxs:
        child = tree[child_idx]
        temp_path, value = minimax(child, depth + 1, not is_max, path + [child.indx])
        # updating values
        if is_max and value > best_value:
            best_value = value
            best_path = temp_path
        elif not is_max and value < best_value:
            best_value = value
            best_path = temp_path

    if best_path:
        return [node.indx] + best_path, best_value
    else:
        return [node.indx], best_value

# init_tree("1010")
# gen_node(tree[0], MAX_VISIBILITY)

# best_path, best_value = minimax(tree[0], 0, True)

# # TESTING
# print("Best path:", best_path)
# print("Best heuristic value:", best_value)

# print("Number of nodes in the tree:", len(tree))
# # Print the tree if necessary
# game_states = [tree[idx].value for idx in best_path]  # Extract the game state representation from each node

# print("Path through game states:", " -> ".join(game_states))

# if best_path:
#     # Get the index of the last node in the best path
#     last_node_index = best_path[-1]
#     # Access the node from the tree using this index
#     last_node = tree[last_node_index]

#     # Print the details of the last node
#     print(f"Node(value='{last_node.value}', p1_points={last_node.p1_points}, p2_points={last_node.p2_points}, level={last_node.level}, indx={last_node.indx}, parent_indx={last_node.parent_indx}, children_indxs={last_node.children_indxs}, heuristic_val={last_node.heuristic_val})")
# # TESTING


# print(len(tree))
# print(tree)