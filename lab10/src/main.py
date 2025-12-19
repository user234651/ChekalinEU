from typing import List, Tuple, Optional
from enum import Enum
from modules.graph_representation import GraphMatrix, GraphList
from modules.graph_traversal import GraphExplorer
from modules.shortest_path import TopologicalSorter

class CellType(Enum):
    """Категории ячеек лабиринта."""
    BLOCK = '#'
    FREE = ' '
    BEGIN = 'S'
    FINAL = 'E'

class MazeSolver:
    """
    Практическая задача 1: Нахождение кратчайшего маршрута в лабиринте.
    
    Алгоритм:
    1. Преобразование лабиринта в граф (вершины — свободные клетки)
    2. Добавление связей между соседними клетками
    3. Поиск кратчайшего пути через BFS
    """
    
    @staticmethod
    def find_path(layout: List[List[str]]) -> Optional[List[Tuple[int, int]]]:
        """
        Найти кратчайший путь от старта к финишу.
        
        Сложность: O(rows * cols)
        """
        rows = len(layout)
        cols = len(layout[0]) if layout else 0
        start_pos = None
        end_pos = None
        
        for r in range(rows):
            for c in range(cols):
                if layout[r][c] == 'S':
                    start_pos = (r, c)
                elif layout[r][c] == 'E':
                    end_pos = (r, c)
        
        if not start_pos or not end_pos:
            return None
        
        cell_to_id = {}
        id_to_cell = {}
        counter = 0
        
        for r in range(rows):
            for c in range(cols):
                if layout[r][c] != '#':
                    cell_to_id[(r, c)] = counter
                    id_to_cell[counter] = (r, c)
                    counter += 1
        
        if start_pos not in cell_to_id or end_pos not in cell_to_id:
            return None
        
        graph = GraphList(counter)
        
        for r in range(rows):
            for c in range(cols):
                if layout[r][c] != '#':
                    cur_id = cell_to_id[(r, c)]
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and layout[nr][nc] != '#':
                            nb_id = cell_to_id[(nr, nc)]
                            graph.add_edge(cur_id, nb_id)
        
        start_id = cell_to_id[start_pos]
        end_id = cell_to_id[end_pos]
        
        route = GraphExplorer.bfs_shortest_path(graph, start_id, end_id)
        
        if route:
            return [id_to_cell[v] for v in route]
        return None
    
    @staticmethod
    def show_path(layout: List[List[str]], route: Optional[List[Tuple[int, int]]]) -> str:
        """
        Отобразить лабиринт с проложенным маршрутом.
        """
        result = [row[:] for row in layout]
        
        if route:
            for idx, (r, c) in enumerate(route):
                if result[r][c] not in ['S', 'E']:
                    result[r][c] = '.'
        
        return '\n'.join(''.join(row) for row in result)

class NetworkAnalyzer:
    """
    Практическая задача 2: Анализ связности сети.
    
    Применение:
    - Проверка целостности сети
    - Выявление групп узлов
    - Поиск узлов, критичных для связности
    """
    
    @staticmethod
    def check_connections(links: List[Tuple[int, int]], node_count: int) -> dict:
        """
        Проанализировать связность сети.
        
        Сложность: O(V + E)
        """
        graph = GraphList(node_count)
        
        for a, b in links:
            if 0 <= a < node_count and 0 <= b < node_count:
                graph.add_edge(a, b)
        
        components = GraphExplorer.find_connected_components(graph)
        
        report = {
            'is_fully_connected': len(components) == 1,
            'component_count': len(components),
            'components': [sorted(list(comp)) for comp in components],
            'biggest_component': max(components, key=len) if components else set(),
            'alone_nodes': [comp.pop() for comp in components if len(comp) == 1]
        }
        
        return report
    
    @staticmethod
    def find_bottlenecks(links: List[Tuple[int, int]], node_count: int) -> List[int]:
        """
        Найти узлы, удаление которых нарушает связность.
        
        Сложность: O(V * (V + E))
        """
        base_graph = GraphList(node_count)
        for a, b in links:
            if 0 <= a < node_count and 0 <= b < node_count:
                base_graph.add_edge(a, b)
        
        base_components = len(GraphExplorer.find_connected_components(base_graph))
        bottlenecks = []
        
        for node in range(node_count):
            temp_graph = GraphList(node_count)
            for a, b in links:
                if a != node and b != node and 0 <= a < node_count and 0 <= b < node_count:
                    temp_graph.add_edge(a, b)
            
            if len(GraphExplorer.find_connected_components(temp_graph)) > base_components:
                bottlenecks.append(node)
        
        return bottlenecks
    
    @staticmethod
    def generate_report(links: List[Tuple[int, int]], node_count: int) -> str:
        """
        Сформировать отчёт о состоянии сети.
        """
        analysis = NetworkAnalyzer.check_connections(links, node_count)
        bottlenecks = NetworkAnalyzer.find_bottlenecks(links, node_count)
        
        report_lines = []
        report_lines.append("=" * 50)
        report_lines.append("ОТЧЕТ О СОСТОЯНИИ СЕТИ")
        report_lines.append("=" * 50)
        report_lines.append(f"Узлов всего: {node_count}")
        report_lines.append(f"Соединений всего: {len(links)}")
        report_lines.append(f"Сеть единая: {'Да' if analysis['is_fully_connected'] else 'Нет'}")
        report_lines.append(f"Количество компонент: {analysis['component_count']}")
        
        if analysis['alone_nodes']:
            report_lines.append(f"Изолированные узлы: {analysis['alone_nodes']}")
        
        if bottlenecks:
            report_lines.append(f"Критические узлы: {bottlenecks}")
        else:
            report_lines.append("Критических узлов не выявлено")
        
        report_lines.append("\nКомпоненты связности:")
        for i, comp in enumerate(analysis['components']):
            report_lines.append(f"  Компонента {i+1}: {comp}")
        
        return '\n'.join(report_lines)

