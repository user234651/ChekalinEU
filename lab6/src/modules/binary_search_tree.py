class BNode:
    """Узел бинарного дерева поиска."""

    def __init__(self, value):
        """
        Инициализация узла.
        Сложность: O(1)
        """
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return f"BNode({self.value})"

class BinTree:
    """Бинарное дерево поиска."""

    def __init__(self):
        """Создаёт пустое дерево."""
        self.root = None

    def add(self, value):
        """
        Вставка значения.
        Сложность: средняя O(log n), худшая O(n)
        """
        if self.root is None:
            self.root = BNode(value)
        else:
            self._add_rec(self.root, value)

    def _add_rec(self, node, value):
        """
        Вспомогательная рекурсивная вставка.
        Сложность: как у add
        """
        if value < node.value:
            if node.left is None:
                node.left = BNode(value)
            else:
                self._add_rec(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = BNode(value)
            else:
                self._add_rec(node.right, value)
        # дубликаты игнорируются

    def find(self, value):
        """
        Поиск узла по значению.
        Сложность: средняя O(log n), худшая O(n)
        """
        return self._find_rec(self.root, value)

    def _find_rec(self, node, value):
        """
        Рекурсивный поиск.
        """
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self._find_rec(node.left, value)
        else:
            return self._find_rec(node.right, value)

    def remove(self, value):
        """
        Удаление значения.
        Сложность: средняя O(log n), худшая O(n)
        """
        if self.root is None:
            return False

        if self.find(value) is None:
            return False

        self.root = self._remove_rec(self.root, value)
        return True

    def _remove_rec(self, node, value):
        """
        Рекурсивное удаление узла.
        """
        if node is None:
            return node

        if value < node.value:
            node.left = self._remove_rec(node.left, value)
        elif value > node.value:
            node.right = self._remove_rec(node.right, value)
        else:
            # Узел найден
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_node = self._min_node(node.right)
            node.value = min_node.value
            node.right = self._remove_rec(node.right, min_node.value)

        return node

    def _min_node(self, node):
        """
        Поиск минимума в поддереве.
        Сложность: O(h)
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_min(self, node=None):
        """
        Возвращает минимальный узел в поддереве.
        Сложность: O(h)
        """
        if node is None:
            node = self.root

        if node is None:
            return None

        return self._min_node(node)

    def get_max(self, node=None):
        """
        Возвращает максимальный узел в поддереве.
        Сложность: O(h)
        """
        if node is None:
            node = self.root

        if node is None:
            return None

        current = node
        while current.right is not None:
            current = current.right

        return current

    def compute_height(self, node=None):
        """
        Вычисление высоты поддерева.
        Сложность: O(n)
        """
        if node is None:
            node = self.root

        if node is None:
            return -1

        left_h = self.compute_height(node.left) if node.left else -1
        right_h = self.compute_height(node.right) if node.right else -1

        return max(left_h, right_h) + 1

    def validate_bst(self):
        """
        Проверка корректности BST.
        Сложность: O(n)
        """
        return self._validate_rec(self.root, float('-inf'), float('inf'))

    def _validate_rec(self, node, min_val, max_val):
        """Вспомогательная проверка."""
        if node is None:
            return True

        if not (min_val < node.value < max_val):
            return False

        return (self._validate_rec(node.left, min_val, node.value) and
                self._validate_rec(node.right, node.value, max_val))

    def __contains__(self, value):
        return self.find(value) is not None

    def __str__(self):
        return self._render()

    def _render(self, node=None, prefix="", is_left=True):
        """
        Текстовая визуализация.
        """
        if node is None:
            node = self.root

        if node is None:
            return "Empty tree"

        result = ""

        if node.right:
            result += self._render(node.right, prefix + ("│   " if is_left else "    "), False)

        result += prefix + ("└── " if is_left else "┌── ") + str(node.value) + "\n"

        if node.left:
            result += self._render(node.left, prefix + ("    " if is_left else "│   "), True)

        return result

    def size(self):
        """
        Количество узлов в дереве.
        Сложность: O(n)
        """
        return self._size_rec(self.root)

    def _size_rec(self, node):
        """Рекурсивный подсчёт размера."""
        if node is None:
            return 0
        return 1 + self._size_rec(node.left) + self._size_rec(node.right)
