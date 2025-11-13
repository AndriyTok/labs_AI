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
        algo_frame = ttk.LabelFrame(self.parent_frame, text="Алгоритми пошуку")
        algo_frame.pack(fill=tk.X, pady=10)

        # Вибір методу пошуку
        ttk.Label(algo_frame, text="Метод пошуку:").pack(pady=5)
        self.search_method_var = tk.StringVar(value="Двонаправлений")
        method_combo = ttk.Combobox(algo_frame, textvariable=self.search_method_var,
                                    values=["Двонаправлений", "Однонаправлений"],
                                    state="readonly")
        method_combo.pack(fill=tk.X, pady=5)

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

        ttk.Button(algo_frame, text="Порівняти методи пошуку",
                   command=self.compare_methods).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Показати хвильові матриці",
                   command=self.show_wave_matrices).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Показати результати",
                   command=self.show_results_window).pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Скинути відображення",
                   command=self.reset_visualization).pack(fill=tk.X, pady=5)

    def reset_visualization(self):
        """Скидає візуалізацію до звичайного лабіринту"""
        if hasattr(self.main_interface, 'maze_drawer'):
            self.main_interface.maze_drawer.reset_visualization()
        else:
            self.main_interface.update_visualization()

    def run_animated_search(self):
        """Запускає анімований пошук"""
        operator = self.operator_var.get()
        method = self.search_method_var.get()
        self.reset_visualization()

        if method == "Двонаправлений":
            self._run_animated_bidirectional(operator)
        else:
            self._run_animated_unidirectional(operator)

    def _run_animated_bidirectional(self, operator):
        """Анімований двонаправлений пошук"""
        path, cycles_f, cycles_b, search_time, meeting = self.bidirectional_search.search(
            operator, save_steps=True)

        if hasattr(self.main_interface, 'maze_drawer'):
            steps = self.bidirectional_search.get_combined_steps()
            self.main_interface.maze_drawer.animate_bidirectional_search(steps)

        if path:
            messagebox.showinfo("Результат",
                                f"Шлях знайдено!\n"
                                f"Довжина: {len(path)} кроків\n"
                                f"Циклів прямого: {cycles_f}\n"
                                f"Циклів зворотного: {cycles_b}\n"
                                f"Всього циклів: {cycles_f + cycles_b}\n"
                                f"Час: {search_time:.4f} сек")
        else:
            messagebox.showwarning("Результат", "Шлях НЕ знайдено!")

    def _run_animated_unidirectional(self, operator):
        """Анімований однонаправлений пошук"""
        from lab4_bidirectional_search.logic.algorithm.unidirectional_search import UnidirectionalSearch

        uni_search = UnidirectionalSearch(self.maze_data, self.bidirectional_search.grid)
        path, cycles, search_time = uni_search.search(operator, save_steps=True)

        if hasattr(self.main_interface, 'maze_drawer'):
            steps = uni_search.get_wave_steps()
            self.main_interface.maze_drawer.animate_unidirectional_search(steps)

        if path:
            messagebox.showinfo("Результат",
                                f"Шлях знайдено!\n"
                                f"Довжина: {len(path)} кроків\n"
                                f"Циклів: {cycles}\n"
                                f"Час: {search_time:.4f} сек")
        else:
            messagebox.showwarning("Результат", "Шлях НЕ знайдено!")

    def run_search(self):
        """Запускає пошук"""
        operator = self.operator_var.get()
        method = self.search_method_var.get()

        self.reset_visualization()

        if method == "Двонаправлений":
            self._run_bidirectional_search(operator)
        else:
            self._run_unidirectional_search(operator)

    def _run_bidirectional_search(self, operator):
        """Двонаправлений пошук"""
        path, cycles_f, cycles_b, search_time, meeting = self.bidirectional_search.search(operator)

        if path:
            self.main_interface.show_path(path)
            messagebox.showinfo("Результат",
                                f"Шлях знайдено!\n"
                                f"Довжина: {len(path)} кроків\n"
                                f"Циклів прямого: {cycles_f}\n"
                                f"Циклів зворотного: {cycles_b}\n"
                                f"Всього циклів: {cycles_f + cycles_b}\n"
                                f"Час: {search_time:.4f} сек")
        else:
            messagebox.showwarning("Результат", "Шлях НЕ знайдено!")

    def _run_unidirectional_search(self, operator):
        """Однонаправлений пошук"""
        from lab4_bidirectional_search.logic.algorithm.unidirectional_search import UnidirectionalSearch

        uni_search = UnidirectionalSearch(self.maze_data, self.bidirectional_search.grid)
        path, cycles, search_time = uni_search.search(operator)

        if path:
            self.maze_data.current_path = path
            self.main_interface.show_path(path)
            messagebox.showinfo("Результат",
                                f"Шлях знайдено!\n"
                                f"Довжина: {len(path)} кроків\n"
                                f"Циклів: {cycles}\n"
                                f"Час: {search_time:.4f} сек")
        else:
            messagebox.showwarning("Результат", "Шлях НЕ знайдено!")

    def research_all(self):
        """Досліджує всі оператори для обраного методу"""
        self.results_data = []
        method = self.search_method_var.get()

        for operator_type in OperatorType:
            operator = operator_type.value

            if method == "Двонаправлений":
                path, cycles_f, cycles_b, search_time, meeting = self.bidirectional_search.search(operator)
                self.add_result(operator, path, cycles_f, cycles_b, search_time, meeting, method)
            else:
                from lab4_bidirectional_search.logic.algorithm.unidirectional_search import UnidirectionalSearch
                uni_search = UnidirectionalSearch(self.maze_data, self.bidirectional_search.grid)
                path, cycles, search_time = uni_search.search(operator)
                self.add_result(operator, path, cycles, 0, search_time, None, method)

        self.show_results_window()

    def compare_methods(self):
        """Порівнює двонаправлений і однонаправлений пошуки"""
        from lab4_bidirectional_search.logic.algorithm.unidirectional_search import UnidirectionalSearch

        operator = self.operator_var.get()

        # Двонаправлений пошук
        bi_path, bi_cycles_f, bi_cycles_b, bi_time, bi_meeting = self.bidirectional_search.search(operator)

        # Однонаправлений пошук
        uni_search = UnidirectionalSearch(self.maze_data, self.bidirectional_search.grid)
        uni_path, uni_cycles, uni_time = uni_search.search(operator)

        # Показуємо результати порівняння
        self.show_comparison_results(operator,
                                     (bi_path, bi_cycles_f + bi_cycles_b, bi_time, bi_meeting),
                                     (uni_path, uni_cycles, uni_time))

    def show_comparison_results(self, operator, bidirectional_result, unidirectional_result):
        """Показує результати порівняння"""
        bi_path, bi_total_cycles, bi_time, bi_meeting = bidirectional_result
        uni_path, uni_cycles, uni_time = unidirectional_result

        comparison_window = tk.Toplevel(self.main_interface.root)
        comparison_window.title("Порівняння алгоритмів")
        comparison_window.geometry("600x400")

        text_widget = tk.Text(comparison_window, font=('Courier', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_widget.insert(tk.END, f"ПОРІВНЯННЯ АЛГОРИТМІВ ПОШУКУ\n")
        text_widget.insert(tk.END, f"Оператор: {operator}\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")

        text_widget.insert(tk.END, "ДВОНАПРАВЛЕНИЙ ПОШУК:\n")
        if bi_path:
            text_widget.insert(tk.END, f"   ✓ Шлях знайдено\n")
            text_widget.insert(tk.END, f"   Довжина: {len(bi_path)} кроків\n")
            text_widget.insert(tk.END, f"   Циклів: {bi_total_cycles}\n")
            text_widget.insert(tk.END, f"   Час: {bi_time:.4f} сек\n")
            text_widget.insert(tk.END, f"   Точка зустрічі: {bi_meeting}\n")
        else:
            text_widget.insert(tk.END, "   ✗ Шлях не знайдено\n")

        text_widget.insert(tk.END, "\nОДНОНАПРАВЛЕНИЙ ПОШУК:\n")
        if uni_path:
            text_widget.insert(tk.END, f"   ✓ Шлях знайдено\n")
            text_widget.insert(tk.END, f"   Довжина: {len(uni_path)} кроків\n")
            text_widget.insert(tk.END, f"   Циклів: {uni_cycles}\n")
            text_widget.insert(tk.END, f"   Час: {uni_time:.4f} сек\n")
        else:
            text_widget.insert(tk.END, "   ✗ Шлях не знайдено\n")

        if bi_path and uni_path:
            text_widget.insert(tk.END, f"\nВИСНОВКИ:\n")
            text_widget.insert(tk.END,
                               f"Економія циклів: {uni_cycles - bi_total_cycles} ({((uni_cycles - bi_total_cycles) / uni_cycles * 100):.1f}%)\n")
            text_widget.insert(tk.END, f"Економія часу: {(uni_time - bi_time) * 1000:.2f} мс\n")
            text_widget.insert(tk.END, f"Співвідношення циклів: {uni_cycles / bi_total_cycles:.2f}x\n")

        text_widget.config(state=tk.DISABLED)

        ttk.Button(comparison_window, text="Закрити",
                   command=comparison_window.destroy).pack(pady=10)

    def show_wave_matrices(self):
        """Показує хвильові матриці залежно від методу"""
        method = self.search_method_var.get()

        if method == "Двонаправлений":
            if self.maze_data.forward_wave_matrix is not None:
                if hasattr(self.main_interface, 'maze_drawer'):
                    self.main_interface.maze_drawer.draw_bidirectional_waves()
            else:
                messagebox.showinfo("Інформація", "Спочатку запустіть двонаправлений пошук")
        else:
            if self.maze_data.wave_matrix is not None:
                if hasattr(self.main_interface, 'maze_drawer'):
                    self.main_interface.maze_drawer.draw_unidirectional_wave()
            else:
                messagebox.showinfo("Інформація", "Спочатку запустіть однонаправлений пошук")

    def add_result(self, operator, path, cycles_f, cycles_b, search_time, meeting, method):
        """Додає результат до списку"""
        self.results_data.append({
            'operator': operator,
            'method': method,
            'length': len(path) if path else 0,
            'cycles_forward': cycles_f,
            'cycles_backward': cycles_b,
            'total_cycles': cycles_f + cycles_b,
            'time': search_time,
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
        self.results_window.title("Результати пошуку")
        self.results_window.geometry("700x700")

        header_frame = ttk.Frame(self.results_window)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        method = self.results_data[0]['method'] if self.results_data else "Невідомо"
        ttk.Label(header_frame, text=f"РЕЗУЛЬТАТИ {method.upper()} ПОШУКУ",
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

                if result['method'] == "Двонаправлений":
                    results_text.insert(tk.END, f"   Циклів прямого пошуку: {result['cycles_forward']}\n")
                    results_text.insert(tk.END, f"   Циклів зворотного пошуку: {result['cycles_backward']}\n")
                    results_text.insert(tk.END, f"   Всього циклів: {result['total_cycles']}\n")
                    results_text.insert(tk.END, f"   Точка зустрічі: {result['meeting_point']}\n")
                else:
                    results_text.insert(tk.END, f"   Циклів: {result['cycles_forward']}\n")

                results_text.insert(tk.END, f"   Час пошуку: {result['time']:.4f} сек\n")
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

            if best_length['method'] == "Двонаправлений":
                results_text.insert(tk.END, f"   Циклів (прямий/зворотний/всього): "
                                            f"{best_length['cycles_forward']}/{best_length['cycles_backward']}/"
                                            f"{best_length['total_cycles']}\n")
                results_text.insert(tk.END, f"   Точка зустрічі: {best_length['meeting_point']}\n")
            else:
                results_text.insert(tk.END, f"   Циклів: {best_length['cycles_forward']}\n")

            results_text.insert(tk.END, f"   Час виконання: {best_length['time']:.4f} сек\n\n")

            # Найшвидший
            best_time = min(found_results, key=lambda r: r['time'])
            results_text.insert(tk.END, "⚡ НАЙШВИДШЕ ВИКОНАННЯ:\n")
            results_text.insert(tk.END, f"   Оператор: {best_time['operator']}\n")
            results_text.insert(tk.END, f"   Час виконання: {best_time['time']:.4f} сек\n")
            results_text.insert(tk.END, f"   Довжина шляху: {best_time['length']} кроків\n")

            if best_time['method'] == "Двонаправлений":
                results_text.insert(tk.END, f"   Циклів (прямий/зворотний/всього): "
                                            f"{best_time['cycles_forward']}/{best_time['cycles_backward']}/"
                                            f"{best_time['total_cycles']}\n")
                results_text.insert(tk.END, f"   Точка зустрічі: {best_time['meeting_point']}\n\n")
            else:
                results_text.insert(tk.END, f"   Циклів: {best_time['cycles_forward']}\n\n")

            # Найменше циклів
            best_cycles = min(found_results, key=lambda r: r['total_cycles'] if r['method'] == "Двонаправлений" else r[
                'cycles_forward'])
            results_text.insert(tk.END, "🔄 НАЙМЕНШЕ ЦИКЛІВ:\n")
            results_text.insert(tk.END, f"   Оператор: {best_cycles['operator']}\n")

            if best_cycles['method'] == "Двонаправлений":
                results_text.insert(tk.END, f"   Всього циклів: {best_cycles['total_cycles']}\n")
                results_text.insert(tk.END, f"   Циклів прямого пошуку: {best_cycles['cycles_forward']}\n")
                results_text.insert(tk.END, f"   Циклів зворотного пошуку: {best_cycles['cycles_backward']}\n")
                results_text.insert(tk.END, f"   Точка зустрічі: {best_cycles['meeting_point']}\n")
            else:
                results_text.insert(tk.END, f"   Циклів: {best_cycles['cycles_forward']}\n")

            results_text.insert(tk.END, f"   Довжина шляху: {best_cycles['length']} кроків\n")
            results_text.insert(tk.END, f"   Час виконання: {best_cycles['time']:.4f} сек\n\n")

            results_text.insert(tk.END, "=" * 80 + "\n")
        else:
            results_text.insert(tk.END, "\nНемає успішних запусків для аналізу.\n")

        results_text.config(state=tk.DISABLED)

        ttk.Button(self.results_window, text="Закрити",
                   command=self.results_window.destroy).pack(pady=10)
