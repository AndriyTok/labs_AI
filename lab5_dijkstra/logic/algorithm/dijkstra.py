# lab5_dijkstra/logic/algorithm/dijkstra.py
import heapq


def dijkstra_search(graph, start, end):
    """
    Знаходить найкоротший шлях (швидка версія).
    Повертає (path, distance, cycles).
    """
    if start not in graph or end not in graph:
        return None, float('inf'), 0

    pq = [(0, start)]
    min_distances = {city: float('inf') for city in graph.nodes}
    min_distances[start] = 0
    predecessors = {city: None for city in graph.nodes}

    cycles = 0
    visited = set()

    while pq:
        cycles += 1
        current_dist, current_city = heapq.heappop(pq)

        if current_city in visited:
            continue
        visited.add(current_city)

        if current_city == end:
            break

        for neighbor in graph.neighbors(current_city):
            if neighbor not in visited:
                weight = graph[current_city][neighbor].get('weight', 1)
                new_dist = current_dist + weight

                if new_dist < min_distances[neighbor]:
                    min_distances[neighbor] = new_dist
                    predecessors[neighbor] = current_city
                    heapq.heappush(pq, (new_dist, neighbor))

    path = []
    if min_distances[end] != float('inf'):
        city = end
        while city is not None:
            path.insert(0, city)
            city = predecessors[city]

    if path and path[0] == start:
        return path, min_distances[end], cycles
    else:
        return None, float('inf'), cycles


def dijkstra_search_animated(graph, start, end):
    """
    Виконує пошук і повертає кроки для анімації.
    Повертає (steps, final_path, final_distance)
    """
    if start not in graph or end not in graph:
        return [], None, float('inf')

    pq = [(0, start)]
    min_distances = {city: float('inf') for city in graph.nodes}
    min_distances[start] = 0
    predecessors = {city: None for city in graph.nodes}
    visited = set()

    steps = []

    while pq:
        current_dist, current_city = heapq.heappop(pq)

        if current_city in visited:
            continue
        visited.add(current_city)

        neighbors_to_check = []
        for neighbor in graph.neighbors(current_city):
            if neighbor not in visited:
                neighbors_to_check.append(neighbor)
                weight = graph[current_city][neighbor].get('weight', 1)
                new_dist = current_dist + weight

                if new_dist < min_distances[neighbor]:
                    min_distances[neighbor] = new_dist
                    predecessors[neighbor] = current_city  # FIX: було neighbor
                    heapq.heappush(pq, (new_dist, neighbor))

        # Додаємо крок: (відвідані, всі відстані, поточна, сусіди)
        steps.append((
            visited.copy(),
            min_distances.copy(),
            current_city,
            neighbors_to_check.copy()
        ))

        if current_city == end:
            break

    # Відновлення шляху
    path = []
    if min_distances[end] != float('inf'):
        city = end
        while city is not None:
            path.insert(0, city)
            city = predecessors[city]

    final_path = path if (path and path[0] == start) else None
    return steps, final_path, min_distances[end]
