# lab5_dijkstra/gui/draw_graph.py
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ми більше не будемо використовувати 'matplotlib.animation'
# import matplotlib.animation as animation

# Використовуємо українські шрифти для Matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'


class GraphDrawer:
    def __init__(self, parent_frame, graph_data):
        self.parent_frame = parent_frame
        self.graph_data = graph_data

        self.fig, self.ax = plt.subplots(figsize=(16, 14))

        self.canvas = FigureCanvasTkAgg(self.fig, self.parent_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.pos = None
        self.current_path_edges = []

        # --- ЗМІНА ТУТ ---
        # Замість self.anim, ми будемо зберігати ID нашого завдання в tkinter
        self.animation_job = None
        self.animation_steps = []
        self.animation_frame_index = 0
        # --- КІНЕЦЬ ЗМІНИ ---

    def draw_graph(self):
        """Малює статичний граф"""
        self.ax.clear()
        g = self.graph_data.graph
        if not g.nodes:
            self.ax.text(0.5, 0.5, "Граф порожній", ha='center', va='center')
            self.canvas.draw()
            return

        self.pos = self.graph_data.get_positions()

        # Базовий граф
        nx.draw_networkx_nodes(g, self.pos, ax=self.ax, node_color='lightblue', node_size=700)
        nx.draw_networkx_labels(g, self.pos, ax=self.ax, font_size=8)
        nx.draw_networkx_edges(g, self.pos, ax=self.ax, alpha=0.4)
        edge_labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, self.pos, ax=self.ax, edge_labels=edge_labels, font_size=8,
                                     bbox=dict(alpha=0, ec='none'))

        # Підсвітка шляху
        if self.current_path_edges:
            nx.draw_networkx_edges(g, self.pos, ax=self.ax, edgelist=self.current_path_edges, edge_color='red', width=3)
            path_nodes = list(set([u for u, v in self.current_path_edges] + [v for u, v in self.current_path_edges]))
            nx.draw_networkx_nodes(g, self.pos, ax=self.ax, nodelist=path_nodes, node_color='#FF6347', node_size=700)

        self.ax.set_title("Схема автомобільних шляхів")
        self.ax.axis('on')
        self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        self.canvas.draw()

    def show_path(self, path):
        """Встановлює шлях для підсвітки"""
        if path and len(path) > 1:
            self.current_path_edges = list(zip(path, path[1:]))
        else:
            self.current_path_edges = []
        self.draw_graph()

    # --- ЛОГІКУ АНІМАЦІЇ ПОВНІСТЮ ПЕРЕПИСАНО ---

    def animate_search(self, steps):
        """Запускає анімацію на основі кроків (дружньо до tkinter)"""

        # Якщо попередня анімація ще йде, зупиняємо її
        if self.animation_job:
            self.parent_frame.after_cancel(self.animation_job)
            self.animation_job = None

        self.pos = self.graph_data.get_positions()
        self.animation_steps = steps
        self.animation_frame_index = 0

        # Запускаємо перший кадр
        self._animation_step()

    def _animation_step(self):
        """Малює один кадр анімації та планує наступний"""

        # Перевірка, чи анімація не закінчилась
        if self.animation_frame_index >= len(self.animation_steps):
            self.animation_steps = []
            self.animation_job = None
            # Можна додати self.draw_graph() тут, якщо хочете
            # повернути фінальний вигляд після анімації
            return

            # Отримуємо дані для поточного кадру
        frame_data = self.animation_steps[self.animation_frame_index]
        visited_nodes, distances, current_node, neighbors = frame_data

        # --- Логіка малювання (та сама, що була в 'update') ---
        self.ax.clear()
        g = self.graph_data.graph

        # Кольори
        node_colors = []
        for node in g.nodes:
            if node == current_node:
                node_colors.append('orange')  # Поточний
            elif node in visited_nodes:
                node_colors.append('gray')  # Відвіданий
            elif node in neighbors:
                node_colors.append('yellow')  # Перевіряється
            else:
                node_colors.append('lightblue')  # Базовий

        # Малюємо
        nx.draw_networkx_nodes(g, self.pos, ax=self.ax, nodelist=list(g.nodes), node_color=node_colors, node_size=700)
        nx.draw_networkx_labels(g, self.pos, ax=self.ax, font_size=8)
        nx.draw_networkx_edges(g, self.pos, ax=self.ax, alpha=0.3)

        # Відстані
        dist_labels = {}
        for node, (x, y) in self.pos.items():
            dist = distances.get(node, float('inf'))
            if dist != float('inf'):
                dist_labels[node] = f"{dist:.0f}"

        label_pos = {k: (v[0], v[1] - 0.2) for k, v in self.pos.items()}
        nx.draw_networkx_labels(g, label_pos, ax=self.ax, labels=dist_labels, font_size=7, font_color='purple')

        self.ax.set_title(f"Крок {self.animation_frame_index + 1}/{len(self.animation_steps)}. Обробка: {current_node}")
        self.ax.axis('on')
        self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

        # Оновлюємо полотно
        self.canvas.draw()

        # --- Кінець логіки малювання ---

        # Готуємо наступний кадр
        self.animation_frame_index += 1

        # Плануємо виклик цієї ж функції через 400мс
        self.animation_job = self.parent_frame.after(400, self._animation_step)