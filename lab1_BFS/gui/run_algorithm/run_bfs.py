from tkinter import messagebox

from lab1_BFS.gui.draw.draw_graph import draw_graph
from lab1_BFS.logic.algorithm.bfs import bfs


def run_bfs(self):
    g = self.active_graph
    graph_data = {n: list(g.neighbors(n)) for n in g.nodes}

    def parse_node(val):
        try:
            return int(val)
        except ValueError:
            return val.strip()

    start = parse_node(self.start_node.get())
    goal = parse_node(self.goal_node.get())
    if start not in graph_data or goal not in graph_data:
        messagebox.showerror("Error", "Invalid nodes.")
        return
    path, path_edges, visited_edges = bfs(graph_data, start, goal, self.order.get())
    if path:
        messagebox.showinfo("Result",
                            f"Path found: {' → '.join(map(str, path))}\n"
                            f"Visited nodes: {len(set([n for edge in visited_edges for n in edge]))}")
        draw_graph(self, path, path_edges, visited_edges)
    else:
        messagebox.showwarning("Result",
                               f"No path found.\n"
                               f"Visited nodes: {len(set([n for edge in visited_edges for n in edge]))}")
        draw_graph(None, [], visited_edges)
