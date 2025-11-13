import numpy as np
from collections import deque
import time


class UnidirectionalSearch:
    def __init__(self, maze_data, grid):
        self.maze_data = maze_data
        self.grid = grid
        self.search_stats = {}
        self.wave_steps = []

    def search(self, operator_type="4 напрямки", save_steps=False):
        """Виконує однонаправлений хвільовий пошук"""
        start_time = time.time()
        self.wave_steps = []

        # Ініціалізація хвилі
        wave_matrix = np.full((self.maze_data.size, self.maze_data.cols), -1, dtype=int)

        # Початкова позиція
        start_x, start_y = self.maze_data.start_pos
        wave_matrix[start_x, start_y] = 0

        if save_steps:
            self.wave_steps.append(wave_matrix.copy())

        # Черга для пошуку
        queue = deque([self.maze_data.start_pos])
        cycles = 0
        found = False

        # Пошук до кінцевої точки
        while queue and not found:
            level_size = len(queue)

            for _ in range(level_size):
                current_x, current_y = queue.popleft()
                current_distance = wave_matrix[current_x, current_y]

                # Перевірка досягнення цілі
                if (current_x, current_y) == self.maze_data.end_pos:
                    found = True
                    break

                neighbors = self.grid.get_neighbors(current_x, current_y, operator_type)

                for new_x, new_y in neighbors:
                    if (self.maze_data.maze[new_x, new_y] != -1 and
                        wave_matrix[new_x, new_y] == -1):

                        wave_matrix[new_x, new_y] = current_distance + 1
                        queue.append((new_x, new_y))

                        # Перевірка досягнення цілі
                        if (new_x, new_y) == self.maze_data.end_pos:
                            found = True
                            break

                if found:
                    break

            cycles += 1

            if save_steps and not found:
                self.wave_steps.append(wave_matrix.copy())

        # Відновлення шляху
        path = self._reconstruct_path(wave_matrix, operator_type) if found else None
        search_time = time.time() - start_time

        self.search_stats = {
            'path': path,
            'cycles': cycles,
            'time': search_time,
            'length': len(path) if path else 0,
            'operator': operator_type,
            'found': found
        }

        self.maze_data.wave_matrix = wave_matrix
        self.maze_data.current_path = path if path else []

        return path, cycles, search_time

    def _reconstruct_path(self, wave_matrix, operator_type):
        """Відновлює шлях від кінця до початку"""
        path = []
        current = self.maze_data.end_pos

        while current != self.maze_data.start_pos:
            path.append(current)
            current_value = wave_matrix[current[0], current[1]]

            neighbors = self.grid.get_neighbors(current[0], current[1], operator_type)
            found_next = False

            for new_x, new_y in neighbors:
                if (self.maze_data.maze[new_x, new_y] != -1 and
                    wave_matrix[new_x, new_y] >= 0 and
                    wave_matrix[new_x, new_y] == current_value - 1):
                    current = (new_x, new_y)
                    found_next = True
                    break

            if not found_next:
                return None

        path.append(self.maze_data.start_pos)
        path.reverse()
        return path

    def get_stats(self):
        return self.search_stats

    def get_wave_steps(self):
        return self.wave_steps