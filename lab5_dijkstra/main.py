# lab5_dijkstra/main.py
import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from gui.App import DijkstraApp


if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()