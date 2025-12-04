import unittest
import random
from modules.heap import SmallHeap, LargeHeap
from modules.heapsort import heapsort_using_smallheap, heapsort_using_largeheap, inplace_heapsort
from modules.priority_queue import TaskQueue

class TestSmallHeap(unittest.TestCase):
    """Тесты для SmallHeap."""

    def setUp(self):
        self.heap = SmallHeap()

    def test_empty_heap(self):
        self.assertEqual(len(self.heap), 0)
        self.assertIsNone(self.heap.top())
        self.assertIsNone(self.heap.pop())
        self.assertTrue(self.heap.validate_heap())

    def test_push_and_top(self):
        self.heap.push(5)
        self.assertEqual(self.heap.top(), 5)
        self.assertEqual(len(self.heap), 1)

        self.heap.push(3)
        self.assertEqual(self.heap.top(), 3)

        self.heap.push(7)
        self.assertEqual(self.heap.top(), 3)

        self.assertTrue(self.heap.validate_heap())

    def test_pop(self):
        values = [5, 3, 8, 1, 9, 2]
        for val in values:
            self.heap.push(val)

        self.assertTrue(self.heap.validate_heap())

        extracted = []
        while len(self.heap) > 0:
            extracted.append(self.heap.pop())
            if len(self.heap) > 0:
                self.assertTrue(self.heap.validate_heap())

        self.assertEqual(extracted, sorted(values))

    def test_heapify(self):
        array = [12, 5, 2, 7, 1, 8, 3]
        heap = SmallHeap(array)

        self.assertTrue(heap.validate_heap())
        self.assertEqual(len(heap), len(array))

        prev = heap.pop()
        while len(heap) > 0:
            current = heap.pop()
            self.assertLessEqual(prev, current)
            prev = current

    def test_large_heap(self):
        size = 1000
        values = random.sample(range(10000), size)

        heap = SmallHeap(values)
        self.assertTrue(heap.validate_heap())

        extracted = []
        for _ in range(size):
            extracted.append(heap.pop())

        self.assertEqual(extracted, sorted(values))

class TestLargeHeap(unittest.TestCase):
    """Тесты для LargeHeap."""

    def test_basic_operations(self):
        heap = LargeHeap()

        values = [5, 3, 8, 1, 9, 2]
        for val in values:
            heap.push(val)

        self.assertTrue(heap.validate_heap())

        extracted = []
        while len(heap) > 0:
            extracted.append(heap.pop())

        self.assertEqual(extracted, sorted(values, reverse=True))

    def test_heapify_max(self):
        array = [12, 5, 2, 7, 1, 8, 3]
        heap = LargeHeap(array)

        self.assertTrue(heap.validate_heap())

        prev = heap.pop()
        while len(heap) > 0:
            current = heap.pop()
            self.assertGreaterEqual(prev, current)
            prev = current

class TestHeapsort(unittest.TestCase):
    """Тесты для heapsort."""

    def test_heapsort_smallheap(self):
        array = [10, 4, 1, 8, 2, 9, 5, 7, 3]
        sorted_array = heapsort_using_smallheap(array)
        self.assertEqual(sorted_array, sorted(array))

    def test_heapsort_largeheap(self):
        array = [10, 4, 1, 8, 2, 9, 5, 7, 3]
        sorted_array = heapsort_using_largeheap(array)
        self.assertEqual(sorted_array, sorted(array))

    def test_inplace_heapsort(self):
        array = [10, 4, 1, 8, 2, 9, 5, 7, 3]
        original = array[:]
        sorted_array = inplace_heapsort(array)

        self.assertEqual(sorted_array, sorted(original))
        self.assertEqual(array, sorted(original))

    def test_empty_array(self):
        self.assertEqual(inplace_heapsort([]), [])

    def test_single_element(self):
        self.assertEqual(inplace_heapsort([5]), [5])

    def test_large_array(self):
        size = 1000
        array = random.sample(range(10000), size)
        sorted_array = inplace_heapsort(array[:])

        self.assertEqual(sorted_array, sorted(array))

class TestTaskQueue(unittest.TestCase):
    """Тесты для приоритетной очереди."""

    def setUp(self):
        self.pq = TaskQueue()

    def test_push_pop(self):
        self.pq.push_with_priority("task1", 3)
        self.pq.push_with_priority("task2", 1)
        self.pq.push_with_priority("task3", 2)

        self.assertEqual(self.pq.pop_priority(), "task2")
        self.assertEqual(self.pq.pop_priority(), "task3")
        self.assertEqual(self.pq.pop_priority(), "task1")
        self.assertIsNone(self.pq.pop_priority())

    def test_peek(self):
        self.pq.push_with_priority("task1", 2)
        self.pq.push_with_priority("task2", 1)

        self.assertEqual(self.pq.peek_priority(), "task2")
        self.assertEqual(self.pq.peek_priority(), "task2")
        self.assertEqual(self.pq.pop_priority(), "task2")

    def test_empty_queue(self):
        self.assertTrue(self.pq.empty())
        self.assertIsNone(self.pq.pop_priority())
        self.assertIsNone(self.pq.peek_priority())

    def test_priority_order(self):
        tasks = [
            ("low", 3),
            ("high", 1),
            ("medium", 2),
            ("urgent", 0),
        ]

        for value, priority in tasks:
            self.pq.push_with_priority(value, priority)

        expected_order = ["urgent", "high", "medium", "low"]
        for expected in expected_order:
            self.assertEqual(self.pq.pop_priority(), expected)

if __name__ == "__main__":
    unittest.main()
