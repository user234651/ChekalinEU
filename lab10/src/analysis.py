import time
import random
import sys
from typing import Dict, Tuple, Callable
from modules.graph_representation import GraphMatrix, GraphList
from modules.graph_traversal import GraphExplorer
from modules.shortest_path import PathFinder

sys.setrecursionlimit(10000)


class Benchmark:
    """Класс для измерения производительности."""
    
    @staticmethod
    def time_function(func: Callable, *args, **kwargs) -> float:
        """Измерить время выполнения функции."""
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        return end - start
    
    @staticmethod
    def make_dense_graph(vertex_count: int) -> Tuple[GraphMatrix, GraphList]:
        """Создать граф с большим числом рёбер."""
        matrix_graph = GraphMatrix(vertex_count)
        list_graph = GraphList(vertex_count)
        
        edge_target = int(vertex_count * (vertex_count - 1) / 2 * 0.5)
        
        for _ in range(edge_target):
            a = random.randint(0, vertex_count - 1)
            b = random.randint(0, vertex_count - 1)
            if a != b:
                matrix_graph.add_edge(a, b)
                list_graph.add_edge(a, b)
        
        return matrix_graph, list_graph
    
    @staticmethod
    def make_sparse_graph(vertex_count: int) -> Tuple[GraphMatrix, GraphList]:
        """Создать граф с малым числом рёбер."""
        matrix_graph = GraphMatrix(vertex_count)
        list_graph = GraphList(vertex_count)
        
        edge_target = vertex_count * 2
        
        for _ in range(edge_target):
            a = random.randint(0, vertex_count - 1)
            b = random.randint(0, vertex_count - 1)
            if a != b and not matrix_graph.has_edge(a, b):
                matrix_graph.add_edge(a, b)
                list_graph.add_edge(a, b)
        
        return matrix_graph, list_graph
    
    @staticmethod
    def compare_memory():
        """Сравнить использование памяти."""
        print("\n" + "=" * 70)
        print("СРАВНЕНИЕ ИСПОЛЬЗОВАНИЯ ПАМЯТИ")
        print("=" * 70)
        
        sizes = [10, 50, 100, 200, 500]
        
        print("\nГраф с 50% рёбер:")
        print(f"{'Вершины':<10} {'Матрица (KB)':<15} {'Список (KB)':<15} {'Экономия':<10}")
        print("-" * 50)
        
        for sz in sizes:
            mat_g, lst_g = Benchmark.make_dense_graph(sz)
            mem_mat = mat_g.get_memory_usage() / 1024
            mem_lst = lst_g.get_memory_usage() / 1024
            saving = (1 - mem_lst / mem_mat) * 100
            print(f"{sz:<10} {mem_mat:<15.2f} {mem_lst:<15.2f} {saving:<10.1f}%")
        
        print("\nГраф с линейным числом рёбер:")
        print(f"{'Вершины':<10} {'Матрица (KB)':<15} {'Список (KB)':<15} {'Экономия':<10}")
        print("-" * 50)
        
        for sz in sizes:
            mat_g, lst_g = Benchmark.make_sparse_graph(sz)
            mem_mat = mat_g.get_memory_usage() / 1024
            mem_lst = lst_g.get_memory_usage() / 1024
            saving = (1 - mem_lst / mem_mat) * 100
            print(f"{sz:<10} {mem_mat:<15.2f} {mem_lst:<15.2f} {saving:<10.1f}%")
    
    @staticmethod
    def compare_edge_check():
        """Сравнить скорость проверки наличия ребра."""
        print("\n" + "=" * 70)
        print("ПРОВЕРКА НАЛИЧИЯ РЕБРА has_edge()")
        print("=" * 70)
        
        sizes = [10, 50, 100, 200, 500]
        
        print("\nДля плотного графа:")
        print(f"{'Вершины':<10} {'Матрица (мкс)':<15} {'Список (мкс)':<15} {'Отношение':<10}")
        print("-" * 50)
        
        for sz in sizes:
            mat_g, lst_g = Benchmark.make_dense_graph(sz)
            
            time_mat = sum(
                Benchmark.time_function(mat_g.has_edge, 0, random.randint(1, sz-1))
                for _ in range(100)
            ) / 100
            
            time_lst = sum(
                Benchmark.time_function(lst_g.has_edge, 0, random.randint(1, sz-1))
                for _ in range(100)
            ) / 100
            
            ratio = time_lst / time_mat if time_mat > 0 else 0
            print(f"{sz:<10} {time_mat*1e6:<15.2f} {time_lst*1e6:<15.2f} {ratio:<10.2f}x")
        
        print("\nДля разреженного графа:")
        print(f"{'Вершины':<10} {'Матрица (мкс)':<15} {'Список (мкс)':<15} {'Отношение':<10}")
        print("-" * 50)
        
        for sz in sizes:
            mat_g, lst_g = Benchmark.make_sparse_graph(sz)
            
            time_mat = sum(
                Benchmark.time_function(mat_g.has_edge, 0, random.randint(1, sz-1))
                for _ in range(100)
            ) / 100
            
            time_lst = sum(
                Benchmark.time_function(lst_g.has_edge, 0, random.randint(1, sz-1))
                for _ in range(100)
            ) / 100
            
            ratio = time_lst / time_mat if time_mat > 0 else 0
            print(f"{sz:<10} {time_mat*1e6:<15.2f} {time_lst*1e6:<15.2f} {ratio:<10.2f}x")
    
    @staticmethod
    def compare_traversal():
        """Сравнить скорость обхода графа."""
        print("\n" + "=" * 70)
        print("СРАВНЕНИЕ АЛГОРИТМОВ ОБХОДА (BFS vs DFS)")
        print("=" * 70)
        
        sizes = [50, 100, 200, 300]
        
        print(f"\n{'Вершины':<10} {'BFS (мкс)':<15} {'DFS Итер. (мкс)':<15}")
        print("-" * 40)
        
        for sz in sizes:
            graph = GraphList(sz)
            
            for i in range(sz - 1):
                graph.add_edge(i, i + 1)
                if i % 10 == 0:
                    graph.add_edge(i, random.randint(0, sz - 1))
            
            bfs_time = Benchmark.time_function(GraphExplorer.bfs, graph, 0)
            dfs_time = Benchmark.time_function(GraphExplorer.dfs_iterative, graph, 0)
            
            print(f"{sz:<10} {bfs_time*1e6:<15.2f} {dfs_time*1e6:<15.2f}")
    
    @staticmethod
    def compare_path_algorithms():
        """Сравнить алгоритмы поиска пути."""
        print("\n" + "=" * 70)
        print("СРАВНЕНИЕ ПОИСКА ПУТЕЙ (BFS vs Dijkstra)")
        print("=" * 70)
        
        sizes = [50, 100, 200, 300]
        
        print(f"\n{'Вершины':<10} {'BFS (мкс)':<15} {'Dijkstra (мкс)':<15} {'Коэф.':<10}")
        print("-" * 50)
        
        for sz in sizes:
            unweighted = GraphList(sz)
            for i in range(sz - 1):
                unweighted.add_edge(i, i + 1)
                if i % 10 == 0 and i + 5 < sz:
                    unweighted.add_edge(i, i + 5)
            
            weighted = GraphList(sz, weighted=True)
            for i in range(sz - 1):
                weighted.add_edge(i, i + 1, weight=random.uniform(0.1, 10))
                if i % 10 == 0 and i + 5 < sz:
                    weighted.add_edge(i, i + 5, weight=random.uniform(0.1, 10))
            
            bfs_time = Benchmark.time_function(GraphExplorer.bfs, unweighted, 0)
            dijkstra_time = Benchmark.time_function(PathFinder.dijkstra, weighted, 0)
            
            ratio = dijkstra_time / bfs_time if bfs_time > 0 else 0
            print(f"{sz:<10} {bfs_time*1e6:<15.2f} {dijkstra_time*1e6:<15.2f} {ratio:<10.2f}x")
    
    @staticmethod
    def scaling_report():
        """Отчёт о масштабируемости."""
        print("\n" + "=" * 70)
        print("АНАЛИЗ МАСШТАБИРУЕМОСТИ")
        print("=" * 70)
        
        print("\nДля графа со списком смежности:")
        print("Сложность BFS: O(V + E)")
        print("Сложность DFS: O(V + E)")
        print("Сложность Dijkstra: O((V + E) log V)")
        
        sizes = [100, 200, 300, 400]
        
        print(f"\n{'Вершины':<10} {'Рёбра':<10} {'BFS (мкс)':<15} {'DFS (мкс)':<15}")
        print("-" * 55)
        
        for sz in sizes:
            g = GraphList(sz)
            edge_cnt = 0
            
            for i in range(sz - 1):
                g.add_edge(i, i + 1)
                edge_cnt += 1
                if i % 5 == 0 and i + 5 < sz:
                    g.add_edge(i, i + 5)
                    edge_cnt += 1
            
            bfs_time = Benchmark.time_function(GraphExplorer.bfs, g, 0)
            dfs_time = Benchmark.time_function(GraphExplorer.dfs_iterative, g, 0)
            
            print(f"{sz:<10} {edge_cnt:<10} {bfs_time*1e6:<15.2f} {dfs_time*1e6:<15.2f}")


class SystemData:
    """Информация о системе."""
    
    @staticmethod
    def get_system_data() -> Dict[str, str]:
        """Получить данные о системе."""
        import platform
        import psutil
        
        data = {
            'ОС': platform.system() + ' ' + platform.release(),
            'Процессор': platform.processor(),
            'Python': platform.python_version(),
            'Ядра CPU': str(psutil.cpu_count()),
            'Память': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'Частота CPU': f"{psutil.cpu_freq().current:.0f} MHz"
        }
        
        return data
    
    @staticmethod
    def print_system_data():
        """Вывести данные о системе."""
        try:
            data = SystemData.get_system_data()
            print("\n" + "=" * 70)
            print("ХАРАКТЕРИСТИКИ СИСТЕМЫ")
            print("=" * 70)
            for key, value in data.items():
                print(f"{key:<20}: {value}")
        except:
            print("Не удалось получить данные о системе")


def run_benchmarks():
    """Запустить все замеры производительности."""
    SystemData.print_system_data()
    Benchmark.compare_memory()
    Benchmark.compare_edge_check()
    Benchmark.compare_traversal()
    Benchmark.compare_path_algorithms()
    Benchmark.scaling_report()


if __name__ == '__main__':
    run_benchmarks()