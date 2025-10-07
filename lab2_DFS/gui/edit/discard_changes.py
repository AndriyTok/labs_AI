import networkx as nx
from lab2_DFS.data.graph_data import GRAPH_POSITIONS
from lab2_DFS.logic.graphs.init_graphs import init_graphs
from lab2_DFS.gui.draw.draw_graph import draw_graph
from lab2_DFS.logic.graphs.init_graphs import on_graph_type_change

def clean_view(app):
    draw_graph(app)  # Drawing without parameters resets to default colors

def restore_default(app):
    gtype = app.graph_type.get().lower()
    # Re-initialize the graphs
    app.graphs = {
        "undirected": nx.Graph(),
        "directed": nx.DiGraph(),
        "tree": nx.Graph()
    }
    app.positions = GRAPH_POSITIONS.copy()
    init_graphs(app)
    # Set the active graph
    app.active_graph = app.graphs[gtype]
    if gtype == "tree":
        app.positions = app.tree_positions
    # Redraw
    draw_graph(app)


