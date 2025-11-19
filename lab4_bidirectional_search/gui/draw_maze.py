import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class MazeDrawer:
    def __init__(self, parent_frame, maze_data, main_interface):
        self.parent_frame = parent_frame
        self.maze_data = maze_data
        self.main_interface = main_interface
        self.edit_mode = "wall"

        # Створення matplotlib фігури
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, parent_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Підключення кліку миші
        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.draw_maze()

    def set_edit_mode(self, mode):
        self.edit_mode = mode

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        col = int(round(event.xdata))
        row = int(round(event.ydata))

        if (0 <= row < self.maze_data.size and 0 <= col < self.maze_data.cols):
            if self.edit_mode == "wall":
                self.maze_data.maze[row, col] = -1
            elif self.edit_mode == "empty":
                self.maze_data.maze[row, col] = 0
            elif self.edit_mode == "start":
                self.maze_data.set_start_position(row, col)
            elif self.edit_mode == "end":
                self.maze_data.set_end_position(row, col)

            self.draw_maze()

    def draw_maze(self):
        """Малює базовий лабіринт"""
        self.ax.clear()

        # Основа лабіринту
        self.ax.imshow(self.maze_data.maze, cmap='gray', vmin=-1, vmax=1)

        # Позначення початку і кінця
        start_x, start_y = self.maze_data.start_pos
        end_x, end_y = self.maze_data.end_pos

        self.ax.plot(start_y, start_x, 'go', markersize=15, label='Початок')
        self.ax.plot(end_y, end_x, 'ro', markersize=15, label='Кінець')

        self.ax.set_xlim(-0.5, self.maze_data.cols - 0.5)
        self.ax.set_ylim(-0.5, self.maze_data.size - 0.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.ax.set_title(f'Лабіринт (режим: {self.edit_mode})')

        self.canvas.draw()

    def draw_path(self, path):
        """Малює шлях з точкою зустрічі (якщо є)"""
        self.draw_maze()

        if not path:
            self.canvas.draw()
            return

        mp = self.maze_data.meeting_point

        # Двонаправлена візуалізація тільки якщо є точка зустрічі І вона в шляху
        if mp and mp in path:
            meeting_idx = path.index(mp)

            # Прямий шлях
            forward_path = path[:meeting_idx + 1]
            if len(forward_path) > 1:
                forward_x = [pos[0] for pos in forward_path]
                forward_y = [pos[1] for pos in forward_path]
                self.ax.plot(forward_y, forward_x, 'b-', linewidth=3, alpha=0.7, label='Прямий шлях')

            # Зворотний шлях
            backward_path = path[meeting_idx:]
            if len(backward_path) > 1:
                backward_x = [pos[0] for pos in backward_path]
                backward_y = [pos[1] for pos in backward_path]
                self.ax.plot(backward_y, backward_x, 'r-', linewidth=3, alpha=0.7, label='Зворотний шлях')

            # Точка зустрічі
            meet_x, meet_y = mp
            self.ax.plot(meet_y, meet_x, 'y*', markersize=20, label='Зустріч')
        else:
            # Однонаправлений шлях (зелений)
            path_x = [pos[0] for pos in path]
            path_y = [pos[1] for pos in path]
            self.ax.plot(path_y, path_x, 'g-', linewidth=3, alpha=0.7, label='Шлях')

        self.ax.legend()
        self.canvas.draw()

    def draw_bidirectional_waves(self):
        """Малює обидві хвильові матриці"""
        if self.maze_data.forward_wave_matrix is None or self.maze_data.backward_wave_matrix is None:
            return

        self.fig.clear()

        # Два підграфіки
        ax1 = self.fig.add_subplot(121)
        ax2 = self.fig.add_subplot(122)

        # Прямий пошук
        base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
        base_matrix[self.maze_data.maze == -1] = 0
        ax1.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

        display_forward = self.maze_data.forward_wave_matrix.copy().astype(float)
        display_forward[display_forward == -1] = np.nan
        ax1.imshow(display_forward, cmap='Blues', alpha=0.6)
        ax1.set_title('Прямий пошук (від початку)')

        # Додавання чисел для прямого пошуку
        for i in range(self.maze_data.size):
            for j in range(self.maze_data.cols):
                if self.maze_data.forward_wave_matrix[i, j] >= 0:
                    ax1.text(j, i, str(self.maze_data.forward_wave_matrix[i, j]),
                             ha='center', va='center', fontsize=8, color='white', weight='bold')

        # Зворотний пошук
        ax2.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

        display_backward = self.maze_data.backward_wave_matrix.copy().astype(float)
        display_backward[display_backward == -1] = np.nan
        ax2.imshow(display_backward, cmap='Reds', alpha=0.6)
        ax2.set_title('Зворотний пошук (від кінця)')

        # Додавання чисел для зворотного пошуку
        for i in range(self.maze_data.size):
            for j in range(self.maze_data.cols):
                if self.maze_data.backward_wave_matrix[i, j] >= 0:
                    ax2.text(j, i, str(self.maze_data.backward_wave_matrix[i, j]),
                             ha='center', va='center', fontsize=8, color='white', weight='bold')

        # Точка зустрічі
        if self.maze_data.meeting_point:
            meet_x, meet_y = self.maze_data.meeting_point
            ax1.plot(meet_y, meet_x, 'y*', markersize=15)
            ax2.plot(meet_y, meet_x, 'y*', markersize=15)

        self.canvas.draw()

    def draw_unidirectional_wave(self):
        """Малює хвильову матрицю однонаправленого пошуку"""
        if not hasattr(self.maze_data, 'wave_matrix') or self.maze_data.wave_matrix is None:
            return

        self.ax.clear()

        # Базовий лабіринт
        base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
        base_matrix[self.maze_data.maze == -1] = 0
        self.ax.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

        # Хвильова матриця
        display_wave = self.maze_data.wave_matrix.copy().astype(float)
        display_wave[display_wave == -1] = np.nan
        self.ax.imshow(display_wave, cmap='Greens', alpha=0.6)

        # Додавання чисел
        for i in range(self.maze_data.size):
            for j in range(self.maze_data.cols):
                if self.maze_data.wave_matrix[i, j] >= 0:
                    self.ax.text(j, i, str(self.maze_data.wave_matrix[i, j]),
                                 ha='center', va='center', fontsize=10, color='white', weight='bold')

        # Позначення початку і кінця
        start_x, start_y = self.maze_data.start_pos
        end_x, end_y = self.maze_data.end_pos
        self.ax.plot(start_y, start_x, 'go', markersize=15, label='Початок')
        self.ax.plot(end_y, end_x, 'ro', markersize=15, label='Кінець')

        self.ax.set_xlim(-0.5, self.maze_data.cols - 0.5)
        self.ax.set_ylim(-0.5, self.maze_data.size - 0.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.ax.set_title('Однонаправлений хвильовий пошук')

        self.canvas.draw()

    def animate_bidirectional_search(self, combined_steps):
        """Анімація двонаправленого пошуку з числами та шляхом"""
        if not combined_steps:
            return

        self.ax.clear()
        path = self.maze_data.current_path if hasattr(self.maze_data, 'current_path') else []

        def update(frame):
            self.ax.clear()

            # Базовий лабіринт
            base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
            base_matrix[self.maze_data.maze == -1] = 0
            self.ax.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

            # Поточний крок
            current_step = combined_steps[frame]

            # Прямий пошук (синій)
            forward_wave = current_step['forward'].copy().astype(float)
            forward_wave[forward_wave == -1] = np.nan
            self.ax.imshow(forward_wave, cmap='Blues', alpha=0.4)

            # Зворотний пошук (червоний)
            backward_wave = current_step['backward'].copy().astype(float)
            backward_wave[backward_wave == -1] = np.nan
            self.ax.imshow(backward_wave, cmap='Reds', alpha=0.4)

            # Малюємо шлях на останньому кадрі
            if path and frame == len(combined_steps) - 1:
                mp = self.maze_data.meeting_point
                if mp and mp in path:
                    meeting_idx = path.index(mp)

                    # Прямий шлях
                    forward_path = path[:meeting_idx + 1]
                    if len(forward_path) > 1:
                        forward_x = [pos[0] for pos in forward_path]
                        forward_y = [pos[1] for pos in forward_path]
                        self.ax.plot(forward_y, forward_x, 'b-', linewidth=3, alpha=0.7)

                    # Зворотний шлях
                    backward_path = path[meeting_idx:]
                    if len(backward_path) > 1:
                        backward_x = [pos[0] for pos in backward_path]
                        backward_y = [pos[1] for pos in backward_path]
                        self.ax.plot(backward_y, backward_x, 'r-', linewidth=3, alpha=0.7)

            # Додавання чисел
            for i in range(self.maze_data.size):
                for j in range(self.maze_data.cols):
                    # Прямі числа (сині)
                    if current_step['forward'][i, j] >= 0:
                        self.ax.text(j - 0.15, i - 0.15, str(current_step['forward'][i, j]),
                                     ha='center', va='center', fontsize=8, color='blue', weight='bold')

                    # Зворотні числа (червоні)
                    if current_step['backward'][i, j] >= 0:
                        self.ax.text(j + 0.15, i + 0.15, str(current_step['backward'][i, j]),
                                     ha='center', va='center', fontsize=8, color='red', weight='bold')

            # Позначення початку і кінця
            start_x, start_y = self.maze_data.start_pos
            end_x, end_y = self.maze_data.end_pos
            self.ax.plot(start_y, start_x, 'go', markersize=12, label='Початок')
            self.ax.plot(end_y, end_x, 'ro', markersize=12, label='Кінець')

            # Точка зустрічі на останньому кадрі
            if self.maze_data.meeting_point and frame == len(combined_steps) - 1:
                meet_x, meet_y = self.maze_data.meeting_point
                self.ax.plot(meet_y, meet_x, 'y*', markersize=20, label='Зустріч')

            self.ax.set_xlim(-0.5, self.maze_data.cols - 0.5)
            self.ax.set_ylim(-0.5, self.maze_data.size - 0.5)
            self.ax.set_aspect('equal')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            self.ax.set_title(f'Двонаправлений пошук (крок {frame + 1}/{len(combined_steps)})')

            return [self.ax]

        anim = animation.FuncAnimation(self.fig, update, frames=len(combined_steps),
                                       interval=200, repeat=False, blit=False)
        self.canvas.draw()

    def animate_unidirectional_search(self, wave_steps):
        """Анімація однонаправленого пошуку з числами та шляхом"""
        if not wave_steps:
            return

        self.ax.clear()
        path = self.maze_data.current_path if hasattr(self.maze_data, 'current_path') else []

        def update(frame):
            self.ax.clear()

            # Базовий лабіринт
            base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
            base_matrix[self.maze_data.maze == -1] = 0
            self.ax.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

            # Поточна хвильова матриця
            current_wave = wave_steps[frame].copy().astype(float)
            current_wave[current_wave == -1] = np.nan
            self.ax.imshow(current_wave, cmap='Greens', alpha=0.6)

            # Малюємо шлях на останньому кадрі
            if path and frame == len(wave_steps) - 1:
                path_x = [pos[0] for pos in path]
                path_y = [pos[1] for pos in path]
                self.ax.plot(path_y, path_x, 'g-', linewidth=3, alpha=0.9)

            # Додавання чисел
            for i in range(self.maze_data.size):
                for j in range(self.maze_data.cols):
                    if wave_steps[frame][i, j] >= 0:
                        self.ax.text(j, i, str(wave_steps[frame][i, j]),
                                     ha='center', va='center', fontsize=10, color='white', weight='bold')

            # Позначення початку і кінця
            start_x, start_y = self.maze_data.start_pos
            end_x, end_y = self.maze_data.end_pos
            self.ax.plot(start_y, start_x, 'go', markersize=15, label='Початок')
            self.ax.plot(end_y, end_x, 'ro', markersize=15, label='Кінець')

            self.ax.set_xlim(-0.5, self.maze_data.cols - 0.5)
            self.ax.set_ylim(-0.5, self.maze_data.size - 0.5)
            self.ax.set_aspect('equal')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            self.ax.set_title(f'Однонаправлений пошук (крок {frame + 1}/{len(wave_steps)})')

            return [self.ax]

        anim = animation.FuncAnimation(self.fig, update, frames=len(wave_steps),
                                       interval=200, repeat=False, blit=False)
        self.canvas.draw()

    def reset_visualization(self):
        """Скидає візуалізацію до базового лабіринту"""
        self.ax.clear()
        self.draw_maze()
