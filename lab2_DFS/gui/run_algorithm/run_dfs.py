import time
from tkinter import messagebox
from lab2_DFS.gui.draw.draw_graph import draw_graph
from lab2_DFS.logic.algorithm.dfs import dfs

def run_dfs(self):
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

    last = None
    for step in dfs(graph_data, start, goal, self.order.get()):
        path, path_edges, visited_edges, stack_nodes = step
        last = (path, path_edges, visited_edges, stack_nodes)
        draw_graph(self, path, path_edges, visited_edges, stack_nodes)
        self.update()
        time.sleep(0.23)

    if last:
        path, path_edges, visited_edges, stack_nodes = last
        visited_nodes = set()
        for edge in visited_edges:
            if isinstance(edge, (list, tuple)):
                visited_nodes.update(edge)
            else:
                visited_nodes.add(edge)

        if path:
            messagebox.showinfo("Result",
                              f"Path found: {' → '.join(map(str, path))}\n"
                              f"Visited nodes: {len(visited_nodes)}")
            draw_graph(self, path, path_edges, visited_edges, stack_nodes)
        else:
            messagebox.showwarning("Result",
                                 f"No path found.\n"
                                 f"Visited nodes: {len(visited_nodes)}")
            draw_graph(self, [], [], visited_edges, stack_nodes)