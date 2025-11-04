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

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, parent_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.canvas.mpl_connect('button_press_event', self.on_click)

    def set_edit_mode(self, mode):
        """Встановлює режим редагування"""
        self.edit_mode = mode

    def on_click(self, event):
        """Обробник кліків мишкою"""
        if event.inaxes != self.ax:
            return

        x = int(round(event.ydata))
        y = int(round(event.xdata))

        if not (0 <= x < self.maze_data.size and 0 <= y < self.maze_data.cols):
            return

        if self.edit_mode == "wall":
            self.maze_data.maze[x, y] = -1
        elif self.edit_mode == "empty":
            self.maze_data.maze[x, y] = 0
        elif self.edit_mode == "start":
            self.maze_data.set_start_position(x, y)
        elif self.edit_mode == "end":
            self.maze_data.set_end_position(x, y)

        self.main_interface.update_visualization()

    def draw_maze(self):
        """Малює лабіринт"""
        self.ax.clear()

        display_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
        display_matrix[self.maze_data.maze == -1] = 0

        self.ax.imshow(display_matrix, cmap='gray', vmin=0, vmax=1)

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
        """Малює шлях з точкою зустрічі"""
        self.draw_maze()

        if path and self.maze_data.meeting_point:
            path_y = [p[1] for p in path]
            path_x = [p[0] for p in path]
            self.ax.plot(path_y, path_x, 'y-', linewidth=3, label='Шлях', alpha=0.7)

            # Позначаємо точку зустрічі
            meet_x, meet_y = self.maze_data.meeting_point
            self.ax.plot(meet_y, meet_x, 'b*', markersize=20, label='Зустріч хвиль')

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

        # Зворотний пошук
        ax2.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

        display_backward = self.maze_data.backward_wave_matrix.copy().astype(float)
        display_backward[display_backward == -1] = np.nan
        ax2.imshow(display_backward, cmap='Reds', alpha=0.6)
        ax2.set_title('Зворотний пошук (від кінця)')

        # Точка зустрічі
        if self.maze_data.meeting_point:
            meet_x, meet_y = self.maze_data.meeting_point
            ax1.plot(meet_y, meet_x, 'g*', markersize=15)
            ax2.plot(meet_y, meet_x, 'g*', markersize=15)

        self.canvas.draw()

    def animate_bidirectional_search(self, combined_steps):
        """Анімація двонаправленого пошуку на одній матриці"""
        if not combined_steps:
            return

        self.ax.clear()

        def update(frame):
            self.ax.clear()

            # Базова матриця
            base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
            base_matrix[self.maze_data.maze == -1] = 0
            self.ax.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

            step = combined_steps[frame]

            # Прямий пошук (синій)
            forward_wave = step['forward'].copy().astype(float)
            forward_wave[forward_wave == -1] = np.nan
            self.ax.imshow(forward_wave, cmap='Blues', alpha=0.4)

            # Зворотний пошук (червоний)
            backward_wave = step['backward'].copy().astype(float)
            backward_wave[backward_wave == -1] = np.nan
            self.ax.imshow(backward_wave, cmap='Reds', alpha=0.4)

            # Позиції
            start_x, start_y = self.maze_data.start_pos
            end_x, end_y = self.maze_data.end_pos

            self.ax.plot(start_y, start_x, 'go', markersize=12, label='Початок')
            self.ax.plot(end_y, end_x, 'ro', markersize=12, label='Кінець')

            # Точка зустрічі
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
                                       interval=400, repeat=False, blit=False)
        self.canvas.draw()
