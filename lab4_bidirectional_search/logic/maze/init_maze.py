import numpy as np
from lab4_bidirectional_search.logic.maze.types import CellType


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