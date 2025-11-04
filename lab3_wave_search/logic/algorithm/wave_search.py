import numpy as np
from collections import deque
import time


class WaveSearch:
    def __init__(self, maze_data, grid):
        self.maze_data = maze_data
        self.grid = grid
        self.search_stats = {}
        self.wave_steps = []

    def search(self, operator_type="4 напрямки", save_steps=False):
        """Виконує хвільовий пошук"""
        start_time = time.time()
        self.wave_steps = []

        wave = np.full((self.maze_data.size, self.maze_data.cols), np.inf, dtype=float)

        # Копіюємо перешкоди
        for i in range(self.maze_data.size):
            for j in range(self.maze_data.cols):
                if self.maze_data.maze[i, j] == -1:
                    wave[i, j] = -1

        wave[self.maze_data.start_pos[0], self.maze_data.start_pos[1]] = 0

        queue = deque([self.maze_data.start_pos])
        cycles = 0

        while queue:
            current = queue.popleft()
            cycles += 1

            if save_steps:
                step_wave = wave.copy()
                step_wave[np.isinf(step_wave)] = -1
                self.wave_steps.append(step_wave)

            if current == self.maze_data.end_pos:
                break

            current_value = wave[current[0], current[1]]
            neighbors = self.grid.get_neighbors(current[0], current[1], operator_type)

            for new_x, new_y in neighbors:
                if self.maze_data.maze[new_x, new_y] != -1 and np.isinf(wave[new_x, new_y]):
                    wave[new_x, new_y] = current_value + 1
                    queue.append((new_x, new_y))

        wave[np.isinf(wave)] = -1

        path = self._reconstruct_path(wave, operator_type)
        search_time = time.time() - start_time

        self.search_stats = {
            'path': path,
            'cycles': cycles,
            'time': search_time,
            'length': len(path) if path else 0,
            'operator': operator_type
        }

        self.maze_data.wave_matrix = wave
        self.maze_data.current_path = path if path else []

        return path, cycles, search_time

    def _reconstruct_path(self, wave, operator_type):
        """Відновлює шлях ТІЛЬКИ по порожніх клітинках"""
        end_value = wave[self.maze_data.end_pos[0], self.maze_data.end_pos[1]]

        if end_value == -1:
            return None

        path = []
        current = self.maze_data.end_pos

        while current != self.maze_data.start_pos:
            path.append(current)
            current_value = wave[current[0], current[1]]

            neighbors = self.grid.get_neighbors(current[0], current[1], operator_type)
            found_next = False

            for new_x, new_y in neighbors:
                # ПЕРЕВІРЯЄМО: не стінка в maze І значення менше на 1
                if (self.maze_data.maze[new_x, new_y] != -1 and
                        wave[new_x, new_y] >= 0 and
                        wave[new_x, new_y] == current_value - 1):
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
