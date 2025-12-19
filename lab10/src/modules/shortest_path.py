from typing import Dict, List, Optional, Tuple
from collections import deque
import heapq
from modules.graph_representation import GraphList

class PathFinder:
    """Класс для алгоритмов поиска кратчайших путей."""
    
    @staticmethod
    def dijkstra(graph: GraphList, start: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Алгоритм Дейкстры для поиска кратчайших путей.
        
        Сложность: O((V + E) log V)
        Память: O(V)
        
        Предусловия:
        - Все веса ребер должны быть неотрицательные
        - Граф должен быть взвешенным
        """
        distances = {i: float('inf') for i in range(graph.vertex_count)}
        distances[start] = 0
        parents = {start: None}
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            cur_dist, v = heapq.heappop(pq)
            
            if v in visited:
                continue
            
            visited.add(v)
            
            if cur_dist > distances[v]:
                continue
            
            for nb in graph.get_neighbors(v):
                w = graph.get_weight(v, nb)
                
                if w != float('inf'):
                    new_dist = distances[v] + w
                    
                    if new_dist < distances[nb]:
                        distances[nb] = new_dist
                        parents[nb] = v
                        heapq.heappush(pq, (new_dist, nb))
        
        return distances, parents
    
    @staticmethod
    def dijkstra_shortest_path(graph: GraphList, start: int, end: int) -> Optional[List[int]]:
        """Найти кратчайший путь между двумя вершинами используя Дейкстру."""
        if start == end:
            return [start]
        
        distances, parents = PathFinder.dijkstra(graph, start)
        
        if distances[end] == float('inf'):
            return None
        
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = parents.get(cur)
        
        return path[::-1]
    
    @staticmethod
    def dijkstra_all_distances(graph: GraphList, start: int) -> Dict[int, float]:
        """Получить кратчайшие расстояния от start до всех вершин."""
        distances, _ = PathFinder.dijkstra(graph, start)
        return distances

class TopologicalSorter:
    """Класс для топологической сортировки."""
    
    @staticmethod
    def topological_sort_dfs(graph: GraphList) -> Optional[List[int]]:
        """
        Топологическая сортировка с использованием DFS.
        
        Сложность: O(V + E)
        Память: O(V)
        
        Применимость:
        - Работает только для DAG
        - Возвращает None если граф содержит цикл
        """
        visited = set()
        rec_stack = set()
        result = []
        
        def dfs(v: int) -> bool:
            visited.add(v)
            rec_stack.add(v)
            
            for nb in graph.get_neighbors(v):
                if nb not in visited:
                    if not dfs(nb):
                        return False
                elif nb in rec_stack:
                    return False
            
            rec_stack.remove(v)
            result.append(v)
            return True
        
        for v in range(graph.vertex_count):
            if v not in visited:
                if not dfs(v):
                    return None
        
        return result[::-1]
    
    @staticmethod
    def topological_sort_kahn(graph: GraphList) -> Optional[List[int]]:
        """
        Топологическая сортировка алгоритмом Кана.
        
        Сложность: O(V + E)
        Память: O(V)
        """
        in_degree = [0] * graph.vertex_count
        
        for v in range(graph.vertex_count):
            for nb in graph.get_neighbors(v):
                in_degree[nb] += 1
        
        q = deque([v for v in range(graph.vertex_count) if in_degree[v] == 0])
        result = []
        
        while q:
            v = q.popleft()
            result.append(v)
            
            for nb in graph.get_neighbors(v):
                in_degree[nb] -= 1
                if in_degree[nb] == 0:
                    q.append(nb)
        
        if len(result) == graph.vertex_count:
            return result
        else:
            return None
    
    @staticmethod
    def detect_cycle_directed(graph: GraphList) -> Optional[List[int]]:
        """
        Обнаружить цикл в ориентированном графе.
        
        Сложность: O(V + E)
        """
        visited = set()
        rec_stack = set()
        parent = {}
        
        def dfs(v: int) -> Optional[List[int]]:
            visited.add(v)
            rec_stack.add(v)
            
            for nb in graph.get_neighbors(v):
                if nb not in visited:
                    parent[nb] = v
                    res = dfs(nb)
                    if res:
                        return res
                elif nb in rec_stack:
                    cycle = [nb]
                    cur = v
                    while cur != nb:
                        cycle.append(cur)
                        cur = parent[cur]
                    return cycle
            
            rec_stack.remove(v)
            return None
        
        for v in range(graph.vertex_count):
            if v not in visited:
                res = dfs(v)
                if res:
                    return res
        
        return None