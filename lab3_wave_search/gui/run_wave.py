import tkinter as tk
from tkinter import ttk, messagebox

from lab3_wave_search.logic.maze.types import OperatorType


class WaveRunner:
    def __init__(self, parent_frame, wave_search, maze_data, main_interface):
        self.parent_frame = parent_frame
        self.wave_search = wave_search
        self.maze_data = maze_data
        self.main_interface = main_interface
        self.results_window = None
        self.results_data = []

        self.create_widgets()

    def create_widgets(self):
        algo_frame = ttk.LabelFrame(self.parent_frame, text="Хвильовий алгоритм")
        algo_frame.pack(fill=tk.X, pady=10)

        ttk.Label(algo_frame, text="Оператор переходу:").pack(pady=5)

        self.operator_var = tk.StringVar(value=OperatorType.FOUR_DIRECTIONS.value)
        operator_combo = ttk.Combobox(algo_frame, textvariable=self.operator_var,
                                      values=[op.value for op in OperatorType],
                                      state="readonly")
        operator_combo.pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Запустити пошук",
                   command=self.run_search).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Анімація пошуку",
                   command=self.run_animated_search).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Дослідити всі оператори",
                   command=self.research_all).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Показати хвильову матрицю",
                   command=self.show_wave_matrix).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Показати результати",
                   command=self.show_results_window).pack(fill=tk.X, pady=5)

    def run_search(self):
        """Запускає пошук з поточними параметрами"""
        operator = self.operator_var.get()
        path, cycles, search_time = self.wave_search.search(operator)

        if path:
            self.main_interface.show_path(path)
            self.add_result(operator, path, cycles, search_time)
            messagebox.showinfo("Успіх", f"Шлях знайдено! Довжина: {len(path)}")
        else:
            messagebox.showwarning("Увага", "Шлях не знайдено!")
            self.add_result(operator, None, cycles, search_time)

    def run_animated_search(self):
        """Запускає пошук з анімацією"""
        operator = self.operator_var.get()
        path, cycles, search_time = self.wave_search.search(operator, save_steps=True)

        if path:
            wave_steps = self.wave_search.get_wave_steps()
            if hasattr(self.main_interface, 'maze_drawer'):
                self.main_interface.maze_drawer.animate_wave(wave_steps)
            self.add_result(operator, path, cycles, search_time)
        else:
            messagebox.showwarning("Увага", "Шлях не знайдено!")
            self.add_result(operator, None, cycles, search_time)

    def research_all(self):
        """Досліджує всі оператори"""
        self.results_data = []

        for operator_type in OperatorType:
            operator = operator_type.value
            path, cycles, search_time = self.wave_search.search(operator)
            self.add_result(operator, path, cycles, search_time)

        self.show_results_window()

    def show_wave_matrix(self):
        """Показує хвильову матрицю"""
        if self.maze_data.wave_matrix is not None:
            if hasattr(self.main_interface, 'maze_drawer'):
                self.main_interface.maze_drawer.draw_wave_matrix(
                    self.maze_data.wave_matrix)
        else:
            messagebox.showinfo("Інформація",
                                "Спочатку запустіть пошук для створення хвильової матриці")

    def add_result(self, operator, path, cycles, search_time):
        """Додає результат до списку"""
        self.results_data.append({
            'operator': operator,
            'path': path,
            'cycles': cycles,
            'time': search_time,
            'length': len(path) if path else 0,
            'found': path is not None
        })

    def show_results_window(self):
        """Показує окреме вікно з результатами"""
        if not self.results_data:
            messagebox.showinfo("Інформація", "Немає результатів для відображення.\nСпочатку запустіть пошук.")
            return

        # Закриваємо попереднє вікно, якщо воно відкрите
        if self.results_window and tk.Toplevel.winfo_exists(self.results_window):
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.main_interface.root)
        self.results_window.title("Результати пошуку")
        self.results_window.geometry("600x500")

        # Заголовок
        header_frame = ttk.Frame(self.results_window)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="РЕЗУЛЬТАТИ ХВИЛЬОВОГО ПОШУКУ",
                  font=('Arial', 14, 'bold')).pack()

        # Текстове поле з прокруткою
        text_frame = ttk.Frame(self.results_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        results_text = tk.Text(text_frame, yscrollcommand=scrollbar.set,
                               font=('Courier', 10), wrap=tk.WORD)
        results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=results_text.yview)

        # Заповнюємо результатами
        results_text.insert(tk.END, "=" * 70 + "\n")

        for i, result in enumerate(self.results_data, 1):
            results_text.insert(tk.END, f"\n{i}. Оператор: {result['operator']}\n")
            results_text.insert(tk.END, "-" * 70 + "\n")

            if result['found']:
                results_text.insert(tk.END, f"   ✓ Шлях знайдено\n")
                results_text.insert(tk.END, f"   Довжина шляху: {result['length']} кроків\n")
                results_text.insert(tk.END, f"   Циклів розкриття: {result['cycles']}\n")
                results_text.insert(tk.END, f"   Час пошуку: {result['time']:.4f} сек\n")

                results_text.insert(tk.END, f"\n   Координати шляху (перші 10 точок):\n")
                for j, (x, y) in enumerate(result['path'][:10], 1):
                    results_text.insert(tk.END, f"      {j}. ({x}, {y})\n")
                if result['length'] > 10:
                    results_text.insert(tk.END, f"      ... та ще {result['length'] - 10} точок\n")
            else:
                results_text.insert(tk.END, f"   ✗ Шлях НЕ знайдено\n")
                results_text.insert(tk.END, f"   Циклів розкриття: {result['cycles']}\n")
                results_text.insert(tk.END, f"   Час пошуку: {result['time']:.4f} сек\n")

            results_text.insert(tk.END, "\n")

        # Аналіз результатів
        valid_results = [r for r in self.results_data if r['found']]
        if valid_results:
            results_text.insert(tk.END, "=" * 70 + "\n")
            results_text.insert(tk.END, "АНАЛІЗ РЕЗУЛЬТАТІВ:\n")
            results_text.insert(tk.END, "=" * 70 + "\n\n")

            shortest = min(valid_results, key=lambda x: x['length'])
            fastest = min(valid_results, key=lambda x: x['time'])
            least_cycles = min(valid_results, key=lambda x: x['cycles'])

            results_text.insert(tk.END,
                                f"Найкоротший шлях:\n   {shortest['operator']} ({shortest['length']} кроків)\n\n")
            results_text.insert(tk.END,
                                f"Найшвидший пошук:\n   {fastest['operator']} ({fastest['time']:.4f} сек)\n\n")
            results_text.insert(tk.END,
                                f"Найменше циклів:\n   {least_cycles['operator']} ({least_cycles['cycles']} циклів)\n")

        results_text.config(state=tk.DISABLED)

        # Кнопка закриття
        ttk.Button(self.results_window, text="Закрити",
                   command=self.results_window.destroy).pack(pady=10)
