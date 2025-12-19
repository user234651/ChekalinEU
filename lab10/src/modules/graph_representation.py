from typing import Dict, List
from collections import defaultdict
import sys

class GraphMatrix:
    """
    Представление графа матрицей смежности.
    
    Сложность операций:
    - Добавление ребра: O(1)
    - Удаление ребра: O(1)
    - Проверка ребра: O(1)
    - Получение соседей: O(V)
    - Память: O(V²)
    """
    
    def __init__(self, vertices: int, directed: bool = False, weighted: bool = False):
        self.vertex_count = vertices
        self.is_directed = directed
        self.is_weighted = weighted
        
        if weighted:
            self.matrix = [[float('inf') for _ in range(vertices)] for _ in range(vertices)]
            for i in range(vertices):
                self.matrix[i][i] = 0
        else:
            self.matrix = [[False for _ in range(vertices)] for _ in range(vertices)]
        
        self.edge_counter = 0
    
    def add_edge(self, u: int, v: int, weight: float = 1) -> None:
        """Добавить ребро в граф."""
        if u >= self.vertex_count or v >= self.vertex_count or u < 0 or v < 0:
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertex_count-1}]")
        
        if self.is_weighted:
            self.matrix[u][v] = weight
            if not self.is_directed:
                self.matrix[v][u] = weight
        else:
            self.matrix[u][v] = True
            if not self.is_directed:
                self.matrix[v][u] = True
        
        self.edge_counter += 1
    
    def remove_edge(self, u: int, v: int) -> None:
        """Удалить ребро из графа."""
        if u >= self.vertex_count or v >= self.vertex_count or u < 0 or v < 0:
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertex_count-1}]")
        
        if self.is_weighted:
            if self.matrix[u][v] != float('inf'):
                self.matrix[u][v] = float('inf')
                if not self.is_directed:
                    self.matrix[v][u] = float('inf')
                self.edge_counter -= 1
        else:
            if self.matrix[u][v]:
                self.matrix[u][v] = False
                if not self.is_directed:
                    self.matrix[v][u] = False
                self.edge_counter -= 1
    
    def has_edge(self, u: int, v: int) -> bool:
        """Проверить наличие ребра."""
        if u >= self.vertex_count or v >= self.vertex_count or u < 0 or v < 0:
            return False
        
        if self.is_weighted:
            return self.matrix[u][v] != float('inf')
        return self.matrix[u][v]
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Получить всех соседей вершины."""
        if vertex >= self.vertex_count or vertex < 0:
            raise ValueError(f"Вершина должна быть в диапазоне [0, {self.vertex_count-1}]")
        
        neighbors = []
        for i in range(self.vertex_count):
            if self.is_weighted:
                if self.matrix[vertex][i] != float('inf') and i != vertex:
                    neighbors.append(i)
            else:
                if self.matrix[vertex][i]:
                    neighbors.append(i)
        return neighbors
    
    def get_weight(self, u: int, v: int) -> float:
        """Получить вес ребра."""
        if self.is_weighted:
            return self.matrix[u][v]
        return 1 if self.has_edge(u, v) else float('inf')
    
    def get_memory_usage(self) -> int:
        """Получить приблизительное потребление памяти в байтах."""
        element_size = sys.getsizeof(True) if not self.is_weighted else sys.getsizeof(1.0)
        return sys.getsizeof(self.matrix) + self.vertex_count**2 * element_size


class GraphList:
    """
    Представление графа списком смежности.
    
    Сложность операций:
    - Добавление ребра: O(1)
    - Удаление ребра: O(E) в худшем случае
    - Проверка ребра: O(degree(v))
    - Получение соседей: O(degree(v))
    - Память: O(V + E)
    """
    
    def __init__(self, vertices: int, directed: bool = False, weighted: bool = False):
        self.vertex_count = vertices
        self.is_directed = directed
        self.is_weighted = weighted
        
        self.adj_list: Dict[int, List] = defaultdict(list)
        self.edge_counter = 0
    
    def add_edge(self, u: int, v: int, weight: float = 1) -> None:
        """Добавить ребро в граф."""
        if u >= self.vertex_count or v >= self.vertex_count or u < 0 or v < 0:
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertex_count-1}]")
        
        if self.is_weighted:
            self.adj_list[u].append((v, weight))
            if not self.is_directed:
                self.adj_list[v].append((u, weight))
        else:
            self.adj_list[u].append(v)
            if not self.is_directed:
                self.adj_list[v].append(u)
        
        self.edge_counter += 1
    
    def remove_edge(self, u: int, v: int) -> None:
        """Удалить ребро из графа."""
        if u >= self.vertex_count or v >= self.vertex_count or u < 0 or v < 0:
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertex_count-1}]")
        
        if self.is_weighted:
            before = len(self.adj_list[u])
            self.adj_list[u] = [(nb, w) for nb, w in self.adj_list[u] if nb != v]
            if not self.is_directed:
                self.adj_list[v] = [(nb, w) for nb, w in self.adj_list[v] if nb != u]
        else:
            before = len(self.adj_list[u])
            self.adj_list[u] = [nb for nb in self.adj_list[u] if nb != v]
            if not self.is_directed:
                self.adj_list[v] = [nb for nb in self.adj_list[v] if nb != u]
        
        if len(self.adj_list[u]) < before:
            self.edge_counter -= 1
    
    def has_edge(self, u: int, v: int) -> bool:
        """Проверить наличие ребра."""
        if u >= self.vertex_count or v >= self.vertex_count or u < 0 or v < 0:
            return False
        
        if self.is_weighted:
            return any(nb == v for nb, _ in self.adj_list[u])
        return v in self.adj_list[u]
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Получить всех соседей вершины."""
        if vertex >= self.vertex_count or vertex < 0:
            raise ValueError(f"Вершина должна быть в диапазоне [0, {self.vertex_count-1}]")
        
        if self.is_weighted:
            return [nb for nb, _ in self.adj_list[vertex]]
        return self.adj_list[vertex].copy()
    
    def get_weight(self, u: int, v: int) -> float:
        """Получить вес ребра."""
        if self.is_weighted:
            for nb, w in self.adj_list[u]:
                if nb == v:
                    return w
            return float('inf')
        return 1 if self.has_edge(u, v) else float('inf')
    
    def get_memory_usage(self) -> int:
        """Получить приблизительное потребление памяти в байтах."""
        total = sys.getsizeof(self.adj_list)
        for v, neighbors in self.adj_list.items():
            total += sys.getsizeof(v) + sys.getsizeof(neighbors)
            for nb in neighbors:
                if isinstance(nb, tuple):
                    total += sys.getsizeof(nb)
                else:
                    total += sys.getsizeof(nb)
        return total