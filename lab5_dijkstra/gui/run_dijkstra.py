# lab5_dijkstra/gui/run_dijkstra.py
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from lab5_dijkstra.logic.algorithm.dijkstra import dijkstra_search, dijkstra_search_animated


class DijkstraRunner:
    def __init__(self, parent_frame, graph_data, main_interface):
        self.parent_frame = parent_frame
        self.graph_data = graph_data
        self.main_interface = main_interface
        self.results_window = None
        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.LabelFrame(self.parent_frame, text="Алгоритм Дейкстри")
        frame.pack(fill=tk.X, pady=10, padx=5)

        ttk.Label(frame, text="Початкова точка:").pack(pady=(5, 0))
        self.start_var = tk.StringVar()
        start_combo = ttk.Combobox(frame, textvariable=self.start_var, state="readonly")
        start_combo.pack(fill=tk.X, pady=2, padx=5)
        self.main_interface.register_combobox(start_combo)

        ttk.Label(frame, text="Кінцева точка:").pack(pady=(5, 0))
        self.end_var = tk.StringVar()
        end_combo = ttk.Combobox(frame, textvariable=self.end_var, state="readonly")
        end_combo.pack(fill=tk.X, pady=2, padx=5)
        self.main_interface.register_combobox(end_combo)

        self.search_btn = ttk.Button(frame, text="Знайти шлях", command=self.run_search)
        self.search_btn.pack(fill=tk.X, pady=5, padx=5)

        self.animate_btn = ttk.Button(frame, text="Анімація пошуку", command=self.run_animated_search)
        self.animate_btn.pack(fill=tk.X, pady=5, padx=5)

    def _validate_input(self):
        start = self.start_var.get()
        end = self.end_var.get()
        if not start or not end:
            messagebox.showwarning("Помилка", "Оберіть початкову та кінцеву точки.")
            return None, None
        if start == end:
            messagebox.showinfo("Результат", "Початкова та кінцева точки співпадають. Шлях = 0.")
            return None, None
        return start, end

    def run_search(self):
        start, end = self._validate_input()
        if not start:
            return

        path, distance, cycles = dijkstra_search(self.graph_data.graph, start, end)
        self.main_interface.show_path(path)
        self.show_results_window(path, distance, cycles)

    def run_animated_search(self):
        start, end = self._validate_input()
        if not start:
            return

        self._set_buttons_state("disabled")

        def compute():
            try:
                steps, path, distance = dijkstra_search_animated(self.graph_data.graph, start, end)

                # Конвертуємо в прості Python типи
                safe_steps = []
                for visited, dists, curr, neighs in steps:
                    safe_steps.append((
                        set(str(v) for v in visited),
                        {str(k): float(v) if v != float('inf') else 9999999 for k, v in dists.items()},
                        str(curr),
                        [str(n) for n in neighs]
                    ))

                safe_path = [str(p) for p in path] if path else None
                safe_dist = float(distance) if distance != float('inf') else None

                self.parent_frame.after(0, lambda: self._on_ready(safe_steps, safe_path, safe_dist))
            except Exception as e:
                import traceback
                error_msg = f"{str(e)}\n\n{traceback.format_exc()}"
                self.parent_frame.after(0, lambda: self._on_error(error_msg))

        threading.Thread(target=compute, daemon=True).start()

    def _on_ready(self, steps, path, distance):
        if not steps:
            messagebox.showwarning("Помилка", "Не вдалося запустити анімацію.")
            self._set_buttons_state("normal")
            return

        self.main_interface.graph_drawer.animate_search(steps)
        self.show_results_window(path, distance, len(steps))
        self._set_buttons_state("normal")

    def _on_error(self, error_msg):
        messagebox.showerror("Помилка", f"Помилка під час обчислення:\n{error_msg}")
        self._set_buttons_state("normal")

    def _set_buttons_state(self, state):
        try:
            self.search_btn.config(state=state)
            self.animate_btn.config(state=state)
        except Exception:
            pass

    def show_results_window(self, path, distance, cycles):
        if self.results_window and tk.Toplevel.winfo_exists(self.results_window):
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.main_interface.root)
        self.results_window.title("Результати пошуку")
        self.results_window.geometry("400x300")

        text_area = tk.Text(self.results_window, wrap=tk.WORD, font=('Arial', 12))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if path:
            text_area.insert(tk.END, f"✅ ШЛЯХ ЗНАЙДЕНО\n")
            text_area.insert(tk.END, f"--------------------------\n")
            text_area.insert(tk.END, f"Маршрут:\n{' -> '.join(path)}\n\n")
            text_area.insert(tk.END, f"Загальна відстань: {distance:.0f} км\n")
            text_area.insert(tk.END, f"Кількість кроків/циклів: {cycles}\n")
        else:
            text_area.insert(tk.END, f"❌ ШЛЯХ НЕ ЗНАЙДЕНО\n")
            text_area.insert(tk.END, f"--------------------------\n")
            text_area.insert(tk.END, f"Не вдалося прокласти маршрут.\n")
            text_area.insert(tk.END, f"Кількість кроків/циклів: {cycles}\n")

        text_area.config(state=tk.DISABLED)
        ttk.Button(self.results_window, text="Закрити", command=self.results_window.destroy).pack(pady=5)