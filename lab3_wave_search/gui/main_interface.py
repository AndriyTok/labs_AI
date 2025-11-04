import tkinter as tk
from tkinter import ttk

from lab3_wave_search.gui.draw_maze import MazeDrawer
from lab3_wave_search.gui.edit_maze import MazeEditor
from lab3_wave_search.gui.run_wave import WaveRunner


class MainInterface:
    def __init__(self, root, maze_data, grid, wave_search):
        self.root = root
        self.maze_data = maze_data
        self.grid = grid
        self.wave_search = wave_search

        self.create_widgets()

        # Ініціалізація компонентів (БЕЗ position_editor)
        self.maze_drawer = MazeDrawer(self.viz_frame, self.maze_data, self)
        self.maze_editor = MazeEditor(self.control_frame, self.maze_data, self)
        self.wave_runner = WaveRunner(self.control_frame, self.wave_search,
                                      self.maze_data, self)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.control_frame = ttk.Frame(main_frame, width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.control_frame.pack_propagate(False)

        self.viz_frame = ttk.Frame(main_frame)
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_visualization(self):
        """Оновлює візуалізацію"""
        if hasattr(self, 'maze_drawer'):
            self.maze_drawer.draw_maze()

    def show_path(self, path):
        """Відображає знайдений шлях"""
        if hasattr(self, 'maze_drawer'):
            self.maze_drawer.draw_path(path)
