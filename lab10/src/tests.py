import unittest
from modules.graph_representation import GraphMatrix, GraphList
from modules.graph_traversal import GraphExplorer
from modules.shortest_path import PathFinder, TopologicalSorter

class TestGraphMatrix(unittest.TestCase):
    """Тесты для матричного представления графа."""
    
    def setUp(self):
        self.g = GraphMatrix(5, directed=False, weighted=False)
    
    def test_add_edge(self):
        self.g.add_edge(0, 1)
        self.assertTrue(self.g.has_edge(0, 1))
        self.assertTrue(self.g.has_edge(1, 0))
    
    def test_remove_edge(self):
        self.g.add_edge(0, 1)
        self.g.remove_edge(0, 1)
        self.assertFalse(self.g.has_edge(0, 1))
    
    def test_has_edge(self):
        self.assertFalse(self.g.has_edge(0, 1))
        self.g.add_edge(0, 1)
        self.assertTrue(self.g.has_edge(0, 1))
    
    def test_get_neighbors(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 2)
        neighbors = self.g.get_neighbors(0)
        self.assertIn(1, neighbors)
        self.assertIn(2, neighbors)
        self.assertEqual(len(neighbors), 2)
    
    def test_directed_graph(self):
        directed_g = GraphMatrix(3, directed=True)
        directed_g.add_edge(0, 1)
        self.assertTrue(directed_g.has_edge(0, 1))
        self.assertFalse(directed_g.has_edge(1, 0))
    
    def test_weighted_graph(self):
        weighted_g = GraphMatrix(3, directed=False, weighted=True)
        weighted_g.add_edge(0, 1, weight=5.0)
        self.assertEqual(weighted_g.get_weight(0, 1), 5.0)
        self.assertEqual(weighted_g.get_weight(1, 0), 5.0)

class TestGraphList(unittest.TestCase):
    """Тесты для списочного представления графа."""
    
    def setUp(self):
        self.g = GraphList(5, directed=False, weighted=False)
    
    def test_add_edge(self):
        self.g.add_edge(0, 1)
        self.assertTrue(self.g.has_edge(0, 1))
        self.assertTrue(self.g.has_edge(1, 0))
    
    def test_remove_edge(self):
        self.g.add_edge(0, 1)
        self.g.remove_edge(0, 1)
        self.assertFalse(self.g.has_edge(0, 1))
    
    def test_has_edge(self):
        self.assertFalse(self.g.has_edge(0, 1))
        self.g.add_edge(0, 1)
        self.assertTrue(self.g.has_edge(0, 1))
    
    def test_get_neighbors(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 2)
        neighbors = self.g.get_neighbors(0)
        self.assertIn(1, neighbors)
        self.assertIn(2, neighbors)
        self.assertEqual(len(neighbors), 2)
    
    def test_directed_graph(self):
        directed_g = GraphList(3, directed=True)
        directed_g.add_edge(0, 1)
        self.assertTrue(directed_g.has_edge(0, 1))
        self.assertFalse(directed_g.has_edge(1, 0))
    
    def test_weighted_graph(self):
        weighted_g = GraphList(3, directed=False, weighted=True)
        weighted_g.add_edge(0, 1, weight=5.0)
        self.assertEqual(weighted_g.get_weight(0, 1), 5.0)
        self.assertEqual(weighted_g.get_weight(1, 0), 5.0)

class TestBFS(unittest.TestCase):
    """Тесты для алгоритма BFS."""
    
    def setUp(self):
        self.g = GraphList(6)
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 3)
        self.g.add_edge(1, 2)
        self.g.add_edge(1, 4)
        self.g.add_edge(2, 5)
        self.g.add_edge(3, 4)
        self.g.add_edge(4, 5)
    
    def test_bfs_distances(self):
        distances, _ = GraphExplorer.bfs(self.g, 0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[3], 1)
        self.assertEqual(distances[2], 2)
    
    def test_bfs_shortest_path(self):
        path = GraphExplorer.bfs_shortest_path(self.g, 0, 5)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 5)
        self.assertEqual(len(path), 4)
    
    def test_bfs_same_vertex(self):
        path = GraphExplorer.bfs_shortest_path(self.g, 0, 0)
        self.assertEqual(path, [0])
    
    def test_bfs_no_path(self):
        disconnected = GraphList(3)
        disconnected.add_edge(0, 1)
        path = GraphExplorer.bfs_shortest_path(disconnected, 0, 2)
        self.assertIsNone(path)

