import numpy as np

from lab3_wave_search.logic.maze.types import CellType


class MazeInitializer:
    @staticmethod
    def create_empty_maze(rows, cols):
        """Створює порожній лабіринт"""
        return np.zeros((rows, cols))

    @staticmethod
    def create_random_maze(rows, cols, obstacle_probability=0.3):
        """Створює випадковий лабіринт"""
        maze = np.random.choice([CellType.EMPTY.value, CellType.OBSTACLE.value],
                                size=(rows, cols),
                                p=[1 - obstacle_probability, obstacle_probability])
        maze[0, 0] = CellType.EMPTY.value
        maze[rows - 1, cols - 1] = CellType.EMPTY.value
        return maze

    @staticmethod
    def create_maze_with_pattern(rows, cols, pattern_type="spiral"):
        """Створює лабіринт з певним патерном"""
        maze = np.zeros((rows, cols))

        if pattern_type == "spiral":
            return MazeInitializer._create_spiral_maze(rows, cols)
        elif pattern_type == "cross":
            return MazeInitializer._create_cross_maze(rows, cols)

        return maze

    @staticmethod
    def _create_spiral_maze(rows, cols):
        """Створює спіральний лабіринт"""
        size = min(rows, cols)
        maze = np.ones((rows, cols)) * CellType.OBSTACLE.value

        x, y = rows // 2, cols // 2
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dir_idx = 0
        steps = 1

        maze[x, y] = CellType.EMPTY.value

        while steps < size:
            for _ in range(2):
                dx, dy = directions[dir_idx]
                for _ in range(steps):
                    x, y = x + dx, y + dy
                    if 0 <= x < rows and 0 <= y < cols:
                        maze[x, y] = CellType.EMPTY.value
                dir_idx = (dir_idx + 1) % 4
            steps += 1

        return maze

    @staticmethod
    def _create_cross_maze(rows, cols):
        """Створює хрестоподібний лабіринт"""
        maze = np.ones((rows, cols)) * CellType.OBSTACLE.value

        maze[rows // 2, :] = CellType.EMPTY.value
        maze[:, cols // 2] = CellType.EMPTY.value

        return maze
