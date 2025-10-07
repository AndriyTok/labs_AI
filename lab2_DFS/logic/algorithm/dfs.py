def dfs(graph, start, goal, order="asc"):
            stack = [[start]]
            visited = {start}
            visited_edges = []

            while stack:
                path = stack.pop()  # DFS uses pop() instead of pop(0)
                current = path[-1]

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
                    print(f"!!! Total nodes explored: {stats['total_explored']}")
                    print(f"!!! Search efficiency: {stats['path_length']}/{stats['total_explored']} = {stats['efficiency']:.1f}%")
                    stack_nodes = [p[-1] for p in stack]  # Keep track of remaining stack nodes
                    yield path, path_edges, visited_edges, stack_nodes
                    return

                # Get neighbors and sort them
                neighbors = sorted(graph[current], reverse=(order == "desc"))

                # Current state visualization
                current_path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                stack_nodes = [p[-1] for p in stack]
                yield path, current_path_edges, visited_edges, stack_nodes

                # Process neighbors
                for neighbor in reversed(neighbors):  # Reverse to maintain correct DFS order
                    if neighbor not in visited:
                        visited.add(neighbor)
                        visited_edges.append((current, neighbor))
                        new_path = path + [neighbor]
                        stack.append(new_path)

            print("!!! No path found")
            print(f"!!! Total nodes explored: {len(visited)}")
            stack_nodes = [p[-1] for p in stack]  # This will be empty but keeps the consistent return format
            yield [], [], visited_edges, stack_nodes