class TestDFS(unittest.TestCase):
    """Тесты для алгоритма DFS."""
    
    def setUp(self):
        self.g = GraphList(4)
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 2)
        self.g.add_edge(1, 3)
    
    def test_dfs_recursive(self):
        visited, _ = GraphExplorer.dfs_recursive(self.g, 0)
        self.assertEqual(visited[0], 0)
        self.assertIn(1, visited)
        self.assertIn(2, visited)
        self.assertIn(3, visited)
    
    def test_dfs_iterative(self):
        visited, _ = GraphExplorer.dfs_iterative(self.g, 0)
        self.assertEqual(visited[0], 0)
        self.assertIn(1, visited)
        self.assertIn(2, visited)
        self.assertIn(3, visited)
    
    def test_dfs_all_vertices(self):
        visited, _ = GraphExplorer.dfs_recursive(self.g, 0)
        self.assertEqual(len(visited), 4)

class TestConnectedComponents(unittest.TestCase):
    """Тесты для поиска компонент связности."""
    
    def test_single_component(self):
        g = GraphList(4)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        
        components = GraphExplorer.find_connected_components(g)
        self.assertEqual(len(components), 1)
    
    def test_multiple_components(self):
        g = GraphList(6)
        g.add_edge(0, 1)
        g.add_edge(2, 3)
        g.add_edge(4, 5)
        
        components = GraphExplorer.find_connected_components(g)
        self.assertEqual(len(components), 3)
    
    def test_isolated_vertices(self):
        g = GraphList(3)
        components = GraphExplorer.find_connected_components(g)
        self.assertEqual(len(components), 3)

class TestDijkstra(unittest.TestCase):
    """Тесты для алгоритма Дейкстры."""
    
    def setUp(self):
        self.g = GraphList(5, weighted=True)
        self.g.add_edge(0, 1, 4)
        self.g.add_edge(0, 2, 1)
        self.g.add_edge(2, 1, 2)
        self.g.add_edge(1, 3, 1)
        self.g.add_edge(2, 3, 5)
        self.g.add_edge(3, 4, 3)
    
    def test_dijkstra_distances(self):
        distances, _ = PathFinder.dijkstra(self.g, 0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 3)
        self.assertEqual(distances[2], 1)
        self.assertEqual(distances[3], 4)
    
    def test_dijkstra_shortest_path(self):
        path = PathFinder.dijkstra_shortest_path(self.g, 0, 3)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 3)
    
    def test_dijkstra_unreachable(self):
        disconnected = GraphList(3, weighted=True)
        disconnected.add_edge(0, 1, 1)
        distances, _ = PathFinder.dijkstra(disconnected, 0)
        self.assertEqual(distances[2], float('inf'))

class TestTopologicalSort(unittest.TestCase):
    """Тесты для топологической сортировки."""
    
    def setUp(self):
        self.dag = GraphList(6, directed=True)
        self.dag.add_edge(0, 1)
        self.dag.add_edge(0, 2)
        self.dag.add_edge(1, 3)
        self.dag.add_edge(2, 3)
        self.dag.add_edge(3, 4)
        self.dag.add_edge(3, 5)
    
    def test_topological_sort_dfs(self):
        result = TopologicalSorter.topological_sort_dfs(self.dag)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.assertLess(result.index(0), result.index(1))
        self.assertLess(result.index(0), result.index(2))
    
    def test_topological_sort_kahn(self):
        result = TopologicalSorter.topological_sort_kahn(self.dag)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
    
    def test_cycle_detection(self):
        cyclic = GraphList(3, directed=True)
        cyclic.add_edge(0, 1)
        cyclic.add_edge(1, 2)
        cyclic.add_edge(2, 0)
        
        result = TopologicalSorter.topological_sort_dfs(cyclic)
        self.assertIsNone(result)

class TestCycleDetection(unittest.TestCase):
    """Тесты для обнаружения циклов."""
    
    def test_cycle_in_undirected_graph(self):
        g = GraphList(4)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        
        cycle = GraphExplorer.find_cycle_undirected(g)
        self.assertIsNotNone(cycle)
    
    def test_no_cycle(self):
        g = GraphList(4)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        
        cycle = GraphExplorer.find_cycle_undirected(g)
        self.assertIsNone(cycle)

class TestBipartiteGraph(unittest.TestCase):
    """Тесты для проверки двудольности."""
    
    def test_bipartite_graph(self):
        g = GraphList(4)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 3)
        
        self.assertTrue(GraphExplorer.is_bipartite(g))
    
    def test_non_bipartite_graph(self):
        g = GraphList(3)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        
        self.assertFalse(GraphExplorer.is_bipartite(g))

class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев."""
    
    def test_single_vertex(self):
        g = GraphList(1)
        distances, _ = GraphExplorer.bfs(g, 0)
        self.assertEqual(distances[0], 0)
    
    def test_self_loop(self):
        g = GraphList(2)
        g.add_edge(0, 0)
        neighbors = g.get_neighbors(0)
        self.assertIn(0, neighbors)
    
    def test_empty_graph(self):
        g = GraphList(5)
        components = GraphExplorer.find_connected_components(g)
        self.assertEqual(len(components), 5)

if __name__ == '__main__':
    unittest.main()