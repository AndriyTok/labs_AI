import tkinter as tk
from tkinter import ttk, messagebox

from lab4_bidirectional_search.logic.maze.types import OperatorType


class BidirectionalRunner:
    def __init__(self, parent_frame, bidirectional_search, maze_data, main_interface):
        self.parent_frame = parent_frame
        self.bidirectional_search = bidirectional_search
        self.maze_data = maze_data
        self.main_interface = main_interface
        self.results_window = None
        self.results_data = []

        self.create_widgets()

    def create_widgets(self):
        algo_frame = ttk.LabelFrame(self.parent_frame, text="Двонаправлений хвильовий алгоритм")
        algo_frame.pack(fill=tk.X, pady=10)

        ttk.Label(algo_frame, text="Оператор переходу:").pack(pady=5)

        self.operator_var = tk.StringVar(value=OperatorType.FOUR_DIRECTIONS.value)
        operator_combo = ttk.Combobox(algo_frame, textvariable=self.operator_var,
                                      values=[op.value for op in OperatorType],
                                      state="readonly")
        operator_combo.pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Запустити пошук",
                   command=self.run_search).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Анімований пошук",
                   command=self.run_animated_search).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Дослідити всі оператори",
                   command=self.research_all).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Показати хвильові матриці",
                   command=self.show_wave_matrices).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Показати результати",
                   command=self.show_results_window).pack(fill=tk.X, pady=5)

    def run_animated_search(self):
        """Запускає анімований двонаправлений пошук"""
        operator = self.operator_var.get()
        path, cycles_f, cycles_b, search_time, meeting = self.bidirectional_search.search(
            operator, save_steps=True)

        if hasattr(self.main_interface, 'maze_drawer'):
            combined_steps = self.bidirectional_search.get_combined_steps()
            self.main_interface.maze_drawer.animate_bidirectional_search(combined_steps)

        if path:
            self.add_result(operator, path, cycles_f, cycles_b, search_time, meeting)
            messagebox.showinfo("Успіх",
                                f"Анімація завершена!\nДовжина шляху: {len(path)}\n"
                                f"Точка зустрічі: {meeting}")
        else:
            messagebox.showwarning("Увага", "Шлях не знайдено!")

    def run_search(self):
        """Запускає двонаправлений пошук"""
        operator = self.operator_var.get()
        path, cycles_f, cycles_b, search_time, meeting = self.bidirectional_search.search(operator)

        if path:
            self.main_interface.show_path(path)
            self.add_result(operator, path, cycles_f, cycles_b, search_time, meeting)
            messagebox.showinfo("Успіх",
                                f"Шлях знайдено!\nДовжина: {len(path)}\n"
                                f"Точка зустрічі: {meeting}")
        else:
            messagebox.showwarning("Увага", "Шлях не знайдено!")
            self.add_result(operator, None, cycles_f, cycles_b, search_time, None)

    def research_all(self):
        """Досліджує всі оператори"""
        self.results_data = []

        for operator_type in OperatorType:
            operator = operator_type.value
            path, cycles_f, cycles_b, search_time, meeting = self.bidirectional_search.search(operator)
            self.add_result(operator, path, cycles_f, cycles_b, search_time, meeting)

        self.show_results_window()

    def show_wave_matrices(self):
        """Показує обidві хвильові матриці"""
        if self.maze_data.forward_wave_matrix is not None:
            if hasattr(self.main_interface, 'maze_drawer'):
                self.main_interface.maze_drawer.draw_bidirectional_waves()
        else:
            messagebox.showinfo("Інформація", "Спочатку запустіть пошук")

    def add_result(self, operator, path, cycles_f, cycles_b, search_time, meeting):
        """Додає результат до списку"""
        self.results_data.append({
            'operator': operator,
            'path': path,
            'cycles_forward': cycles_f,
            'cycles_backward': cycles_b,
            'total_cycles': cycles_f + cycles_b,
            'time': search_time,
            'length': len(path) if path else 0,
            'found': path is not None,
            'meeting_point': meeting
        })

    def show_results_window(self):
        """Показує окреме вікно з результатами"""
        if not self.results_data:
            messagebox.showinfo("Інформація", "Немає результатів")
            return

        if self.results_window and tk.Toplevel.winfo_exists(self.results_window):
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.main_interface.root)
        self.results_window.title("Результати двонаправленого пошуку")
        self.results_window.geometry("700x700")

        header_frame = ttk.Frame(self.results_window)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="РЕЗУЛЬТАТИ ДВОНАПРАВЛЕНОГО ХВИЛЬОВОГО ПОШУКУ",
                  font=('Arial', 14, 'bold')).pack()

        text_frame = ttk.Frame(self.results_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        results_text = tk.Text(text_frame, yscrollcommand=scrollbar.set,
                               font=('Courier', 10), wrap=tk.WORD)
        results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=results_text.yview)

        results_text.insert(tk.END, "=" * 80 + "\n")

        for i, result in enumerate(self.results_data, 1):
            results_text.insert(tk.END, f"\n{i}. Оператор: {result['operator']}\n")
            results_text.insert(tk.END, "-" * 80 + "\n")

            if result['found']:
                results_text.insert(tk.END, f"   ✓ Шлях знайдено\n")
                results_text.insert(tk.END, f"   Довжина шляху: {result['length']} кроків\n")
                results_text.insert(tk.END, f"   Циклів прямого пошуку: {result['cycles_forward']}\n")
                results_text.insert(tk.END, f"   Циклів зворотного пошуку: {result['cycles_backward']}\n")
                results_text.insert(tk.END, f"   Всього циклів: {result['total_cycles']}\n")
                results_text.insert(tk.END, f"   Час пошуку: {result['time']:.4f} сек\n")
                results_text.insert(tk.END, f"   Точка зустрічі: {result['meeting_point']}\n")
            else:
                results_text.insert(tk.END, f"   ✗ Шлях НЕ знайдено\n")

            results_text.insert(tk.END, "\n")

        # Аналіз найкращих результатів
        found_results = [r for r in self.results_data if r['found']]

        if found_results:
            results_text.insert(tk.END, "=" * 80 + "\n")
            results_text.insert(tk.END, "АНАЛІЗ НАЙКРАЩИХ РЕЗУЛЬТАТІВ\n")
            results_text.insert(tk.END, "=" * 80 + "\n\n")

            # Найкоротший шлях
            best_length = min(found_results, key=lambda r: r['length'])
            results_text.insert(tk.END, "🏆 НАЙКОРОТШИЙ ШЛЯХ:\n")
            results_text.insert(tk.END, f"   Оператор: {best_length['operator']}\n")
            results_text.insert(tk.END, f"   Довжина: {best_length['length']} кроків\n")
            results_text.insert(tk.END, f"   Циклів (прямий/зворотний/всього): "
                                        f"{best_length['cycles_forward']}/{best_length['cycles_backward']}/"
                                        f"{best_length['total_cycles']}\n")
            results_text.insert(tk.END, f"   Час виконання: {best_length['time']:.4f} сек\n")
            results_text.insert(tk.END, f"   Точка зустрічі: {best_length['meeting_point']}\n\n")

            # Найшвидший
            best_time = min(found_results, key=lambda r: r['time'])
            results_text.insert(tk.END, "⚡ НАЙШВИДШЕ ВИКОНАННЯ:\n")
            results_text.insert(tk.END, f"   Оператор: {best_time['operator']}\n")
            results_text.insert(tk.END, f"   Час виконання: {best_time['time']:.4f} сек\n")
            results_text.insert(tk.END, f"   Довжина шляху: {best_time['length']} кроків\n")
            results_text.insert(tk.END, f"   Циклів (прямий/зворотний/всього): "
                                        f"{best_time['cycles_forward']}/{best_time['cycles_backward']}/"
                                        f"{best_time['total_cycles']}\n")
            results_text.insert(tk.END, f"   Точка зустрічі: {best_time['meeting_point']}\n\n")

            # Найменше циклів
            best_cycles = min(found_results, key=lambda r: r['total_cycles'])
            results_text.insert(tk.END, "🔄 НАЙМЕНШЕ ЦИКЛІВ:\n")
            results_text.insert(tk.END, f"   Оператор: {best_cycles['operator']}\n")
            results_text.insert(tk.END, f"   Всього циклів: {best_cycles['total_cycles']}\n")
            results_text.insert(tk.END, f"   Циклів прямого пошуку: {best_cycles['cycles_forward']}\n")
            results_text.insert(tk.END, f"   Циклів зворотного пошуку: {best_cycles['cycles_backward']}\n")
            results_text.insert(tk.END, f"   Довжина шляху: {best_cycles['length']} кроків\n")
            results_text.insert(tk.END, f"   Час виконання: {best_cycles['time']:.4f} сек\n")
            results_text.insert(tk.END, f"   Точка зустрічі: {best_cycles['meeting_point']}\n\n")

            results_text.insert(tk.END, "=" * 80 + "\n")
        else:
            results_text.insert(tk.END, "\nНемає успішних запусків для аналізу.\n")

        results_text.config(state=tk.DISABLED)

        ttk.Button(self.results_window, text="Закрити",
                   command=self.results_window.destroy).pack(pady=10)
