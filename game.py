# python3

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
# children_indxs - list of childr indexes, this should make it easier to determine better paths

Node = namedtuple('Node',
                  ['value', 'p1_points', 'p2_points', 'is_root', 'level', 'indx', 'parent_indx', 'children_indxs'])

# root_node has to be recalculated from UI
# root_node = Node(value="1010", p1_points=0, p2_points=0, is_root=True, level=0, indx=0, parent_indx=-1,
#                  children_indxs=[])

# this will contain all required properties for generating a tree
# tree = [root_node]  # This will contain nodes for tree
tree = []


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
            tree[parent_node.indx] = tree[parent_node.indx]._replace(
                children_indxs=getattr(tree[parent_node.indx], 'children_indxs') + [node.indx])
            # parent_node = parent_node._replace(children_indxs=getattr(parent_node, 'children_indxs') + [node.indx])
            tree.append(node)
            if len(getattr(node, 'value')) >= 2:
                gen_node(node)
            else:
                return


def init_tree(digit_string):
    tree.append(Node(value=digit_string, p1_points=0, p2_points=0, is_root=True, level=0, indx=0, parent_indx=-1,
                     children_indxs=[]))


gen_node(tree[0])

print(len(tree))
print(tree)
