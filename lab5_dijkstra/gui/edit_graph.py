# lab5_dijkstra/gui/edit_graph.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


class GraphEditor:
    def __init__(self, parent_frame, graph_data, main_interface):
        self.parent_frame = parent_frame
        self.graph_data = graph_data
        self.main_interface = main_interface
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.LabelFrame(self.parent_frame, text="Редагування графу")
        frame.pack(fill=tk.X, pady=10, padx=5)

        # --- Додати місто ---
        ttk.Button(frame, text="Додати місто", command=self.add_city).pack(fill=tk.X, pady=2)

        # --- Видалити місто ---
        self.remove_city_var = tk.StringVar()
        remove_combo = ttk.Combobox(frame, textvariable=self.remove_city_var, state="readonly")
        remove_combo.pack(fill=tk.X, pady=2)
        self.main_interface.register_combobox(remove_combo)
        ttk.Button(frame, text="Видалити місто", command=self.remove_city).pack(fill=tk.X, pady=2)

        # --- Додати шлях ---
        ttk.Button(frame, text="Додати/Оновити шлях", command=self.add_road).pack(fill=tk.X, pady=(10, 2))

        # --- Видалити шлях ---
        ttk.Button(frame, text="Видалити шлях", command=self.remove_road).pack(fill=tk.X, pady=2)

    def add_city(self):
        city = simpledialog.askstring("Додати місто", "Введіть назву міста:")
        if city:
            if self.graph_data.add_city(city):
                self.main_interface.update_all()
                messagebox.showinfo("Успіх", f"Місто '{city}' додано.")
            else:
                messagebox.showwarning("Помилка", f"Місто '{city}' вже існує або назва некоректна.")

    def remove_city(self):
        city = self.remove_city_var.get()
        if not city:
            messagebox.showwarning("Помилка", "Оберіть місто для видалення.")
            return
        if messagebox.askyesno("Підтвердження", f"Ви впевнені, що хочете видалити '{city}' та всі пов'язані шляхи?"):
            if self.graph_data.remove_city(city):
                self.main_interface.update_all()
                messagebox.showinfo("Успіх", f"Місто '{city}' видалено.")

    def _ask_for_road(self, title):
        """Допоміжний діалог для отримання двох міст"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(title)

        ttk.Label(dialog, text="Місто 1:").pack(padx=10, pady=5)
        city1_var = tk.StringVar()
        combo1 = ttk.Combobox(dialog, textvariable=city1_var, values=self.graph_data.get_cities(), state="readonly")
        combo1.pack(padx=10, pady=2)

        ttk.Label(dialog, text="Місто 2:").pack(padx=10, pady=5)
        city2_var = tk.StringVar()
        combo2 = ttk.Combobox(dialog, textvariable=city2_var, values=self.graph_data.get_cities(), state="readonly")
        combo2.pack(padx=10, pady=2)

        result = {"city1": None, "city2": None, "distance": None}

        def on_ok():
            c1 = city1_var.get()
            c2 = city2_var.get()
            if not c1 or not c2:
                messagebox.showwarning("Помилка", "Оберіть обидва міста.", parent=dialog)
                return
            if c1 == c2:
                messagebox.showwarning("Помилка", "Міста не повинні співпадати.", parent=dialog)
                return

            result["city1"] = c1
            result["city2"] = c2
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        dialog.transient(self.parent_frame)
        dialog.wait_window()
        return result

    def add_road(self):
        data = self._ask_for_road("Додати шлях")
        city1, city2 = data["city1"], data["city2"]

        if city1 and city2:
            distance = simpledialog.askinteger("Відстань", f"Введіть відстань між '{city1}' та '{city2}':", minvalue=1)
            if distance:
                if self.graph_data.add_road(city1, city2, distance):
                    self.main_interface.update_all(keep_layout=True)
                    messagebox.showinfo("Успіх", "Шлях додано/оновлено.")

    def remove_road(self):
        data = self._ask_for_road("Видалити шлях")
        city1, city2 = data["city1"], data["city2"]

        if city1 and city2:
            if self.graph_data.remove_road(city1, city2):
                self.main_interface.update_all(keep_layout=True)
                messagebox.showinfo("Успіх", "Шлях видалено.")
            else:
                messagebox.showwarning("Помилка", "Такого шляху не існує.")