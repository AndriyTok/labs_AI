import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import io
import networkx as nx

def draw_graph(self, path=None, path_edges=None, visited_edges=None):
    G = self.active_graph
    pos = self.positions

    plt.figure(figsize=(7, 7))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10)

    # Draw visited edges (wrong) in yellow
    if visited_edges:
        nx.draw_networkx_edges(G, pos, edgelist=[e for e in visited_edges if e not in (path_edges or [])],
                               edge_color="red", width=2)
    # Draw path edges (correct) in orange
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="green", width=3)

    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img = Image.open(buf)
    self.imgtk = ImageTk.PhotoImage(img)
    self.image_label.configure(image=self.imgtk)
