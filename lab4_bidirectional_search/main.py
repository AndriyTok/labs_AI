import tkinter as tk
from gui.App import BidirectionalSearchApp

if __name__ == "__main__":
    root = tk.Tk()
    app = BidirectionalSearchApp(root)
    root.mainloop()