# lab5_dijkstra/gui/App.py
from lab5_dijkstra.data.graph_data import GraphData
from lab5_dijkstra.gui.main_interface import MainInterface


class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм Дейкстри - Автомобільні шляхи України")
        self.root.geometry("1400x900")

        # Ініціалізація даних
        self.graph_data = GraphData()

        # Створення інтерфейсу
        self.main_interface = MainInterface(root, self.graph_data)