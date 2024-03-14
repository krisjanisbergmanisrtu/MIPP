# Work In Progress
# Nodes inspired by Datu struktūras(1),22/23-P Uzdevums Nr.1-2, Krisjanis Bergmanis
from collections import namedtuple

# value - digit string - actual game tree property
# p1_points - player 1 points - actual game tree property
# p2_points - player 2 points - actual game tree property
# is_root - allows to know if, this is root node
# level - which tree level is, this allows to determine which is the active player
# index - current node index, this should make it easier to determine better paths
# parent_index - parent node index, this should make it easier to determine better paths
# children_indxs - list of children indexes, this should make it easier to determine better paths

Node = namedtuple('Node',
                  ['value', 'p1_points', 'p2_points', 'is_root', 'level', 'indx', 'parent_indx', 'children_indxs'])

# root_node has to be recalculated from UI
root_node = Node(value="1010", p1_points=0, p2_points=0, is_root=True, level=0, indx=0, parent_indx=-1,
                 children_indxs=[])

# this will contain all required properties for generating a tree
tree = [root_node]  # This will contain nodes for tree


# generate_base_nodes - this method generates new possible nodes based on parent node
# it takes value and then iterates the string of digits to make possible combinations
# and calculates new digit string and potential points for each player
# returns list of new nodes
def generate_base_nodes(parent_node):
    nodes = []
    value = getattr(parent_node, 'value')
    for i in range(0, len(value) - 1):  # iterate over the parent value
        combo = value[i:i + 2]  # take two possible digits and create combos
        # create new value by replacing new combo with a specific string
        # create a new node with new value and points depending on combo
        new_node = Node(value="", p1_points=getattr(parent_node, 'p1_points'),
                        p2_points=getattr(parent_node, 'p2_points'), is_root=False,
                        level=getattr(parent_node, 'level') + 1,
                        indx=len(tree), parent_indx=getattr(parent_node, 'indx'),
                        children_indxs=[])
        # determine which player would make a move
        if new_node.level % 2 != 0:
            p_active = new_node.p1_points
            p_waiting = new_node.p2_points
        else:
            p_active = new_node.p2_points
            p_waiting = new_node.p1_points

        # calculate new possible nodes
        if combo == "00":
            new_node = new_node._replace(value=value[:i] + "1" + value[i + 2:])
            p_active = p_active + 1
        elif combo == "01":
            new_node = new_node._replace(value=value[:i] + "0" + value[i + 2:])
            p_waiting = p_waiting + 1
        elif combo == "10":
            new_node = new_node._replace(value=value[:i] + "1" + value[i + 2:])
            p_waiting = p_waiting - 1
        elif combo == "11":
            new_node = new_node._replace(value=value[:i] + "0" + value[i + 2:])
            p_active = p_active + 1

        # add points to correct player
        if new_node.level % 2 != 0:
            new_node = new_node._replace(p1_points=p_active)
            new_node = new_node._replace(p2_points=p_waiting)
        else:
            new_node = new_node._replace(p2_points=p_active)
            new_node = new_node._replace(p1_points=p_waiting)

        nodes.append(new_node)
    return nodes


# generate node and add it to the tree
def gen_node(parent_node):
    # if length is less than two then it is not possible to play anymore
    if len(getattr(parent_node, 'value')) < 2:
        return
    # while length is at least 2 then we can still play the game
    else:  # while len(getattr(parent_node, 'value')) >= 2:
        nodes = generate_base_nodes(parent_node)

        for node in nodes:
            node = node._replace(indx=len(tree))
            # TODO Update children index list for parent node
            # parent_node = parent_node._replace(children_indxs=getattr(parent_node, 'children_indxs') + [node.indx])
            tree.append(node)
            if len(getattr(node, 'value')) >= 2:
                gen_node(node)
            else:
                return


# Minimax algorithm with alpha-beta pruning
def alpha_beta(node, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or len(node.value) < 2:
        # Print information about the node being evaluated
        print("Evaluated node:", node)
        return evaluate(node)

    if maximizingPlayer:
        # Initialize maximum value to negative infinity
        maxEval = float('-inf')
        # Loop through child nodes
        for child_indx in node.children_indxs:
            child_node = tree[child_indx]
            print("Evaluating child node:", child_node)
            # Recursively call alpha-beta on child node, switching to minimizing player's turn
            eval = alpha_beta(child_node, depth - 1, alpha, beta, False)
            # Update maximum value
            maxEval = max(maxEval, eval)
            # Update alpha value
            alpha = max(alpha, eval)
            # Perform alpha-beta pruning if beta is less than or equal to alpha
            if beta <= alpha:
                print("Beta cut-off at node:", node)
                break  # Beta cut-off
        return maxEval
    else:
        # Initialize minimum value to positive infinity
        minEval = float('inf')
        # Loop through child nodes
        for child_indx in node.children_indxs:
            child_node = tree[child_indx]
            print("Evaluating child node:", child_node)
            # Recursively call alpha-beta on child node, switching to maximizing player's turn
            eval = alpha_beta(child_node, depth - 1, alpha, beta, True)
            # Update minimum value
            minEval = min(minEval, eval)
            # Update beta value
            beta = min(beta, eval)
            # Perform alpha-beta pruning if beta is less than or equal to alpha
            if beta <= alpha:
                print("Alpha cut-off at node:", node)
                break  # Alpha cut-off
        return minEval


# Evaluation function (to be implemented based on your game logic)
def evaluate(node):
    # Example evaluation function, returns difference in player 1 and player 2 points
    return node.p1_points - node.p2_points


# Generating the tree
gen_node(root_node)

# Calling alpha-beta algorithm
best_score = alpha_beta(root_node, depth=3, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True)
print("Best score:", best_score)