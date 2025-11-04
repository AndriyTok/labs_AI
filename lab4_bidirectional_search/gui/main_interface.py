import tkinter as tk
from tkinter import ttk

from lab4_bidirectional_search.gui.draw_maze import MazeDrawer
from lab4_bidirectional_search.gui.edit_maze import MazeEditor
from lab4_bidirectional_search.gui.run_bidirectional import BidirectionalRunner


class MainInterface:
    def __init__(self, root, maze_data, grid, bidirectional_search):
        self.root = root
        self.maze_data = maze_data
        self.grid = grid
        self.bidirectional_search = bidirectional_search

        self.create_widgets()

        self.maze_drawer = MazeDrawer(self.viz_frame, self.maze_data, self)
        self.maze_editor = MazeEditor(self.control_frame, self.maze_data, self)
        self.bidirectional_runner = BidirectionalRunner(self.control_frame, self.bidirectional_search,
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