import matplotlib.pyplot as plt
import numpy as np

def plot_search_performance(results):
    sizes = sorted(set(r['size'] for r in results))  # O(n log n)
    
    linear_times = []                                # O(1)
    binary_times = []                                # O(1)
    
    for size in sizes:                               # O(len(sizes))
        size_results = [r for r in results if r['size'] == size]  # O(n)
        avg_linear = np.mean([r['linear_time'] for r in size_results])  # O(n)
        avg_binary = np.mean([r['binary_time'] for r in size_results])  # O(n)
        linear_times.append(avg_linear)              # O(1)
        binary_times.append(avg_binary)              # O(1)
    
    plt.figure(figsize=(12, 8))                      # O(1)
    
    plt.subplot(2, 1, 1)                            # O(1)
    plt.plot(sizes, linear_times, 'b-o', label='Линейный поиск')  # O(n)
    plt.xlabel('Размер массива')                     # O(1)
    plt.ylabel('Время (секунды)')                    # O(1)
    plt.title('Зависимость времени линейного поиска от размера массива')  # O(1)
    plt.grid(True)                                   # O(1)
    plt.legend()                                     # O(1)
    plt.yscale('log')                                # O(1)

    plt.subplot(2, 1, 2)                            # O(1)
    plt.plot(sizes, binary_times, 'r-o', label='Бинарный поиск')  # O(n)
    plt.xlabel('Размер массива')                     # O(1)
    plt.ylabel('Время (секунды)')                    # O(1)
    plt.title('Зависимость времени бинарного поиска от размера массива')  # O(1)
    plt.grid(True)                                   # O(1)
    plt.legend()                                     # O(1)
    plt.yscale('log')                                # O(1)
    
    plt.tight_layout()                               # O(1)
    plt.savefig('lab1/report/search_performance.png')   # O(1)
    plt.show()                                       # O(1)
# Общая сложность: O(n log n)

def plot_comparsion(results):
    sizes = sorted(set(r['size'] for r in results))  # O(n log n)
    
    linear_times = []                                # O(1)
    binary_times = []                                # O(1)
    
    for size in sizes:                               # O(len(sizes))
        size_results = [r for r in results if r['size'] == size]  # O(n)
        avg_linear = np.mean([r['linear_time'] for r in size_results])  # O(n)
        avg_binary = np.mean([r['binary_time'] for r in size_results])  # O(n)
        linear_times.append(avg_linear)              # O(1)
        binary_times.append(avg_binary)              # O(1)
    
    plt.figure(figsize=(10, 6))                      # O(1)
    plt.plot(sizes, linear_times, 'b-o', label='Линейный поиск O(n)')  # O(n)
    plt.plot(sizes, binary_times, 'r-o', label='Бинарный поиск O(log n)')  # O(n)
    plt.xlabel('Размер массива')                     # O(1)
    plt.ylabel('Время (секунды)')                    # O(1)
    plt.title('Сравнение производительности алгоритмов поиска')  # O(1)
    plt.grid(True)                                   # O(1)
    plt.legend()                                     # O(1)
    plt.yscale('log')                                # O(1)
    plt.xscale('log')                                # O(1)
    
    plt.tight_layout()                               # O(1)
    plt.savefig('lab1/report/search_comparison.png')    # O(1)
    plt.show()                                       # O(1)
# Общая сложность: O(n log n)