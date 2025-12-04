import time
import random
import matplotlib.pyplot as plt
from modules.heap import SmallHeap
from modules.heapsort import inplace_heapsort, heapsort_using_smallheap
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
report_dir = os.path.join(base_dir, 'report')

os.makedirs(report_dir, exist_ok=True)

output_path = os.path.join(report_dir, 'analysis.png')

def measure_heap_operations():
    """Измеряем время ключевых операций над кучей. Сложность отмечена там, где важно."""
    print("=== АНАЛИЗ ВЫЧИСЛИТЕЛЬНОЙ СЛОЖНОСТИ ДЕЙСТВИЙ С HEAP ===\n")
    print()

    sizes = [100, 500, 1000, 5000, 10000]
    build_heap_times = []
    sequential_insert_times = []
    extract_all_times = []

    print("Размер | Build (мс) | SeqInsert (мс) | ExtractAll (мс)")
    print("-" * 75)

    for size in sizes:
        array = random.sample(range(size * 10), size)

        start_time = time.perf_counter()
        heap1 = SmallHeap(array)
        build_time = (time.perf_counter() - start_time) * 1000

        heap2 = SmallHeap()
        start_time = time.perf_counter()
        for value in array:
            heap2.push(value)
        insert_time = (time.perf_counter() - start_time) * 1000

        start_time = time.perf_counter()
        while len(heap1) > 0:
            heap1.pop()
        extract_time = (time.perf_counter() - start_time) * 1000

        build_heap_times.append(build_time)
        sequential_insert_times.append(insert_time)
        extract_all_times.append(extract_time)

        print(f"{size:6} | {build_time:9.2f} | {insert_time:13.2f} | {extract_time:13.2f}")

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, build_heap_times, 'o-', label='Build Heap (O(n))', linewidth=2)
    plt.plot(sizes, sequential_insert_times, 's-', label='Sequential Insert (O(n log n))', linewidth=2)
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (мс)')
    plt.title('Build vs Sequential Insert')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(sizes, extract_all_times, 'o-', label='Extract All', linewidth=2)
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (мс)')
    plt.title('Извлечение всех элементов')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

    return sizes, build_heap_times, sequential_insert_times, extract_all_times

def compare_sorting_algorithms():
    """Сравнение времени разных алгоритмов сортировки (ориентиры по сложности)."""
    print("\n=== СРАВНЕНИЕ АЛГОРИТМОВ СОРТИРОВКИ ===\n")

    sizes = [100, 500, 1000, 5000, 10000]
    heapsort_times = []
    quicksort_times = []
    mergesort_times = []
    builtin_sort_times = []

    print("Размер | Heapsort (мс) | Quicksort (мс) | Mergesort (мс) | Built-in (мс)")
    print("-" * 85)

    for size in sizes:
        array = random.sample(range(size * 10), size)

        arr1 = array[:]
        start_time = time.perf_counter()
        inplace_heapsort(arr1)
        heapsort_time = (time.perf_counter() - start_time) * 1000

        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quicksort(left) + middle + quicksort(right)

        arr2 = array[:]
        start_time = time.perf_counter()
        quicksort(arr2)
        quicksort_time = (time.perf_counter() - start_time) * 1000

        def mergesort(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = mergesort(arr[:mid])
            right = mergesort(arr[mid:])
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        arr3 = array[:]
        start_time = time.perf_counter()
        mergesort(arr3)
        mergesort_time = (time.perf_counter() - start_time) * 1000

        arr4 = array[:]
        start_time = time.perf_counter()
        sorted(arr4)
        builtin_time = (time.perf_counter() - start_time) * 1000

        heapsort_times.append(heapsort_time)
        quicksort_times.append(quicksort_time)
        mergesort_times.append(mergesort_time)
        builtin_sort_times.append(builtin_time)

        print(
            f"{size:6} | {heapsort_time:13.2f} | {quicksort_time:14.2f} | {mergesort_time:13.2f} | {builtin_time:12.2f}")

    plt.figure(figsize=(10, 6))

    plt.plot(sizes, heapsort_times, 'o-', label='Heapsort', linewidth=2)
    plt.plot(sizes, quicksort_times, 's-', label='Quicksort', linewidth=2)
    plt.plot(sizes, mergesort_times, '^-', label='Mergesort', linewidth=2)
    plt.plot(sizes, builtin_sort_times, 'd-', label='Built-in (Timsort)', linewidth=2)

    plt.xlabel('Количество элементов')
    plt.ylabel('Время (мс)')
    plt.title('Сравнение алгоритмов')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

    return sizes, heapsort_times, quicksort_times, mergesort_times, builtin_sort_times

if __name__ == "__main__":
    random.seed(42)

    measure_heap_operations()
    compare_sorting_algorithms()
