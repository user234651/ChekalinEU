import time
import random
import matplotlib.pyplot as plt
import numpy as np

from modules.graph_representation import GraphList
from modules.graph_traversal import GraphExplorer
from modules.shortest_path import PathFinder

class GraphPlotter:
    """Класс для визуализации графов."""
    
    @staticmethod
    def plot_scaling():
        """Построить графики масштабируемости алгоритмов."""
        sizes = list(range(100, 2001, 200))
        bfs_times = []
        dfs_times = []
        dijkstra_times = []
        
        print("Сбор данных для графика масштабируемости...")
        
        for sz in sizes:
            graph = GraphList(sz)
            weighted_graph = GraphList(sz, weighted=True)
            
            for i in range(sz - 1):
                graph.add_edge(i, i + 1)
                weighted_graph.add_edge(i, i + 1, weight=random.uniform(1, 10))
                
                if i % 10 == 0:
                    max_skip = min(10, sz - i - 1)
                    if max_skip > 2:
                        neighbor = i + random.randint(2, max_skip)
                        if neighbor < sz:
                            graph.add_edge(i, neighbor)
                            weighted_graph.add_edge(i, neighbor, weight=random.uniform(1, 10))
            
            start = time.perf_counter()
            GraphExplorer.bfs(graph, 0)
            bfs_times.append((time.perf_counter() - start) * 1000)
            
            start = time.perf_counter()
            GraphExplorer.dfs_iterative(graph, 0)
            dfs_times.append((time.perf_counter() - start) * 1000)
            
            start = time.perf_counter()
            PathFinder.dijkstra(weighted_graph, 0)
            dijkstra_times.append((time.perf_counter() - start) * 1000)
        
        plt.figure(figsize=(12, 6))
        
        plt.plot(sizes, bfs_times, 'b-o', label='BFS O(V+E)', linewidth=2, markersize=6)
        plt.plot(sizes, dfs_times, 'r-s', label='DFS O(V+E)', linewidth=2, markersize=6)
        plt.plot(sizes, dijkstra_times, 'g-^', label='Dijkstra O((V+E)logV)', linewidth=2, markersize=6)
        
        plt.xlabel('Количество вершин', fontsize=12)
        plt.ylabel('Время (мс)', fontsize=12)
        plt.title('Масштабируемость алгоритмов', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('scalability.png', dpi=150)
        print("✓ График сохранён: scalability.png")
        
        return sizes, bfs_times, dfs_times, dijkstra_times
    
    @staticmethod
    def plot_memory_usage():
        """Построить сравнение использования памяти."""
        from modules.graph_representation import GraphMatrix
        
        sizes = list(range(10, 201, 20))
        matrix_mem = []
        list_mem = []
        
        print("Сбор данных для графика памяти...")
        
        for sz in sizes:
            mat_g = GraphMatrix(sz)
            lst_g = GraphList(sz)
            
            for i in range(sz):
                for j in range(i + 1, min(i + 5, sz)):
                    mat_g.add_edge(i, j)
                    lst_g.add_edge(i, j)
            
            matrix_mem.append(mat_g.get_memory_usage() / 1024)
            list_mem.append(lst_g.get_memory_usage() / 1024)
        
        plt.figure(figsize=(12, 6))
        
        plt.plot(sizes, matrix_mem, 'b-o', label='Матрица O(V²)', linewidth=2, markersize=6)
        plt.plot(sizes, list_mem, 'r-s', label='Список O(V+E)', linewidth=2, markersize=6)
        
        plt.xlabel('Количество вершин', fontsize=12)
        plt.ylabel('Память (KB)', fontsize=12)
        plt.title('Сравнение использования памяти', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('memory_comparison.png', dpi=150)
        print("✓ График сохранён: memory_comparison.png")
    
    @staticmethod
    def plot_operations_complexity():
        """Визуализировать сложность операций."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        operations = ['Добавить\nребро', 'Удалить\nребро', 'Проверить\nребро', 'Получить\nсоседей']
        matrix_cost = [1, 1, 1, 100]
        list_cost = [1, 50, 30, 100]
        
        x = np.arange(len(operations))
        width = 0.35
        
        ax1.bar(x - width/2, matrix_cost, width, label='Матрица', color='blue', alpha=0.7)
        ax1.bar(x + width/2, list_cost, width, label='Список', color='red', alpha=0.7)
        ax1.set_ylabel('Относительное время', fontsize=10)
        ax1.set_title('Сложность операций (V=100)', fontsize=11, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(operations, fontsize=9)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        graph_types = ['Плотный\nграф', 'Средний\nграф', 'Разреженный\nграф']
        matrix_usage = [100, 80, 60]
        list_usage = [20, 15, 8]
        
        x2 = np.arange(len(graph_types))
        ax2.bar(x2 - width/2, matrix_usage, width, label='Матрица', color='blue', alpha=0.7)
        ax2.bar(x2 + width/2, list_usage, width, label='Список', color='red', alpha=0.7)
        ax2.set_ylabel('Память (KB)', fontsize=10)
        ax2.set_title('Память для V=100', fontsize=11, fontweight='bold')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(graph_types, fontsize=9)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        algo_names = ['BFS', 'DFS Рек.', 'DFS Итер.']
        algo_perf = [100, 95, 100]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        ax3.bar(algo_names, algo_perf, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Время (отн. ед.)', fontsize=10)
        ax3.set_title('Сравнение алгоритмов обхода', fontsize=11, fontweight='bold')
        ax3.set_ylim([0, 120])
        ax3.grid(True, alpha=0.3, axis='y')
        
        algos = ['BFS', 'DFS', 'Dijkstra', 'Топо-\nсортировка', 'Поиск\nцикла']
        complexities = ['O(V+E)', 'O(V+E)', 'O((V+E)\nlogV)', 'O(V+E)', 'O(V+E)']
        
        ax4.axis('off')
        ax4.text(0.5, 0.95, 'Сложность алгоритмов', ha='center', va='top', 
                fontsize=12, fontweight='bold', transform=ax4.transAxes)
        
        y_pos = 0.85
        for algo, compl in zip(algos, complexities):
            ax4.text(0.1, y_pos, f"• {algo}:", fontsize=10, transform=ax4.transAxes, fontweight='bold')
            ax4.text(0.35, y_pos, compl, fontsize=10, transform=ax4.transAxes, 
                    family='monospace', color='darkblue')
            y_pos -= 0.15
        
        plt.tight_layout()
        plt.savefig('complexity_comparison.png', dpi=150)
        print("✓ График сохранён: complexity_comparison.png")
    
    @staticmethod
    def draw_sample_graphs():
        """Нарисовать примеры графов."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        ax = axes[0]
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Граф для BFS', fontsize=12, fontweight='bold')
        
        positions = {0: (1, 4), 1: (1, 2), 2: (3, 4), 3: (3, 2), 4: (3, 0)}
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
        
        for v, (x, y) in positions.items():
            circle = plt.Circle((x, y), 0.3, color='lightblue', ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)
        
        for u, v in edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            ax.arrow(x1, y1 - 0.3, (x2-x1)*0.8, (y2-y1)*0.8, 
                    head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=1.5, zorder=2)
        
        bfs_info = "Порядок BFS: 0, 1, 2, 3, 4\nДистанции: [0, 1, 1, 2, 3]"
        ax.text(0.5, -0.5, bfs_info, fontsize=10, family='monospace', 
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        ax = axes[1]
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Взвешенный граф (Dijkstra)', fontsize=12, fontweight='bold')
        
        weighted_edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
        
        for v, (x, y) in positions.items():
            circle = plt.Circle((x, y), 0.3, color='lightgreen', ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)
        
        for u, v, w in weighted_edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            ax.arrow(x1, y1 - 0.3, (x2-x1)*0.8, (y2-y1)*0.8, 
                    head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=1.5, zorder=2)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.2, my + 0.2, str(w), fontsize=10, 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        dijkstra_info = "Dijkstra от 0:\nДистанции: [0, 3, 1, 4, 7]\nПуть к 4: 0→2→1→3→4"
        ax.text(0.5, -0.5, dijkstra_info, fontsize=10, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
        
        ax = axes[2]
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Компоненты связности', fontsize=12, fontweight='bold')
        
        positions2 = {0: (0.5, 4), 1: (0.5, 2), 2: (1.5, 3),
                     3: (3, 4), 4: (4, 3), 5: (4, 1)}
        edges2 = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5)]
        
        colors = ['red', 'red', 'red', 'blue', 'blue', 'blue']
        
        for v, (x, y) in positions2.items():
            circle = plt.Circle((x, y), 0.3, color=colors[v], alpha=0.5, 
                              ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)
        
        for u, v in edges2:
            x1, y1 = positions2[u]
            x2, y2 = positions2[v]
            ax.arrow(x1, y1 - 0.3, (x2-x1)*0.8, (y2-y1)*0.8, 
                    head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=1.5, zorder=2)
        
        comp_info = "2 компоненты связности:\nКомпонента 1: {0, 1, 2}\nКомпонента 2: {3, 4, 5}"
        ax.text(0.5, -0.5, comp_info, fontsize=10, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig('graph_examples.png', dpi=150)
        print("✓ Примеры графов сохранены: graph_examples.png")

def run_plots():
    """Создать все графики."""
    print("\n" + "=" * 70)
    print("СОЗДАНИЕ ВИЗУАЛИЗАЦИЙ")
    print("=" * 70)
    
    GraphPlotter.plot_scaling()
    GraphPlotter.plot_memory_usage()
    GraphPlotter.plot_operations_complexity()
    GraphPlotter.draw_sample_graphs()
    
    print("\n" + "=" * 70)
    print("✓ Все визуализации готовы!")
    print("=" * 70)

if __name__ == '__main__':
    run_plots()