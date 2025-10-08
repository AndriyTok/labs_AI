def dfs(graph, start, goal, order="asc"):
    stack = [[start]]
    visited = set()
    visited_edges = []
    stack_nodes = {start}  # Add this line to track stack nodes separately

    while stack:
        path = stack.pop()
        current = path[-1]
        stack_nodes.remove(current)  # Remove from stack nodes when processing

        visited.add(current)

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
            yield path, path_edges, visited_edges, list(stack_nodes), visited
            return

        neighbors = sorted(graph[current], reverse=(order == "desc"))
        current_path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        yield path, current_path_edges, visited_edges, list(stack_nodes), visited

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
                    yield new_path, path_edges, visited_edges, list(stack_nodes), visited
                    return

                visited_edges.append((current, neighbor))
                new_path = path + [neighbor]
                stack.append(new_path)
                stack_nodes.add(neighbor)  # Add to stack nodes when pushing

    print("!!! No path found")
    print(f"!!! Total nodes explored: {len(visited)}")
    yield [], [], visited_edges, list(stack_nodes), visited
