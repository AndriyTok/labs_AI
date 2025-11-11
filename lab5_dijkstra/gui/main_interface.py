# lab5_dijkstra/gui/main_interface.py
import tkinter as tk
from tkinter import ttk
from lab5_dijkstra.gui.draw_graph import GraphDrawer
from lab5_dijkstra.gui.edit_graph import GraphEditor
from lab5_dijkstra.gui.run_dijkstra import DijkstraRunner


class MainInterface:
    def __init__(self, root, graph_data):
        self.root = root
        self.graph_data = graph_data
        self.comboboxes_to_update = []
        self.create_widgets()

        # Ініціалізація компонентів
        self.graph_drawer = GraphDrawer(self.viz_frame, self.graph_data)
        self.graph_editor = GraphEditor(self.control_frame, self.graph_data, self)
        self.dijkstra_runner = DijkstraRunner(self.control_frame, self.graph_data, self)

        self.update_all()  # Початкове малювання

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.control_frame = ttk.Frame(main_frame, width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.control_frame.pack_propagate(False)  # Зафіксувати ширину

        self.viz_frame = ttk.Frame(main_frame)
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def register_combobox(self, combo):
        """Реєструє combobox для оновлення списку міст"""
        self.comboboxes_to_update.append(combo)

    def update_comboboxes(self):
        """Оновлює списки міст у всіх зареєстрованих combobox"""
        cities = self.graph_data.get_cities()
        for combo in self.comboboxes_to_update:
            current_val = combo.get()
            combo['values'] = cities
            if current_val in cities:
                combo.set(current_val)  # Зберегти вибір, якщо можливо
            else:
                combo.set('')  # Очистити, якщо місто видалено

    def update_all(self):
        """Повністю оновлює GUI (мапу та списки)"""
        # Більше не потрібна логіка 'keep_layout',
        # draw_graph() тепер сам керує позиціями
        self.graph_drawer.draw_graph()
        self.update_comboboxes()

    def show_path(self, path):
        """Передає фінальний шлях для візуалізації"""
        self.graph_drawer.show_path(path)