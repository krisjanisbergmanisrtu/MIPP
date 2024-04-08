# Algorithm inspired by materials in Mākslīgā intelekta pamati(1),23/24-P:
# 3.3. Tēma - Heiristiski informētas pārmeklēšanas algoritmi spēļu izstrādei
# Minimaksa algoritma lietojums spēles "Krustiņi-nullītes" izstrādei Python valodā (angļu valodā): https://levelup.gitconnected.com/mastering-tic-tac-toe-with-minimax-algorithm-3394d65fa88f

from tree import *

def minimax(node, depth, is_max, path=[]):
    # checks if max depth has been reached and if there are children
    if depth == MAX_VISIBILITY or not node.children_indxs:
        return [node.indx], node.heuristic_val

    best_path = []
    best_value = float('-inf') if is_max else float('inf')

    for child_idx in node.children_indxs :
        child = tree[child_idx]
        temp_path, value = minimax(child, depth + 1, not is_max, path + [child.indx])

# Checks which players turn is it and updates best values and path
        if is_max and value > best_value:
            best_value = value
            best_path = temp_path
        elif not is_max and value < best_value:
            best_value = value

    if best_path :
        return [node.indx] + best_path, best_value
    else:
        return [node.indx], best_value

