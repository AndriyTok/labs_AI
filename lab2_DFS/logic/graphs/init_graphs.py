from lab2_DFS.data.graph_data import (
    GRAPH_UNDIRECTED, GRAPH_POSITIONS
)
from lab2_DFS.data.tree import (
    tree_positions, calculate_tree_pos
)

from lab2_DFS.logic.graphs.types import get_graph

from lab2_DFS.gui.draw.draw_graph import draw_graph


def init_graphs(self):
    # Undirected
    for node, neighbors in GRAPH_UNDIRECTED.items():
        for n in neighbors:
            self.graphs["undirected"].add_edge(node, n)

    # Directed
    for node, neighbors in get_graph("directed").items():
        for n in neighbors:
            self.graphs["directed"].add_edge(node, n)

    # Tree: build a binary tree with nice layout
    tree_edges = []
    for parent in range(1, 16):
        left = parent * 2
        right = parent * 2 + 1
        if left <= 30:
            tree_edges.append((parent, left))
        if right <= 30:
            tree_edges.append((parent, right))
    self.graphs["tree"].add_edges_from(tree_edges)

    calculate_tree_pos(1, 0, -10, 10)
    self.tree_positions = tree_positions


def on_graph_type_change(self, event=None):
    gtype = self.graph_type.get().lower()
    self.active_graph = self.graphs[gtype]
    if gtype == "tree":
        self.positions = self.tree_positions
    else:
        self.positions = GRAPH_POSITIONS.copy()
    draw_graph(self)
