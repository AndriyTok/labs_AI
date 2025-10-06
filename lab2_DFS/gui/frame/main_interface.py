import tkinter as tk
from tkinter import ttk

from lab2_DFS.gui.edit.edit import add_node, remove_node, add_edge, remove_edge
from lab2_DFS.gui.run_algorithm.run_bfs import run_bfs
from lab2_DFS.gui.run_algorithm.run_dfs import run_dfs
from lab2_DFS.logic.graphs.init_graphs import on_graph_type_change


def run_search(app):
    if app.algorithm.get() == "DFS":
        run_dfs(app)
    else:
        run_bfs(app)


def build_interface(app):
    frame = tk.Frame(app)
    frame.pack(side='left', fill='y', padx=10, pady=10)

    tk.Label(frame, text="Graph type:").pack(anchor="w")
    cb = ttk.Combobox(frame, textvariable=app.graph_type,
                      values=["Undirected", "Directed", "Tree"])
    cb.pack(fill="x")
    cb.bind("<<ComboboxSelected>>", lambda e: on_graph_type_change(app, e))

    tk.Label(frame, text="Start node:").pack(anchor="w")
    tk.Entry(frame, textvariable=app.start_node).pack(fill="x")

    tk.Label(frame, text="Goal node:").pack(anchor="w")
    tk.Entry(frame, textvariable=app.goal_node).pack(fill="x")

    tk.Label(frame, text="Algorithm:").pack(anchor="w")
    ttk.Combobox(frame, textvariable=app.algorithm,
                 values=["DFS", "BFS"]).pack(fill="x")

    tk.Label(frame, text="Order:").pack(anchor="w")
    ttk.Combobox(frame, textvariable=app.order,
                 values=["asc", "desc"]).pack(fill="x")

    tk.Button(frame, text="Run Search", command=lambda: run_search(app)).pack(fill="x", pady=5)

    node_ops = tk.LabelFrame(frame, text="Node Ops")
    node_ops.pack(fill="x", pady=10)

    tk.Label(node_ops, text="Add node at x,y:").pack(fill="x", anchor="w", pady=2)

    addNode_row = tk.Frame(node_ops)
    addNode_row.pack(anchor="center", pady=2)

    app.x_var = tk.StringVar()
    app.y_var = tk.StringVar()
    tk.Entry(addNode_row, textvariable=app.x_var, width=5).pack(side='left', padx=2)
    tk.Entry(addNode_row, textvariable=app.y_var, width=5).pack(side="left", padx=2)
    tk.Button(addNode_row, text="+", command=lambda: add_node(app)).pack(side="left", padx=2)

    tk.Label(node_ops, text="Remove node:").pack(fill="x", anchor="w", pady=2)

    removeNode_row = tk.Frame(node_ops)
    removeNode_row.pack(anchor="center", pady=2)

    app.del_node_var = tk.StringVar()
    tk.Entry(removeNode_row, textvariable=app.del_node_var, width=5).pack(side="left", pady=2)
    tk.Button(removeNode_row, text="-", command=lambda: remove_node(app)).pack(side="left", pady=2)

    tk.Label(node_ops, text="Add edge (u,v):").pack(fill="x", anchor="w", pady=2)

    addEdge_row = tk.Frame(node_ops)
    addEdge_row.pack(anchor="center", pady=2)

    app.edge_u = tk.StringVar()
    app.edge_v = tk.StringVar()
    tk.Entry(addEdge_row, textvariable=app.edge_u, width=5).pack(side="left", pady=2)
    tk.Entry(addEdge_row, textvariable=app.edge_v, width=5).pack(side="left", pady=2)
    tk.Button(addEdge_row, text="~", command=lambda: add_edge(app)).pack(side="left", pady=2)

    tk.Label(node_ops, text="Remove edge (u,v):").pack(fill="x", anchor="w", pady=2)

    delEdge_row = tk.Frame(node_ops)
    delEdge_row.pack(anchor="center", pady=2)

    app.del_edge_u = tk.StringVar()
    app.del_edge_v = tk.StringVar()
    tk.Entry(delEdge_row, textvariable=app.del_edge_u, width=5).pack(side="left", pady=2)
    tk.Entry(delEdge_row, textvariable=app.del_edge_v, width=5).pack(side="left", pady=2)
    tk.Button(delEdge_row, text="-", command=lambda: remove_edge(app)).pack(side="left", pady=2)
