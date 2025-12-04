import unittest
from modules.binary_search_tree import BinTree, BNode
from modules.tree_traversal import *

class TestBinTree(unittest.TestCase):
    """Тесты для бинарного дерева поиска."""

    def setUp(self):
        """Настройка."""
        self.tree = BinTree()

    def test_insert_and_find(self):
        """Тест вставки и поиска."""
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.tree.add(value)

        for value in values:
            node = self.tree.find(value)
            self.assertIsNotNone(node)
            self.assertEqual(node.value, value)

        self.assertIsNone(self.tree.find(100))
        self.assertIsNone(self.tree.find(10))

    def test_remove(self):
        """Тест удаления."""
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.tree.add(value)

        success = self.tree.remove(20)
        self.assertTrue(success)
        self.assertIsNone(self.tree.find(20))
        self.assertTrue(self.tree.validate_bst())

        success = self.tree.remove(30)
        self.assertTrue(success)
        self.assertIsNone(self.tree.find(30))
        self.assertTrue(self.tree.validate_bst())

        success = self.tree.remove(50)
        self.assertTrue(success)
        self.assertIsNone(self.tree.find(50))
        self.assertTrue(self.tree.validate_bst())

        success = self.tree.remove(100)
        self.assertFalse(success)

    def test_min_max(self):
        """Тест минимума и максимума."""
        values = [50, 30, 70, 20, 40, 60, 80]

        for value in values:
            self.tree.add(value)

        self.assertEqual(self.tree.get_min().value, 20)
        self.assertEqual(self.tree.get_max().value, 80)

        node_30 = self.tree.find(30)
        self.assertEqual(self.tree.get_min(node_30).value, 20)
        self.assertEqual(self.tree.get_max(node_30).value, 40)

    def test_height(self):
        """Тест высоты."""
        self.assertEqual(self.tree.compute_height(), -1)

        self.tree.add(50)
        self.assertEqual(self.tree.compute_height(), 0)

        self.tree.add(30)
        self.tree.add(70)
        self.assertEqual(self.tree.compute_height(), 1)

        self.tree.add(20)
        self.tree.add(40)
        self.assertEqual(self.tree.compute_height(), 2)

    def test_validate_bst(self):
        """Тест валидации BST."""
        values = [50, 30, 70, 20, 40, 60, 80]
        for value in values:
            self.tree.add(value)
        self.assertTrue(self.tree.validate_bst())

        # Нарушаем вручную
        self.tree.root = BNode(50)
        self.tree.root.left = BNode(60)
        self.tree.root.right = BNode(70)
        self.assertFalse(self.tree.validate_bst())

    def test_traversals(self):
        """Тест обходов."""
        values = [50, 30, 70, 20, 40, 60, 80]
        sorted_values = sorted(values)

        for value in values:
            self.tree.add(value)

        self.assertEqual(inorder_rec(self.tree.root), sorted_values)
        self.assertEqual(inorder_iter(self.tree.root), sorted_values)

        preorder_result = preorder_rec(self.tree.root)
        self.assertEqual(preorder_result[0], 50)

        postorder_result = postorder_rec(self.tree.root)
        self.assertEqual(postorder_result[-1], 50)

        level_order_vals = level_order(self.tree.root)
        self.assertEqual(len(level_order_vals), len(values))

    def test_size(self):
        """Тест размера."""
        self.assertEqual(self.tree.size(), 0)

        values = [50, 30, 70, 20, 40]
        for value in values:
            self.tree.add(value)

        self.assertEqual(self.tree.size(), len(values))

        self.tree.remove(30)
        self.assertEqual(self.tree.size(), len(values) - 1)

if __name__ == "__main__":
    unittest.main()
