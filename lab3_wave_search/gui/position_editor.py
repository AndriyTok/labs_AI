import tkinter as tk
from tkinter import ttk


class PositionEditor:
    def __init__(self, parent_frame, maze_data, main_interface):
        self.parent_frame = parent_frame
        self.maze_data = maze_data
        self.main_interface = main_interface

        self.create_widgets()

    def create_widgets(self):
        pos_frame = ttk.LabelFrame(self.parent_frame, text="Позиції")
        pos_frame.pack(fill=tk.X, pady=10)

        # Початкова позиція
        start_frame = ttk.Frame(pos_frame)
        start_frame.pack(fill=tk.X, pady=5)
        ttk.Label(start_frame, text="Початок (x,y):").pack(side=tk.LEFT)

        self.start_x_var = tk.IntVar(value=self.maze_data.start_pos[0])
        self.start_y_var = tk.IntVar(value=self.maze_data.start_pos[1])

        ttk.Spinbox(start_frame, from_=0, to=self.maze_data.size - 1,
                    textvariable=self.start_x_var, width=5,
                    command=self.update_start).pack(side=tk.RIGHT, padx=2)
        ttk.Spinbox(start_frame, from_=0, to=self.maze_data.cols - 1,
                    textvariable=self.start_y_var, width=5,
                    command=self.update_start).pack(side=tk.RIGHT)

        # Кінцева позиція
        end_frame = ttk.Frame(pos_frame)
        end_frame.pack(fill=tk.X, pady=5)
        ttk.Label(end_frame, text="Кінець (x,y):").pack(side=tk.LEFT)

        self.end_x_var = tk.IntVar(value=self.maze_data.end_pos[0])
        self.end_y_var = tk.IntVar(value=self.maze_data.end_pos[1])

        ttk.Spinbox(end_frame, from_=0, to=self.maze_data.size - 1,
                    textvariable=self.end_x_var, width=5,
                    command=self.update_end).pack(side=tk.RIGHT, padx=2)
        ttk.Spinbox(end_frame, from_=0, to=self.maze_data.cols - 1,
                    textvariable=self.end_y_var, width=5,
                    command=self.update_end).pack(side=tk.RIGHT)

    def update_start(self):
        """Оновлює початкову позицію"""
        x, y = self.start_x_var.get(), self.start_y_var.get()
        self.maze_data.set_start_position(x, y)
        self.main_interface.update_visualization()

    def update_end(self):
        """Оновлює кінцеву позицію"""
        x, y = self.end_x_var.get(), self.end_y_var.get()
        self.maze_data.set_end_position(x, y)
        self.main_interface.update_visualization()

    def update_position_vars(self):
        """Оновлює змінні позицій після кліку"""
        self.start_x_var.set(self.maze_data.start_pos[0])
        self.start_y_var.set(self.maze_data.start_pos[1])
        self.end_x_var.set(self.maze_data.end_pos[0])
        self.end_y_var.set(self.maze_data.end_pos[1])
