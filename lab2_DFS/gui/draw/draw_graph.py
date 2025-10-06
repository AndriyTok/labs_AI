import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import io
import networkx as nx


def draw_graph(self, path=None, path_edges=None, visited_edges=None, queue_nodes=None):
    G = self.active_graph
    pos = self.positions

    plt.figure(figsize=(7, 7))

    # Draw base graph
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10)

    # Draw visited edges in red
    if visited_edges:
        visited_edge_list = [e for e in visited_edges if isinstance(e, tuple) and e not in (path_edges or [])]
        nx.draw_networkx_edges(G, pos, edgelist=visited_edge_list, edge_color="red", width=2)

    # Draw path edges in green
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="green", width=3)

    # Draw visited nodes in yellow
    visited_nodes = set()
    if visited_edges:
        for edge in visited_edges:
            if isinstance(edge, tuple):
                visited_nodes.update(edge)
            else:
                visited_nodes.add(edge)
        nx.draw_networkx_nodes(G, pos, nodelist=list(visited_nodes), node_color="yellow", node_size=800)

    # Draw queue nodes in orange
    if queue_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=queue_nodes, node_color="orange", node_size=800)

    # Draw path nodes in green
    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green", node_size=800)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img = Image.open(buf)
    self.imgtk = ImageTk.PhotoImage(img)
    self.image_label.configure(image=self.imgtk)
