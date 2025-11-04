import numpy as np


class MazeData:
    def __init__(self, rows=20, cols=20):
        self.size = rows
        self.cols = cols
        self.maze = np.zeros((rows, cols))
        self.start_pos = (0, 0)
        self.end_pos = (rows - 1, cols - 1)
        self.current_path = []
        self.forward_wave_matrix = None
        self.backward_wave_matrix = None
        self.meeting_point = None

    def generate_random_maze(self, obstacle_probability=0.3):
        """Генерує випадковий лабіринт"""
        self.maze = np.random.choice([0, -1], size=(self.size, self.cols),
                                     p=[1 - obstacle_probability, obstacle_probability])
        self.maze[self.start_pos[0], self.start_pos[1]] = 0
        self.maze[self.end_pos[0], self.end_pos[1]] = 0

    def set_size(self, new_rows, new_cols):
        """Змінює розмір лабіринту"""
        self.size = new_rows
        self.cols = new_cols
        self.maze = np.zeros((new_rows, new_cols))
        self.end_pos = (new_rows - 1, new_cols - 1)
        if self.start_pos[0] >= new_rows or self.start_pos[1] >= new_cols:
            self.start_pos = (0, 0)

    def is_valid_position(self, x, y):
        """Перевіряє валідність позиції"""
        return (0 <= x < self.size and
                0 <= y < self.cols and
                self.maze[x, y] != -1)

    def set_start_position(self, x, y):
        """Встановлює початкову позицію"""
        if 0 <= x < self.size and 0 <= y < self.cols:
            self.maze[x, y] = 0
            self.start_pos = (x, y)

    def set_end_position(self, x, y):
        """Встановлює кінцеву позицію"""
        if 0 <= x < self.size and 0 <= y < self.cols:
            self.maze[x, y] = 0
            self.end_pos = (x, y)