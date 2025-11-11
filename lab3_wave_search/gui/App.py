from lab3_wave_search.data.grid import Grid
from lab3_wave_search.data.maze_data import MazeData
from lab3_wave_search.gui.main_interface import MainInterface
from lab3_wave_search.logic.algorithm.wave_search import WaveSearch


class WaveAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Хвильовий алгоритм - Однонаправлений пошук")
        self.root.geometry("1200x800")

        # Ініціалізація компонентів
        self.maze_data = MazeData()
        self.grid = Grid(self.maze_data)
        self.wave_search = WaveSearch(self.maze_data, self.grid)

        # Створення інтерфейсу
        self.main_interface = MainInterface(root, self.maze_data,
                                          self.grid, self.wave_search)

        # Відображаємо дефолтний лабіринт (БЕЗ генерації випадкового)
        self.main_interface.update_visualization()