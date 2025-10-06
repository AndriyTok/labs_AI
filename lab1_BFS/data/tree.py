tree_positions = {}
level_y_spacing = 2.0

def calculate_tree_pos(node, depth, min_x, max_x):
    if node > 30:
        return
    x = (min_x + max_x) / 2
    y = 12 - depth * level_y_spacing
    tree_positions[node] = (x, y)
    calculate_tree_pos(node * 2, depth + 1, min_x, x)
    calculate_tree_pos(node * 2 + 1, depth + 1, x, max_x)