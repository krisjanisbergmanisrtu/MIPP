from tree import *


def alpha_beta(node, alpha, beta, max_visibility):
    if len(getattr(node, 'value')) < 2 or getattr(node, 'level') >= max_visibility:
        return node

    if node.level % 2 == 0:  # Maximizing player
        print(f"Max player at level {node.level}")
        for child_idx in getattr(node, 'children_indxs'):
            print(f"  gen_node(tree[0], MAX_VISIBILITY) # This is used for testing with index {child_idx}")
            val = alpha_beta(tree[child_idx], alpha, beta, max_visibility)
            # If determined value is greater than current alpha then reasign this value to alpha
            if getattr(alpha, 'heuristic_val') <= getattr(val, 'heuristic_val'):
                alpha = val

            print(f"  Updated alpha: {alpha}")
            if getattr(beta, 'heuristic_val') <= getattr(alpha, 'heuristic_val'):
                print("  Pruned")
                break
        return alpha
    else:  # Minimizing player
        print(f"Min player at level {node.level}")
        for child_idx in getattr(node, 'children_indxs'):
            print(f"  gen_node(tree[0], MAX_VISIBILITY) # This is used for testing with index {child_idx}")
            val = alpha_beta(tree[child_idx], alpha, beta, max_visibility)
            # If determined value is less than current beta then reasign this value to beta
            if getattr(beta, 'heuristic_val') > getattr(val, 'heuristic_val'):
                beta = val
            print(f"  Updated beta: {beta}")
            if getattr(beta, 'heuristic_val') <= getattr(alpha, 'heuristic_val'):
                print("  Pruned")
                break
        return beta


# Initialize alpha and beta
alpha = Node(value="", p1_points=0, p2_points=0, level=0, indx=0, parent_indx=-1,
             children_indxs=[], heuristic_val=float('-inf'))
beta = Node(value="", p1_points=0, p2_points=0, level=0, indx=0, parent_indx=-1,
            children_indxs=[], heuristic_val=float('inf'))

# init_tree('1010')  # This is used for testing
# gen_node(tree[0], MAX_VISIBILITY)  # This is used for testing
# # Perform alpha-beta pruning and print each step
# print("Alpha-Beta steps:")  # This is used for testing
# print(f"Initial Alpha: {alpha}, Initial Beta: {beta}")  # This is used for testing
# result = alpha_beta(tree[0], alpha, beta, MAX_VISIBILITY)  # This is used for testing
# print(f"Optimal Value: {result}")  # This is used for testing
