import tkinter as tk
import networkx as nx

from lab1_BFS.gui.draw.draw_graph import draw_graph

from lab1_BFS.data.graph_data import (
    DEFAULT_START, DEFAULT_GOAL,
    GRAPH_POSITIONS
)
from lab1_BFS.gui.frame.main_interface import build_interface
from lab1_BFS.logic.graphs.init_graphs import init_graphs


class BFSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BFS Visualizer")
        self.geometry("1000x700")

        self.graph_type = tk.StringVar(value="Undirected")
        self.order = tk.StringVar(value="asc")
        self.start_node = tk.StringVar(value=str(DEFAULT_START))
        self.goal_node = tk.StringVar(value=str(DEFAULT_GOAL))

        self.image_label = tk.Label(self)
        self.image_label.pack(side='right', fill='both', expand=True)

        self.graphs = {
            "undirected": nx.Graph(),
            "directed": nx.DiGraph(),
            "tree": nx.Graph()
        }
        self.positions = GRAPH_POSITIONS.copy()
        init_graphs(self)

        self.active_graph = self.graphs["undirected"]

        build_interface(self)
        draw_graph(self)

