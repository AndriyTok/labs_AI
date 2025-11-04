import tkinter as tk
from tkinter import ttk

from lab3_wave_search.logic.maze.init_maze import MazeInitializer


class MazeEditor:
    def __init__(self, parent_frame, maze_data, main_interface):
        self.parent_frame = parent_frame
        self.maze_data = maze_data
        self.main_interface = main_interface

        self.create_widgets()

    def create_widgets(self):
        edit_frame = ttk.LabelFrame(self.parent_frame, text="Редагування лабіринту")
        edit_frame.pack(fill=tk.X, pady=10)

        # Розмір сітки (рядки)
        rows_frame = ttk.Frame(edit_frame)
        rows_frame.pack(fill=tk.X, pady=5)
        ttk.Label(rows_frame, text="Рядки (X):").pack(side=tk.LEFT)

        self.rows_var = tk.IntVar(value=self.maze_data.size)
        rows_spinbox = ttk.Spinbox(rows_frame, from_=10, to=30,
                                   textvariable=self.rows_var, width=10)
        rows_spinbox.pack(side=tk.RIGHT)

        # Розмір сітки (стовпці)
        cols_frame = ttk.Frame(edit_frame)
        cols_frame.pack(fill=tk.X, pady=5)
        ttk.Label(cols_frame, text="Стовпці (Y):").pack(side=tk.LEFT)

        self.cols_var = tk.IntVar(value=self.maze_data.cols)
        cols_spinbox = ttk.Spinbox(cols_frame, from_=10, to=30,
                                   textvariable=self.cols_var, width=10)
        cols_spinbox.pack(side=tk.RIGHT)

        # Кнопки
        ttk.Button(edit_frame, text="Застосувати розмір",
                   command=self.update_size).pack(fill=tk.X, pady=2)

        ttk.Button(edit_frame, text="Генерувати випадковий",
                   command=self.generate_random).pack(fill=tk.X, pady=2)

        ttk.Button(edit_frame, text="Очистити лабіринт",
                   command=self.clear_maze).pack(fill=tk.X, pady=2)

        # Режими редагування
        mode_frame = ttk.LabelFrame(edit_frame, text="Режим кліку мишкою")
        mode_frame.pack(fill=tk.X, pady=5)

        ttk.Button(mode_frame, text="Стінка",
                   command=lambda: self.set_edit_mode("wall")).pack(fill=tk.X, pady=1)
        ttk.Button(mode_frame, text="Порожня клітинка",
                   command=lambda: self.set_edit_mode("empty")).pack(fill=tk.X, pady=1)
        ttk.Button(mode_frame, text="Початок",
                   command=lambda: self.set_edit_mode("start")).pack(fill=tk.X, pady=1)
        ttk.Button(mode_frame, text="Кінець",
                   command=lambda: self.set_edit_mode("end")).pack(fill=tk.X, pady=1)

    def set_edit_mode(self, mode):
        """Встановлює режим редагування"""
        if hasattr(self.main_interface, 'maze_drawer'):
            self.main_interface.maze_drawer.set_edit_mode(mode)
            self.main_interface.update_visualization()

    def update_size(self):
        """Оновлює розмір лабіринту"""
        new_rows = self.rows_var.get()
        new_cols = self.cols_var.get()
        self.maze_data.set_size(new_rows, new_cols)
        self.main_interface.update_visualization()

    def generate_random(self):
        """Генерує випадковий лабіринт"""
        self.maze_data.generate_random_maze()
        self.main_interface.update_visualization()

    def clear_maze(self):
        """Очищає лабіринт"""
        self.maze_data.maze = MazeInitializer.create_empty_maze(
            self.maze_data.size, self.maze_data.cols)
        self.main_interface.update_visualization()
