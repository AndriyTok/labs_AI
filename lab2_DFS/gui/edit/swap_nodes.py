import networkx as nx
from lab2_DFS.data.graph_data import GRAPH_POSITIONS
from lab2_DFS.logic.graphs.init_graphs import init_graphs


def swap_nodes(app):
    start_val = app.start_node.get()
    goal_val = app.goal_node.get()
    app.start_node.set(goal_val)
    app.goal_node.set(start_val)