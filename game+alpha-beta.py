# python3

# Work In Progress
# Nodes inspired by Datu struktūras(1),22/23-P Uzdevums Nr.1-2, Krisjanis Bergmanis
from collections import namedtuple
import math

# Static variable that is hardcoded to represent max visibility
MAX_VISIBILITY = 5

# value - digit string - actual game tree property
# p1_points - player 1 points - actual game tree property
# p2_points - player 2 points - actual game tree property
# is_root - allows to know if, this is root node
# level - which tree level is, this allows to determine which is the active player
# index - current node index, this should make it easier to determine better paths
# parent_index - parent node index, this should make it easier to determine better paths
# children_indxs - list of childr indexes, this should make it easier to determine better paths
# heuristic_val - heuristic value of node

Node = namedtuple('Node',
                  ['value', 'p1_points', 'p2_points', 'is_root', 'level', 'indx', 'parent_indx', 'children_indxs',
                   'heuristic_val'])

# root_node has to be recalculated from UI
# root_node = Node(value="1010", p1_points=0, p2_points=0, is_root=True, level=0, indx=0, parent_indx=-1,
#                  children_indxs=[])

# this will contain all required properties for generating a tree
# tree = [root_node]  # This will contain nodes for tree
tree = []

def calc_heuristic_val(parent_node, current_node):
    
    heuristic_val = current_node.level * 2 + getattr(current_node, 'p1_points') - getattr(current_node, 'p2_points')
    if getattr(parent_node, 'heuristic_val') >= heuristic_val:
        return heuristic_val + 1 + (getattr(parent_node, 'heuristic_val') - heuristic_val)
    else:
        return heuristic_val

def generate_base_nodes(parent_node):
    
    nodes = []
    value = getattr(parent_node, 'value')
    for i in range(0, len(value) - 1):
        combo = value[i:i + 2]
        new_node = Node(value="", p1_points=getattr(parent_node, 'p1_points'), p2_points=getattr(parent_node, 'p2_points'), is_root=False, level=getattr(parent_node, 'level') + 1, indx=len(tree), parent_indx=getattr(parent_node, 'indx'), children_indxs=[], heuristic_val=0)
        if new_node.level % 2 != 0:
            p_active = new_node.p1_points
            p_waiting = new_node.p2_points
        else:
            p_active = new_node.p2_points
            p_waiting = new_node.p1_points

        if combo == "00":
            new_node = new_node._replace(value=value[:i] + "1" + value[i + 2:])
            p_active += 1
        elif combo == "01":
            new_node = new_node._replace(value=value[:i] + "0" + value[i + 2:])
            p_waiting += 1
        elif combo == "10":
            new_node = new_node._replace(value=value[:i] + "1" + value[i + 2:])
            p_waiting -= 1
        elif combo == "11":
            new_node = new_node._replace(value=value[:i] + "0" + value[i + 2:])
            p_active += 1

        if new_node.level % 2 != 0:
            new_node = new_node._replace(p1_points=p_active, p2_points=p_waiting)
        else:
            new_node = new_node._replace(p2_points=p_active, p1_points=p_waiting)

        new_node = new_node._replace(heuristic_val=calc_heuristic_val(parent_node, new_node))

        nodes.append(new_node)
    return nodes

def alpha_beta(node, alpha, beta, max_visibility):
    
    if len(getattr(node, 'value')) < 2 or getattr(node, 'level') >= max_visibility:
        return node.heuristic_val

    if node.level % 2 == 0:  # Maximizing player
        print(f"Max player at level {node.level}")
        for child_idx in getattr(node, 'children_indxs'):
            print(f"  Exploring child node {child_idx}")
            val = alpha_beta(tree[child_idx], alpha, beta, max_visibility)
            alpha = max(alpha, val)
            print(f"  Updated alpha: {alpha}")
            if beta <= alpha:
                print("  Pruned")
                break
        return alpha
    else:  # Minimizing player
        print(f"Min player at level {node.level}")
        for child_idx in getattr(node, 'children_indxs'):
            print(f"  Exploring child node {child_idx}")
            val = alpha_beta(tree[child_idx], alpha, beta, max_visibility)
            beta = min(beta, val)
            print(f"  Updated beta: {beta}")
            if beta <= alpha:
                print("  Pruned")
                break
        return beta

def gen_node(parent_node, max_visibility):
    # if length is less than two then it is not possible to play anymore
    if len(getattr(parent_node, 'value')) < 2:
        return
        # while length is at least 2 then we can still play the game
    elif getattr(parent_node, 'level') >= max_visibility:
        return
    else:  # while len(getattr(parent_node, 'value')) >= 2:
        nodes = generate_base_nodes(parent_node)

        for node in nodes:
            node = node._replace(indx=len(tree))
            tree[parent_node.indx] = tree[parent_node.indx]._replace(
                children_indxs=getattr(tree[parent_node.indx], 'children_indxs') + [node.indx])

            tree.append(node)
            if len(getattr(node, 'value')) >= 2:
                gen_node(node, max_visibility)
            elif getattr(node, 'level') >= max_visibility:
                return
            else:
                return

def init_tree(digit_string):
    
    tree.append(Node(value=digit_string, p1_points=0, p2_points=0, is_root=True, level=0, indx = 0, parent_indx=-1, children_indxs=[], heuristic_val=0))

# Initialize the tree with the given digit string
init_tree("101")

# Generate the game tree
gen_node(tree[0], MAX_VISIBILITY)

# Initialize alpha and beta
alpha = float('-inf')
beta = float('inf')

# Perform alpha-beta pruning and print each step
print("Alpha-Beta steps:")
print(f"Initial Alpha: {alpha}, Initial Beta: {beta}")
result = alpha_beta(tree[0], alpha, beta, MAX_VISIBILITY)
print(f"Optimal Value: {result}")

