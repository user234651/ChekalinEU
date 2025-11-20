from typing import List
import heapq

def bubble_sort(arr: List[int]) -> List[int]:
    """
    Bubble Sort
    Time complexity:
      Worst: O(n^2)
      Average: O(n^2)
      Best: O(n)
    Space complexity: O(1) extra
    """
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def insertion_sort(arr: List[int]) -> List[int]:
    """
    Insertion Sort
    Time complexity:
      Worst: O(n^2)
      Average: O(n^2)
      Best: O(n)
    Space complexity: O(1) extra
    """
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr: List[int]) -> List[int]:
    """
    Merge Sort (stable)
    Time complexity:
      Worst: O(n log n)
      Average: O(n log n)
      Best: O(n log n)
    Space complexity: O(n) extra
    """
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # merge
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick Sort (Lomuto partition, recursive)
    Time complexity:
      Worst: O(n^2) (плохой выбор опорного элемента; например, отсортированные входы)
      Average: O(n log n)
      Best: O(n log n)
    Space complexity: O(log n) average (рекурсивный стек), O(n) worst
    """
    a = arr.copy()
    def _quick(a, lo, hi):
        if lo >= hi:
            return
        pivot = a[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while a[i] < pivot:
                i += 1
            while a[j] > pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1; j -= 1
        if lo < j:
            _quick(a, lo, j)
        if i < hi:
            _quick(a, i, hi)
    _quick(a, 0, len(a)-1)
    return a

def heap_sort(arr: List[int]) -> List[int]:
    """
    Heap Sort
    Time complexity:
      Worst: O(n log n)
      Average: O(n log n)
      Best: O(n log n)
    Space complexity: O(n) extra if using heaps created from data (here we make a copy)
    """
    a = arr.copy()
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]
