class SmallHeap:
    """
    Мин-куча: каждый узел <= потомков. Корень — минимум.

    Сложность: build O(n), push/pop O(log n)
    """

    def __init__(self, array=None):
        self.heap = []
        if array is not None:
            self.heapify(array)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return f"SmallHeap({self.heap})"

    def _parent(self, index):
        if index == 0:
            return -1
        return (index - 1) // 2

    def _left(self, index):
        left = 2 * index + 1
        return left if left < len(self.heap) else -1

    def _right(self, index):
        right = 2 * index + 2
        return right if right < len(self.heap) else -1

    def _bubble_up(self, index):
        parent = self._parent(index)
        while parent >= 0 and self.heap[parent] > self.heap[index]:
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
            parent = self._parent(index)

    def _sink_down(self, index):
        while True:
            left = self._left(index)
            right = self._right(index)
            smallest = index

            if left != -1 and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right != -1 and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def push(self, value):
        """Вставка. Сложность: O(log n)"""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        """Извлечь минимум. Сложность: O(log n)"""
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)
        return root

    def top(self):
        """Просмотр минимума. Сложность: O(1)"""
        return self.heap[0] if self.heap else None

    def heapify(self, array):
        """Построение кучи из массива. Сложность: O(n)"""
        self.heap = array[:]
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sink_down(i)

    def validate_heap(self):
        """Проверка свойства min-кучи. Сложность: O(n)"""
        for i in range(len(self.heap)):
            left = self._left(i)
            right = self._right(i)
            if left != -1 and self.heap[i] > self.heap[left]:
                return False
            if right != -1 and self.heap[i] > self.heap[right]:
                return False
        return True

    def render(self):
        """Текстовая визуализация дерева."""
        if not self.heap:
            return "Empty heap"

        def _rec(idx, prefix="", is_left=True):
            result = ""
            right = self._right(idx)
            if right != -1:
                result += _rec(right, prefix + ("│   " if is_left else "    "), False)

            result += prefix + ("└── " if is_left else "┌── ") + str(self.heap[idx]) + "\n"

            left = self._left(idx)
            if left != -1:
                result += _rec(left, prefix + ("    " if is_left else "│   "), True)

            return result

        return _rec(0)


class LargeHeap:
    """
    Макс-куча: каждый узел >= потомков. Корень — максимум.

    Сложность: build O(n), push/pop O(log n)
    """

    def __init__(self, array=None):
        self.heap = []
        if array is not None:
            self.heapify(array)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return f"LargeHeap({self.heap})"

    def _parent(self, index):
        if index == 0:
            return -1
        return (index - 1) // 2

    def _left(self, index):
        left = 2 * index + 1
        return left if left < len(self.heap) else -1

    def _right(self, index):
        right = 2 * index + 2
        return right if right < len(self.heap) else -1

    def _bubble_up(self, index):
        parent = self._parent(index)
        while parent >= 0 and self.heap[parent] < self.heap[index]:
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
            parent = self._parent(index)

    def _sink_down(self, index):
        while True:
            left = self._left(index)
            right = self._right(index)
            largest = index

            if left != -1 and self.heap[left] > self.heap[largest]:
                largest = left
            if right != -1 and self.heap[right] > self.heap[largest]:
                largest = right

            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break

    def push(self, value):
        """Вставка. Сложность: O(log n)"""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        """Извлечение максимума. Сложность: O(log n)"""
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)
        return root

    def top(self):
        """Просмотр максимума. Сложность: O(1)"""
        return self.heap[0] if self.heap else None

    def heapify(self, array):
        """Построение max-кучи из массива. Сложность: O(n)"""
        self.heap = array[:]
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sink_down(i)

    def validate_heap(self):
        """Проверка свойства max-кучи. Сложность: O(n)"""
        for i in range(len(self.heap)):
            left = self._left(i)
            right = self._right(i)
            if left != -1 and self.heap[i] < self.heap[left]:
                return False
            if right != -1 and self.heap[i] < self.heap[right]:
                return False
        return True

    def render(self):
        """Визуализация."""
        if not self.heap:
            return "Empty heap"

        def _rec(idx, prefix="", is_left=True):
            result = ""
            right = self._right(idx)
            if right != -1:
                result += _rec(right, prefix + ("│   " if is_left else "    "), False)

            result += prefix + ("└── " if is_left else "┌── ") + str(self.heap[idx]) + "\n"

            left = self._left(idx)
            if left != -1:
                result += _rec(left, prefix + ("    " if is_left else "│   "), True)

            return result

        return _rec(0)
