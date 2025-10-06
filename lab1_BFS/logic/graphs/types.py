from lab1_BFS.data.graph_data import (
    GRAPH_UNDIRECTED
)

def to_directed(graph):
    directed = {}
    for u in graph:
        directed[u] = []
        for v in graph[u]:
            if u < v:
                directed[u].append(v)
    return directed

def to_tree(graph, root=0):
    from collections import deque
    tree = {}
    visited = set([root])
    queue = deque([root])
    while queue:
        node = queue.popleft()
        children = []
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                children.append(neighbor)
                queue.append(neighbor)
        tree[node] = children
    for node in graph:
        if node not in tree:
            tree[node] = []
    return tree

def get_graph(graph_type='undirected'):
    if graph_type == 'undirected':
        return GRAPH_UNDIRECTED
    elif graph_type == 'directed':
        return to_directed(GRAPH_UNDIRECTED)
    elif graph_type == 'tree':
        return to_tree(GRAPH_UNDIRECTED)
    else:
        raise ValueError('Unknown graph type')