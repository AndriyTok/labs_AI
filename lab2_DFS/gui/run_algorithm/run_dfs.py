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
    try:
        for step in dfs(graph_data, start, goal, self.order.get()):
            if len(step) == 5:
                path, path_edges, visited_edges, stack_nodes, visited = step
                last = (path, path_edges, visited_edges, stack_nodes, visited)
            else:
                path, path_edges, visited_edges, stack_nodes = step
                last = (path, path_edges, visited_edges, stack_nodes, None)

            draw_graph(self, path, path_edges, visited_edges, stack_nodes)
            self.update()
            time.sleep(0.23)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return

    if last:
        path, path_edges, visited_edges, stack_nodes, visited = last
        if path:
            visited_count = len(visited) if visited is not None else len(set().union(*[set(edge) for edge in visited_edges]))
            messagebox.showinfo("Result",
                              f"Path found: {' → '.join(map(str, path))}\n"
                              f"Visited nodes: {visited_count}"
                              f"\nPath length: {len(path)} nodes"
                              f"\nSearch efficiency: {len(path)}/{visited_count} "
                              f"= {len(path)/visited_count*100:.1f}%")
            draw_graph(self, path, path_edges, visited_edges, stack_nodes)
        else:
            visited_count = len(visited) if visited is not None else len(set().union(*[set(edge) for edge in visited_edges]))
            messagebox.showwarning("Result",
                               f"No path found.\n"
                               f"Visited nodes: {visited_count}")
            draw_graph(self, [], [], visited_edges, stack_nodes)
