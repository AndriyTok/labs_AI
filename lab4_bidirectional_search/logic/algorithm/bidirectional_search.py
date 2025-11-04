import numpy as np
from collections import deque
import time


class BidirectionalSearch:
    def __init__(self, maze_data, grid):
        self.maze_data = maze_data
        self.grid = grid
        self.search_stats = {}
        self.combined_steps = []

    def search(self, operator_type="4 напрямки", save_steps=False):
        """Виконує двонаправлений хвільовий пошук"""
        start_time = time.time()
        self.combined_steps = []

        # Ініціалізація хвиль
        forward_wave = np.full((self.maze_data.size, self.maze_data.cols), -1, dtype=int)
        backward_wave = np.full((self.maze_data.size, self.maze_data.cols), -1, dtype=int)

        # Початкові позиції
        start_x, start_y = self.maze_data.start_pos
        end_x, end_y = self.maze_data.end_pos

        forward_wave[start_x, start_y] = 0
        backward_wave[end_x, end_y] = 0

        if save_steps:
            self.combined_steps.append({
                'forward': forward_wave.copy(),
                'backward': backward_wave.copy()
            })

        # Черги для обох напрямків
        forward_queue = deque([self.maze_data.start_pos])
        backward_queue = deque([self.maze_data.end_pos])

        cycles_forward = 0
        cycles_backward = 0
        meeting_point = None

        # Двонаправлений пошук
        while (forward_queue or backward_queue) and meeting_point is None:
            # Прямий пошук
            if forward_queue:
                level_size = len(forward_queue)
                for _ in range(level_size):
                    current_x, current_y = forward_queue.popleft()
                    current_distance = forward_wave[current_x, current_y]

                    # Перевірка зустрічі на поточній вершині
                    if backward_wave[current_x, current_y] >= 0 and (current_x, current_y) != self.maze_data.start_pos:
                        meeting_point = (current_x, current_y)
                        break

                    neighbors = self.grid.get_neighbors(current_x, current_y, operator_type)

                    for new_x, new_y in neighbors:
                        if self.maze_data.maze[new_x, new_y] != -1:
                            if forward_wave[new_x, new_y] == -1:
                                forward_wave[new_x, new_y] = current_distance + 1
                                forward_queue.append((new_x, new_y))

                                # Перевірка зустрічі одразу після додавання
                                if backward_wave[new_x, new_y] >= 0:
                                    meeting_point = (new_x, new_y)
                                    break

                    if meeting_point:
                        break

                cycles_forward += 1

                if save_steps and not meeting_point:
                    self.combined_steps.append({
                        'forward': forward_wave.copy(),
                        'backward': backward_wave.copy()
                    })

            if meeting_point:
                break

            # Зворотний пошук
            if backward_queue:
                level_size = len(backward_queue)
                for _ in range(level_size):
                    current_x, current_y = backward_queue.popleft()
                    current_distance = backward_wave[current_x, current_y]

                    # Перевірка зустрічі на поточній вершині
                    if forward_wave[current_x, current_y] >= 0 and (current_x, current_y) != self.maze_data.end_pos:
                        meeting_point = (current_x, current_y)
                        break

                    neighbors = self.grid.get_neighbors(current_x, current_y, operator_type)

                    for new_x, new_y in neighbors:
                        if self.maze_data.maze[new_x, new_y] != -1:
                            if backward_wave[new_x, new_y] == -1:
                                backward_wave[new_x, new_y] = current_distance + 1
                                backward_queue.append((new_x, new_y))

                                # Перевірка зустрічі одразу після додавання
                                if forward_wave[new_x, new_y] >= 0:
                                    meeting_point = (new_x, new_y)
                                    break

                    if meeting_point:
                        break

                cycles_backward += 1

                if save_steps and not meeting_point:
                    self.combined_steps.append({
                        'forward': forward_wave.copy(),
                        'backward': backward_wave.copy()
                    })

        # Відновлення шляху
        path = self._reconstruct_path(forward_wave, backward_wave, operator_type, meeting_point)
        search_time = time.time() - start_time

        self.search_stats = {
            'path': path,
            'cycles_forward': cycles_forward,
            'cycles_backward': cycles_backward,
            'total_cycles': cycles_forward + cycles_backward,
            'time': search_time,
            'length': len(path) if path else 0,
            'operator': operator_type,
            'meeting_point': meeting_point
        }

        self.maze_data.forward_wave_matrix = forward_wave
        self.maze_data.backward_wave_matrix = backward_wave
        self.maze_data.meeting_point = meeting_point
        self.maze_data.current_path = path if path else []

        return path, cycles_forward, cycles_backward, search_time, meeting_point

    def _reconstruct_path(self, forward_wave, backward_wave, operator_type, meeting_point):
        """Відновлює шлях від початку до кінця через точку зустрічі"""
        if meeting_point is None:
            return None

        # Шлях від початку до точки зустрічі
        forward_path = []
        current = meeting_point

        while current != self.maze_data.start_pos:
            forward_path.append(current)
            current_value = forward_wave[current[0], current[1]]

            neighbors = self.grid.get_neighbors(current[0], current[1], operator_type)
            found_next = False

            for new_x, new_y in neighbors:
                if (self.maze_data.maze[new_x, new_y] != -1 and
                        forward_wave[new_x, new_y] >= 0 and
                        forward_wave[new_x, new_y] == current_value - 1):
                    current = (new_x, new_y)
                    found_next = True
                    break

            if not found_next:
                return None

        forward_path.append(self.maze_data.start_pos)
        forward_path.reverse()

        # Шлях від точки зустрічі до кінця
        backward_path = []
        current = meeting_point
        current_value = backward_wave[meeting_point[0], meeting_point[1]]

        while current != self.maze_data.end_pos:
            neighbors = self.grid.get_neighbors(current[0], current[1], operator_type)
            found_next = False

            for new_x, new_y in neighbors:
                if (self.maze_data.maze[new_x, new_y] != -1 and
                        backward_wave[new_x, new_y] >= 0 and
                        backward_wave[new_x, new_y] == current_value - 1):
                    current = (new_x, new_y)
                    current_value = backward_wave[new_x, new_y]
                    backward_path.append(current)
                    found_next = True
                    break

            if not found_next:
                return None

        # Об'єднання шляхів (без дублювання точки зустрічі)
        full_path = forward_path + backward_path

        return full_path

    def get_stats(self):
        return self.search_stats

    def get_combined_steps(self):
        return self.combined_steps
