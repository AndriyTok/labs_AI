class Grid:
    def __init__(self, maze_data):
        self.maze_data = maze_data

    def get_neighbors(self, x, y, operator_type):
        """Отримує сусідів для заданого типу оператора"""
        operators = {
            "4 напрямки": [(-1, 0), (1, 0), (0, -1), (0, 1)],
            "8 напрямків (діагоналі)": [(-1, -1), (-1, 0), (-1, 1),
                                        (0, -1), (0, 1),
                                        (1, -1), (1, 0), (1, 1)],
            "Комбінований": [(-1, 0), (1, 0), (0, -1), (0, 1),
                             (-1, -1), (-1, 1), (1, -1), (1, 1)]
        }

        moves = operators.get(operator_type, operators["4 напрямки"])
        neighbors = []

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if self.maze_data.is_valid_position(new_x, new_y):
                neighbors.append((new_x, new_y))

        return neighbors
