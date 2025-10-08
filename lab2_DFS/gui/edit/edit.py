from tkinter import messagebox

from lab2_DFS.gui.draw.draw_graph import draw_graph


def add_node(self):
    try:
        x = float(self.x_var.get())
        y = float(self.y_var.get())
        existing = [int(n) for n in self.active_graph.nodes if str(n).isdigit()]
        new_id = max(existing) + 1 if existing else "1"
        self.active_graph.add_node(new_id)
        self.positions[new_id] = (x, y)
        draw_graph(self)
    except Exception:
        messagebox.showerror("Error", "Invalid coordinates")


def remove_node(self):
    try:
        node = int(self.del_node_var.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Invalid node identifier")
        return

    if node in self.active_graph.nodes:
        self.active_graph.remove_node(node)
        self.positions.pop(node, None)
        draw_graph(self)
    else:
        messagebox.showerror("Error", "Node not found")


def add_edge(self):
    try:
        u = int(self.edge_u.get().strip())
        v = int(self.edge_v.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Invalid node identifiers")
        return
    if u in self.active_graph.nodes and v in self.active_graph.nodes:
        if not self.active_graph.has_edge(u, v):
            self.active_graph.add_edge(u, v)
            draw_graph(self)
        else:
            messagebox.showinfo("Info", "Edge already exists")
    else:
        print("Edges:", list(self.active_graph.edges()))
        print("Trying to remove:", u, v)
        messagebox.showerror("Error", "Both nodes must exist")



def remove_edge(self):
    try:
        u=int(self.del_edge_u.get().strip())
        v=int(self.del_edge_v.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Invalid node identifiers")
        return

    if self.active_graph.has_edge(u, v):
        self.active_graph.remove_edge(u, v)
        draw_graph(self)
    else:
        messagebox.showerror("Error", "Edge does not exist")
