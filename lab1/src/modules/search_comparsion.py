import time
import random
import os

def linear_search(arr, target):
    for i in range(len(arr)):  # O(n)
        if arr[i] == target:   # O(1)
            return i           # O(1)
    return -1                  # O(1)
# Общая сложность: O(n)

def binary_search(arr, target):
    left = 0                              # O(1)
    right = len(arr) - 1                  # O(1)
    
    while left <= right:                  # O(log n)
        mid = (left + right) // 2         # O(1)
        if arr[mid] == target:            # O(1)
            return mid                    # O(1)
        elif arr[mid] < target:           # O(1)
            left = mid + 1                # O(1)
        else:                             # O(1)
            right = mid - 1               # O(1)
    return -1                             # O(1)
# Общая сложность: O(log n)

def generate_sorted_array(size):
    arr = [random.randint(1, size * 10) for _ in range(size)]  # O(n)
    arr.sort()                                                 # O(n log n)
    return arr                                                 # O(1)
# Общая сложность: O(n log n)

def save_array_to_file(arr, filename):
    with open(filename, 'w') as f:                    # O(1)
        for num in arr:                               # O(n)
            f.write(f"{num}\n")                       # O(1)
# Общая сложность: O(n)

def load_array_from_file(filename):
    arr = []                                         # O(1)
    with open(filename, 'r') as f:                   # O(1)
        for line in f:                               # O(n)
            arr.append(int(line.strip()))            # O(1)
    return arr                                       # O(1)
# Общая сложность: O(n)

def measure_search_time(search_func, arr, target, iterations=100):
    total_time = 0                                   # O(1)
    
    for _ in range(iterations):                      # O(iterations)
        start_time = time.time()                     # O(1)
        search_func(arr, target)                     # O(сложность search_func)
        end_time = time.time()                       # O(1)
        total_time += (end_time - start_time)        # O(1)
    
    return total_time / iterations                   # O(1)
# Общая сложность: O(iterations * сложность search_func)

def prepare_test_data():
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]  # O(1)
    arrays = {}                                      # O(1)
    targets = {}                                     # O(1)
    
    # Создаем директорию для данных, если её нет
    os.makedirs('lab1/src/data', exist_ok=True)     # O(1)
    
    for size in sizes:                              # O(len(sizes))
        # Генерируем массив
        arr = generate_sorted_array(size)           # O(n log n)
        arrays[size] = arr                          # O(1)
        
        # Сохраняем в файл
        filename = f'lab1/src/data/array_{size}.txt'     # O(1)
        save_array_to_file(arr, filename)           # O(n)
        
        # Определяем ТОЛЬКО СРЕДНИЙ элемент для тестирования
        targets[size] = arr[size // 2]              # O(1)
    
    return arrays, targets                          # O(1)
# Общая сложность: O(Σ(n_i log n_i)) где n_i - размеры массивов

def run_performance_analysis():
    print("Подготовка тестовых данных...")          # O(1)
    arrays, targets = prepare_test_data()           # O(Σ(n_i log n_i))
    
    results = []                                    # O(1)
    iterations = 10                                 # O(1)
    
    print("Запуск анализа производительности...")   # O(1)
    
    for size, arr in arrays.items():                # O(len(sizes))
        print(f"Тестирование массива размером {size}...")  # O(1)
        
        # Берем ТОЛЬКО СРЕДНИЙ элемент для тестирования
        target_value = targets[size]                # O(1)
        
        # Линейный поиск
        linear_time = measure_search_time(linear_search, arr, target_value, iterations)  # O(iterations * n)
        
        # Бинарный поиск
        binary_time = measure_search_time(binary_search, arr, target_value, iterations)  # O(iterations * log n)
        
        results.append({                            # O(1)
            'size': size,
            'target_type': 'middle',                # Теперь только один тип
            'linear_time': linear_time,
            'binary_time': binary_time
        })
        
        print(f"  средний элемент: линейный={linear_time:.6f}s, бинарный={binary_time:.6f}s")  # O(1)
    
    return results                                  # O(1)
# Общая сложность: O(Σ(iterations * (n_i + log n_i)))