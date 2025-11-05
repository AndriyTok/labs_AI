from lab4_bidirectional_search.data.grid import Grid
from lab4_bidirectional_search.data.maze_data import MazeData
from lab4_bidirectional_search.gui.main_interface import MainInterface
from lab4_bidirectional_search.logic.algorithm.bidirectional_search import BidirectionalSearch


class BidirectionalSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Двонаправлений хвильовий пошук")
        self.root.geometry("1200x800")

        # Ініціалізація компонентів
        self.maze_data = MazeData()
        self.grid = Grid(self.maze_data)
        self.bidirectional_search = BidirectionalSearch(self.maze_data, self.grid)

        # Створення інтерфейсу
        self.main_interface = MainInterface(root, self.maze_data,
                                          self.grid, self.bidirectional_search)

        # Відображаємо дефолтний лабіринт (БЕЗ генерації випадкового)
        self.main_interface.update_visualization()