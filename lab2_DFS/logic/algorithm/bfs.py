def bfs(graph, start, goal, order="asc"):
    queue = [[start]]
    visited = {start}
    visited_edges = []

    while queue:
        path = queue.pop(0)
        current = path[-1]

        # Goal check first - before processing neighbors
        if current == goal:
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            stats = {
                'path_length': len(path),
                'total_explored': len(visited),
                'efficiency': (len(path) / len(visited) * 100)
            }
            print(f"!!! TARGET FOUND! Path: {' -> '.join(map(str, path))}")
            print(f"!!! Path length: {stats['path_length']} nodes")
            print(f"!!! Total nodes explored: {len(visited)}")
            print(f"!!! Search efficiency: {stats['path_length']}/{len(visited)} = {stats['efficiency']:.1f}%")
            yield path, path_edges, visited_edges, []
            return

        # Get neighbors and sort them
        neighbors = sorted(graph[current], reverse=(order == "desc"))

        # Current state visualization
        current_path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        queue_nodes = [p[-1] for p in queue]
        yield path, current_path_edges, visited_edges, queue_nodes

        # Process neighbors - mark them visited when adding to queue
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark as visited immediately
                if neighbor == goal:  # Early goal check
                    new_path = path + [neighbor]
                    path_edges = [(new_path[i], new_path[i + 1]) for i in range(len(new_path) - 1)]
                    visited_edges.append((current, neighbor))
                    stats = {
                        'path_length': len(new_path),
                        'total_explored': len(visited),
                        'efficiency': (len(new_path) / len(visited) * 100)
                    }
                    print(f"!!! TARGET FOUND! Path: {' -> '.join(map(str, new_path))}")
                    print(f"!!! Path length: {stats['path_length']} nodes")
                    print(f"!!! Total nodes explored: {len(visited)}")
                    print(f"!!! Search efficiency: {stats['path_length']}/{len(visited)} = {stats['efficiency']:.1f}%")
                    yield new_path, path_edges, visited_edges, []
                    return

                new_path = path + [neighbor]
                queue.append(new_path)
                visited_edges.append((current, neighbor))
                queue_nodes = [p[-1] for p in queue]
                yield path, current_path_edges, visited_edges, queue_nodes

    # No path found
    print("!!! No path found")
    print(f"!!! Total nodes explored: {len(visited)}")
    yield [], [], visited_edges, []