class TaskPlanner:
    """
    Практическая задача 3: Упорядочивание задач с учётом зависимостей.
    
    Применение:
    - Планирование проектных работ
    - Разрешение зависимостей пакетов
    - Составление расписаний
    """
    
    @staticmethod
    def schedule_tasks(task_names: List[str], deps: List[Tuple[int, int]]) -> Optional[List[str]]:
        """
        Определить порядок выполнения задач с зависимостями.
        
        Сложность: O(V + E)
        """
        task_count = len(task_names)
        graph = GraphList(task_count, directed=True)
        
        for u, v in deps:
            if 0 <= u < task_count and 0 <= v < task_count:
                graph.add_edge(u, v)
        
        order = TopologicalSorter.topological_sort_kahn(graph)
        
        if order is None:
            return None
        
        return [task_names[i] for i in order]
    
    @staticmethod
    def estimate_project_time(task_names: List[str], 
                             durations: List[float],
                             deps: List[Tuple[int, int]]) -> Tuple[float, List[int]]:
        """
        Оценить общее время выполнения проекта (критический путь).
        """
        task_count = len(task_names)
        earliest_start = [0.0] * task_count
        predecessors = [[] for _ in range(task_count)]
        
        for u, v in deps:
            if 0 <= u < task_count and 0 <= v < task_count:
                predecessors[v].append(u)
        
        changed = True
        while changed:
            changed = False
            for task in range(task_count):
                if predecessors[task]:
                    max_pred_time = max(earliest_start[pred] + durations[pred]
                                       for pred in predecessors[task])
                    if max_pred_time > earliest_start[task]:
                        earliest_start[task] = max_pred_time
                        changed = True
        
        total_time = max(earliest_start[i] + durations[i]
                        for i in range(task_count))
        
        critical_path = []
        for i in range(task_count):
            if earliest_start[i] + durations[i] == total_time:
                critical_path.append(i)
        
        return total_time, critical_path
    
    @staticmethod
    def validate_schedule(task_count: int, deps: List[Tuple[int, int]]) -> Tuple[bool, Optional[List[int]]]:
        """
        Проверить возможность выполнения расписания (отсутствие циклов).
        """
        graph = GraphList(task_count, directed=True)
        
        for u, v in deps:
            if 0 <= u < task_count and 0 <= v < task_count:
                graph.add_edge(u, v)
        
        cycle = TopologicalSorter.detect_cycle_directed(graph)
        return cycle is None, cycle

def run_demo():
    """Запустить демонстрацию практических задач."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ НА ГРАФАХ")
    print("=" * 70)
    
    # ЗАДАЧА 1: ЛАБИРИНТ
    print("\n" + "=" * 70)
    print("ЗАДАЧА 1: Поиск пути в лабиринте")
    print("=" * 70)
    
    maze = [
        ['S', ' ', '#', ' ', ' '],
        ['#', ' ', '#', ' ', '#'],
        [' ', ' ', ' ', ' ', ' '],
        [' ', '#', '#', '#', ' '],
        [' ', ' ', ' ', ' ', 'E']
    ]
    
    print("\nИсходный лабиринт:")
    for row in maze:
        print(''.join(row))
    
    path = MazeSolver.find_path(maze)
    
    if path:
        print(f"\nНайден маршрут длиной {len(path)}:")
        print("Координаты пути:", path)
        print("\nЛабиринт с решением:")
        print(MazeSolver.show_path(maze, path))
    else:
        print("\nПуть не существует")
    
    # ЗАДАЧА 2: СЕТЬ
    print("\n" + "=" * 70)
    print("ЗАДАЧА 2: Анализ сетевой связности")
    print("=" * 70)
    
    connections = [
        (0, 1), (1, 2), (0, 2),
        (3, 4), (4, 5),
        (6, 7),
    ]
    nodes = 9
    
    print(NetworkAnalyzer.generate_report(connections, nodes))
    
    # ЗАДАЧА 3: ЗАДАЧИ
    print("\n" + "=" * 70)
    print("ЗАДАЧА 3: Планирование задач")
    print("=" * 70)
    
    tasks = ['A', 'B', 'C', 'D', 'E', 'F']
    times = [2, 3, 1, 2, 1, 3]
    dependencies = [
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 3),
        (3, 4),
        (4, 5)
    ]
    
    feasible, cycle = TaskPlanner.validate_schedule(len(tasks), dependencies)
    print(f"\nРасписание выполнимо: {'Да' if feasible else f'Нет (цикл: {cycle})'}")
    
    order = TaskPlanner.schedule_tasks(tasks, dependencies)
    if order:
        print(f"Порядок выполнения: {' → '.join(order)}")
    else:
        print("Невозможно определить порядок (циклические зависимости)")
    
    if feasible:
        duration, critical = TaskPlanner.estimate_project_time(tasks, times, dependencies)
        print(f"\nОбщая длительность: {duration}")
        print(f"Критический путь: {' → '.join([tasks[i] for i in critical])}")

if __name__ == '__main__':
    run_demo()