from typing import Dict, List, Tuple, Set, Optional
from collections import deque
from modules.graph_representation import GraphList

class GraphExplorer:
    """Класс для алгоритмов обхода графов."""
    
    @staticmethod
    def bfs(graph: GraphList, start: int) -> Tuple[Dict[int, int], Dict[int, Optional[int]]]:
        """
        Поиск в ширину (BFS).
        
        Сложность: O(V + E)
        Память: O(V)
        """
        distances = {start: 0}
        parents = {start: None}
        queue = deque([start])
        
        while queue:
            v = queue.popleft()
            
            for nb in graph.get_neighbors(v):
                if nb not in distances:
                    distances[nb] = distances[v] + 1
                    parents[nb] = v
                    queue.append(nb)
        
        return distances, parents
    
    @staticmethod
    def bfs_shortest_path(graph: GraphList, start: int, end: int) -> Optional[List[int]]:
        """Найти кратчайший путь между двумя вершинами используя BFS."""
        if start == end:
            return [start]
        
        distances, parents = GraphExplorer.bfs(graph, start)
        
        if end not in distances:
            return None
        
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = parents[cur]
        
        return path[::-1]
    
    @staticmethod
    def dfs_recursive(graph: GraphList, start: int) -> Tuple[List[int], Dict[int, Optional[int]]]:
        """
        Поиск в глубину (DFS) - рекурсивная реализация.
        
        Сложность: O(V + E)
        """
        visited = set()
        order = []
        parents = {}
        
        def dfs_helper(vertex: int, parent: Optional[int] = None):
            visited.add(vertex)
            order.append(vertex)
            parents[vertex] = parent
            
            for nb in graph.get_neighbors(vertex):
                if nb not in visited:
                    dfs_helper(nb, vertex)
        
        dfs_helper(start)
        return order, parents
    
    @staticmethod
    def dfs_iterative(graph: GraphList, start: int) -> Tuple[List[int], Dict[int, Optional[int]]]:
        """
        Поиск в глубину (DFS) - итеративная реализация.
        
        Сложность: O(V + E)
        """
        visited = set()
        order = []
        parents = {start: None}
        stack = [start]
        
        while stack:
            v = stack.pop()
            
            if v not in visited:
                visited.add(v)
                order.append(v)
                
                for nb in reversed(graph.get_neighbors(v)):
                    if nb not in visited:
                        if nb not in parents:
                            parents[nb] = v
                        stack.append(nb)
        
        return order, parents
    
    @staticmethod
    def find_connected_components(graph: GraphList) -> List[Set[int]]:
        """
        Найти все компоненты связности неориентированного графа.
        
        Сложность: O(V + E)
        """
        visited = set()
        components = []
        
        def dfs(v: int, comp: Set[int]):
            visited.add(v)
            comp.add(v)
            
            for nb in graph.get_neighbors(v):
                if nb not in visited:
                    dfs(nb, comp)
        
        for v in range(graph.vertex_count):
            if v not in visited:
                comp = set()
                dfs(v, comp)
                components.append(comp)
        
        return components
    
    @staticmethod
    def find_cycle_undirected(graph: GraphList) -> Optional[List[int]]:
        """
        Найти цикл в неориентированном графе.
        
        Сложность: O(V + E)
        """
        visited = set()
        parent = {}
        cycle_path = []
        
        def dfs(v: int, p: int = -1) -> bool:
            visited.add(v)
            parent[v] = p
            
            for nb in graph.get_neighbors(v):
                if nb not in visited:
                    if dfs(nb, v):
                        return True
                elif nb != p:
                    cur = v
                    while cur != nb:
                        cycle_path.append(cur)
                        cur = parent[cur]
                    cycle_path.append(nb)
                    return True
            
            return False
        
        for v in range(graph.vertex_count):
            if v not in visited:
                if dfs(v):
                    return cycle_path
        
        return None
        
    @staticmethod
    def is_bipartite(graph: GraphList) -> bool:
        """
        Проверить, является ли граф двудольным.
        
        Сложность: O(V + E)
        """
        color = {-1: None}
        
        def bfs_check(start: int) -> bool:
            q = deque([start])
            color[start] = 0
            
            while q:
                v = q.popleft()
                
                for nb in graph.get_neighbors(v):
                    if nb not in color:
                        color[nb] = 1 - color[v]
                        q.append(nb)
                    elif color[nb] == color[v]:
                        return False
            
            return True
        
        for v in range(graph.vertex_count):
            if v not in color:
                if not bfs_check(v):
                    return False
        
        return True