from modules.heap import SmallHeap, LargeHeap
from modules.heapsort import heapsort_using_smallheap, heapsort_using_largeheap, inplace_heapsort
from modules.priority_queue import TaskQueue
import random

def demonstrate_heap_operations():
    """Короткая демонстрация основных операций с min-кучей."""
    print("=== ДЕМОНСТРАЦИЯ ОСНОВНЫХ ОПЕРАЦИЙ С SmallHeap ===\n")

    heap = SmallHeap()
    values = [10, 4, 1, 8, 2, 9, 5, 7, 3]

    print(f"Исходный набор: {values}")

    print("\nПоследовательная вставка:")
    for value in values:
        heap.push(value)
        print(f"После push {value}: {heap}")

    print(f"\nВид кучи:")
    print(heap.render())

    print(f"Корень (минимум): {heap.top()}")
    print(f"Куча валидна: {heap.validate_heap()}")

    print("\nИзвлечение по возрастанию:")
    extracted = []
    while len(heap) > 0:
        value = heap.pop()
        extracted.append(value)
        print(f"Извлечено {value}, текущая куча: {heap}")

    print(f"Извлеченные: {extracted}")
    print(f"Ожидаемый отсортированный: {sorted(values)}")

def demonstrate_heap_construction():
    """Демонстрация построения кучи из массива."""
    print("\n\n=== СОЗДАНИЕ КУЧИ ИЗ МАССИВА ===\n")

    array = [11, 6, 2, 9, 3, 10, 4]
    print(f"Массив: {array}")

    heap = SmallHeap(array)
    print(f"Куча после heapify: {heap}")
    print(f"Валидность: {heap.validate_heap()}")

    print("\nТекстовая визуализация:")
    print(heap.render())

def demonstrate_max_heap():
    """Пример работы max-кучи."""
    print("\n\n=== DEMO LargeHeap (max) ===\n")

    array = [11, 6, 2, 9, 3, 10, 4]
    heap = LargeHeap(array)

    print(f"Массив: {array}")
    print(f"LargeHeap: {heap}")
    print(f"Корень (макс): {heap.top()}")
    print(f"Корректность: {heap.validate_heap()}")

    print("\nВизуализация:")
    print(heap.render())

    print("\nИзвлечение по убыванию:")
    extracted = []
    while len(heap) > 0:
        extracted.append(heap.pop())

    print(f"Извлечено: {extracted}")

def demonstrate_heapsort():
    """Короткий показ пирамидальной сортировки."""
    print("\n\n=== HEAPSORT DEMO ===\n")

    array = [10, 4, 1, 8, 2, 9, 5, 7, 3]
    print(f"Исходный: {array}")

    sorted_array = inplace_heapsort(array[:])
    print(f"Отсортировано (in-place): {sorted_array}")

    print(f"Совпадает с sorted: {sorted_array == sorted(array)}")

def demonstrate_priority_queue():
    """Демонстрация приоритетной очереди."""
    print("\n\n=== TASK QUEUE DEMO ===\n")

    pq = TaskQueue()

    tasks = [
        ("Обычное", 2),
        ("Срочно", 1),
        ("Очень срочно", 0),
        ("Менее срочно", 3),
    ]

    print("Добавляем задачи:")
    for value, priority in tasks:
        pq.push_with_priority(value, priority)
        print(f"Добавлено: {value} с приоритетом {priority}")

    print(f"\nСостояние: {pq}")
    print(f"Следующая задача: {pq.peek_priority()}")

    print("\nВыполняем по приоритету:")
    while not pq.empty():
        task = pq.pop_priority()
        print(f"Выполнена: {task}")

def demonstrate_large_example():
    """Небольшая демонстрация на большом наборе."""
    print("\n\n=== ДЕМО НА БОЛЬШОМ НАБОРЕ ===\n")

    size = 20
    large_array = random.sample(range(100), size)

    print(f"Большой массив ({size}): {large_array[:10]}...")

    heap = SmallHeap(large_array)
    sorted_elements = []

    for i in range(min(5, size)):
        sorted_elements.append(heap.pop())

    print(f"Первые 5 элементов: {sorted_elements}")
    print(f"Осталось в куче: {len(heap)}")

if __name__ == "__main__":
    random.seed(42)

    demonstrate_heap_operations()
    demonstrate_heap_construction()
    demonstrate_max_heap()
    demonstrate_heapsort()
    demonstrate_priority_queue()
    demonstrate_large_example()
