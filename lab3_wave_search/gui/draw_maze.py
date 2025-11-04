import matplotlib.pyplot as plt
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
        """Малює лабіринт БЕЗ чисел"""
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
        """Малює шлях на лабіринті"""
        self.draw_maze()

        if path:
            path_y = [p[1] for p in path]
            path_x = [p[0] for p in path]
            self.ax.plot(path_y, path_x, 'y-', linewidth=3, label='Шлях', alpha=0.7)
            self.ax.legend()

        self.canvas.draw()

    def draw_wave_matrix(self, wave_matrix):
        """Малює хвильову матрицю ПОВЕРХ лабіринту"""
        self.ax.clear()

        base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
        base_matrix[self.maze_data.maze == -1] = 0
        self.ax.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

        display_matrix = wave_matrix.copy().astype(float)
        display_matrix[wave_matrix == -1] = np.nan

        im = self.ax.imshow(display_matrix, cmap='viridis', alpha=0.6)

        if len(self.fig.axes) == 1:
            self.fig.colorbar(im, ax=self.ax, label='Хвильові значення')

        for i in range(self.maze_data.size):
            for j in range(self.maze_data.cols):
                if wave_matrix[i, j] >= 0:
                    self.ax.text(j, i, int(wave_matrix[i, j]),
                                 ha='center', va='center', color='white', fontsize=8)

        start_x, start_y = self.maze_data.start_pos
        end_x, end_y = self.maze_data.end_pos
        self.ax.plot(start_y, start_x, 'go', markersize=10, label='Початок')
        self.ax.plot(end_y, end_x, 'ro', markersize=10, label='Кінець')

        self.ax.set_xlim(-0.5, self.maze_data.cols - 0.5)
        self.ax.set_ylim(-0.5, self.maze_data.size - 0.5)
        self.ax.legend()
        self.ax.set_title('Хвильова матриця')
        self.canvas.draw()

    def animate_wave(self, wave_steps):
        """Анімація поширення хвилі ПОВЕРХ лабіринту"""
        import matplotlib.animation as animation

        for ax in self.fig.axes[1:]:
            ax.remove()

        def update(frame):
            self.ax.clear()
            wave = wave_steps[frame]

            base_matrix = np.ones((self.maze_data.size, self.maze_data.cols))
            base_matrix[self.maze_data.maze == -1] = 0
            self.ax.imshow(base_matrix, cmap='gray', vmin=0, vmax=1, alpha=0.3)

            display_matrix = wave.copy().astype(float)
            display_matrix[wave == -1] = np.nan

            im = self.ax.imshow(display_matrix, cmap='viridis', alpha=0.6)

            for i in range(self.maze_data.size):
                for j in range(self.maze_data.cols):
                    if wave[i, j] >= 0:
                        self.ax.text(j, i, int(wave[i, j]),
                                     ha='center', va='center', color='white', fontsize=8)

            start_x, start_y = self.maze_data.start_pos
            end_x, end_y = self.maze_data.end_pos
            self.ax.plot(start_y, start_x, 'go', markersize=10, label='Початок')
            self.ax.plot(end_y, end_x, 'ro', markersize=10, label='Кінець')

            self.ax.set_xlim(-0.5, self.maze_data.cols - 0.5)
            self.ax.set_ylim(-0.5, self.maze_data.size - 0.5)
            self.ax.legend()
            self.ax.set_title(f'Крок {frame + 1}/{len(wave_steps)}')

            return [im]

        anim = animation.FuncAnimation(self.fig, update, frames=len(wave_steps),
                                       interval=300, repeat=False, blit=False)
        self.canvas.draw()
