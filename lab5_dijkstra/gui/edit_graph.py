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

        # Додати місто (розширена версія)
        ttk.Button(frame, text="Додати місто (розширене)",
                   command=self.add_city_advanced).pack(fill=tk.X, pady=2)

        # Видалити місто
        self.remove_city_var = tk.StringVar()
        remove_combo = ttk.Combobox(frame, textvariable=self.remove_city_var, state="readonly")
        remove_combo.pack(fill=tk.X, pady=2)
        self.main_interface.register_combobox(remove_combo)
        ttk.Button(frame, text="Видалити місто", command=self.remove_city).pack(fill=tk.X, pady=2)

        # Додати/оновити шлях
        ttk.Button(frame, text="Додати/Оновити шлях",
                   command=self.add_road).pack(fill=tk.X, pady=(10, 2))

        # Видалити шлях
        ttk.Button(frame, text="Видалити шлях", command=self.remove_road).pack(fill=tk.X, pady=2)

    def add_city_advanced(self):
        """Додає місто з координатами"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Додати місто")
        dialog.geometry("300x250")  # Збільшено висоту

        ttk.Label(dialog, text="Назва міста:").pack(padx=10, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(padx=10, pady=2, fill=tk.X)

        ttk.Label(dialog, text="Довгота (x):").pack(padx=10, pady=5)
        lon_var = tk.StringVar(value="30.0")
        ttk.Entry(dialog, textvariable=lon_var).pack(padx=10, pady=2, fill=tk.X)

        ttk.Label(dialog, text="Широта (y):").pack(padx=10, pady=5)
        lat_var = tk.StringVar(value="50.0")
        ttk.Entry(dialog, textvariable=lat_var).pack(padx=10, pady=2, fill=tk.X)

        def on_ok():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Помилка", "Введіть назву міста.", parent=dialog)
                return

            try:
                lon = float(lon_var.get())
                lat = float(lat_var.get())
            except ValueError:
                messagebox.showwarning("Помилка", "Координати мають бути числами.", parent=dialog)
                return

            if self.graph_data.add_city_with_coords(name, lon, lat):
                self.main_interface.update_all()
                messagebox.showinfo("Успіх", f"Місто '{name}' додано.")
                dialog.destroy()
            else:
                messagebox.showwarning("Помилка", f"Місто '{name}' вже існує.", parent=dialog)

        ttk.Button(dialog, text="Додати", command=on_ok).pack(pady=10)
        dialog.transient(self.parent_frame)
        dialog.grab_set()  # Блокує головне вікно

    def remove_city(self):
        city = self.remove_city_var.get()
        if not city:
            messagebox.showwarning("Помилка", "Оберіть місто для видалення.")
            return
        if messagebox.askyesno("Підтвердження",
                               f"Видалити '{city}' та всі пов'язані шляхи?"):
            if self.graph_data.remove_city(city):
                self.main_interface.update_all()
                messagebox.showinfo("Успіх", f"Місто '{city}' видалено.")

    def _ask_for_road(self, title):
        """Діалог для вибору двох міст"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(title)

        ttk.Label(dialog, text="Місто 1:").pack(padx=10, pady=5)
        city1_var = tk.StringVar()
        combo1 = ttk.Combobox(dialog, textvariable=city1_var,
                              values=self.graph_data.get_cities(), state="readonly")
        combo1.pack(padx=10, pady=2)

        ttk.Label(dialog, text="Місто 2:").pack(padx=10, pady=5)
        city2_var = tk.StringVar()
        combo2 = ttk.Combobox(dialog, textvariable=city2_var,
                              values=self.graph_data.get_cities(), state="readonly")
        combo2.pack(padx=10, pady=2)

        result = {"city1": None, "city2": None}

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
            distance = simpledialog.askinteger("Відстань",
                                               f"Відстань між '{city1}' та '{city2}':",
                                               minvalue=1)
            if distance:
                if self.graph_data.add_road(city1, city2, distance):
                    self.main_interface.update_all()
                    messagebox.showinfo("Успіх", "Шлях додано/оновлено.")

    def remove_road(self):
        data = self._ask_for_road("Видалити шлях")
        city1, city2 = data["city1"], data["city2"]

        if city1 and city2:
            if self.graph_data.remove_road(city1, city2):
                self.main_interface.update_all()
                messagebox.showinfo("Успіх", "Шлях видалено.")
            else:
                messagebox.showwarning("Помилка", "Такого шляху не існує.")
