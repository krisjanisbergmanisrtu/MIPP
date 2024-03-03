# python3

# Threading setup from RTU - Datu struktūras(1),22/23-P Uzdevums Nr.1-2, Krisjanis Bergmanis
import sys
import threading
from collections import namedtuple

#
nodes = []  # This will store nodes that we have already handled
# is_root - is this node the root of tree
# value - digit string
# level - in which level this node is located in
# parent_index - parent node index
# p1_points - player 1 points
# p2_points - player 2 points
Node = namedtuple('Node', ['is_root', 'value', 'p1_points', 'p2_points', 'level', 'parent', 'children'])

#def_generate_tree()
# gen_node

# def gen_node()
# receive is_root, digit string, parent node, p1 points, p2, points,  array of children nodes
# while length of digit string 2 >=2 do
# generate possible string combos and for each calc points
#   gen_node() with the calculated string and points for each possible node, it is a recursion until
# length of digit string < 2
# then just return so it exits recursion


def main():
    print("Hello world!")


# In Python, the default limit on recursion depth is rather low,
# so raise it here for this problem. Note that to take advantage
# of bigger stack, we have to launch the computation in a new thread.
sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size
threading.Thread(target=main).start()
