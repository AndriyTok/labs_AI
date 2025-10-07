def dfs(graph, start, goal, order="asc"):
    stack = [[start]]
    visited = set()  # Start empty
    visited_edges = []

    while stack:
        path = stack.pop()
        current = path[-1]

        # Add to visited only when processing
        visited.add(current)

        # Goal check
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
            stack_nodes = [p[-1] for p in stack]
            yield path, path_edges, visited_edges, stack_nodes, visited
            return

        # Get neighbors and sort them
        neighbors = sorted(graph[current], reverse=(order == "desc"))

        # Current state visualization
        current_path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        stack_nodes = [p[-1] for p in stack]
        yield path, current_path_edges, visited_edges, stack_nodes, visited

        # Process neighbors
        for neighbor in reversed(neighbors):
            if neighbor not in visited and neighbor not in stack_nodes:
                if neighbor == goal:
                    new_path = path + [neighbor]
                    path_edges = [(new_path[i], new_path[i + 1]) for i in range(len(new_path) - 1)]
                    visited_edges.append((current, neighbor))
                    visited.add(neighbor)
                    stats = {
                        'path_length': len(new_path),
                        'total_explored': len(visited),
                        'efficiency': (len(new_path) / len(visited) * 100)
                    }
                    print(f"!!! TARGET FOUND! Path: {' -> '.join(map(str, new_path))}")
                    print(f"!!! Path length: {stats['path_length']} nodes")
                    print(f"!!! Total nodes explored: {len(visited)}")
                    print(f"!!! Search efficiency: {stats['path_length']}/{len(visited)} = {stats['efficiency']:.1f}%")
                    yield new_path, path_edges, visited_edges, stack_nodes, visited
                    return

                visited_edges.append((current, neighbor))
                new_path = path + [neighbor]
                stack.append(new_path)

    print("!!! No path found")
    print(f"!!! Total nodes explored: {len(visited)}")
    stack_nodes = [p[-1] for p in stack]
    yield [], [], visited_edges, stack_nodes, visited
