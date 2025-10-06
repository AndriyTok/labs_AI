# bfs_visualizer/bfs.py
from collections import deque


def bfs(graph: dict, start: str, goal: str, order: str = "asc"):
    visited = set()
    visited_edges = []
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node not in visited:
            visited.add(node)
            if node == goal:
                # Build path edges
                path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                return path, path_edges, visited_edges
            neighbors = graph.get(node, [])
            neighbors = sorted(neighbors) if order == "asc" else sorted(neighbors, reverse=True)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                visited_edges.append((node, neighbor))
    return None, [], visited_edges