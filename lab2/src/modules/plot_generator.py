import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os

def save_plot(fig, filename):
    os.makedirs('lab2/report', exist_ok=True)
    fig.savefig(f'lab2/report/{filename}', dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_insertion_comparison(sizes, list_times, linked_list_times):
    """График сравнения вставки в начало"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(sizes, list_times, 'ro-', label='list.insert(0)', linewidth=2, markersize=6)
    ax.plot(sizes, linked_list_times, 'bo-', label='LinkedList.insert_at_start', linewidth=2, markersize=6)
    
    ax.set_xlabel('Количество элементов')
    ax.set_ylabel('Время выполнения (секунды)')
    ax.set_title('Сравнение производительности вставки в начало')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_plot(fig, 'insertion_comparsion.png')
    return fig

def plot_queue_comparison(sizes, list_times, deque_times):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(sizes, list_times, 'ro-', label='list.pop(0)', linewidth=2, markersize=6)
    ax.plot(sizes, deque_times, 'go-', label='deque.popleft()', linewidth=2, markersize=6)
    
    ax.set_xlabel('Количество операций')
    ax.set_ylabel('Время выполнения (секунды)')
    ax.set_title('Сравнение производительности операций очереди')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_plot(fig, 'queue_comparsion.png')
    return fig

def plot_asymptotic_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Теоретическая сложность
    n = list(range(1, 1001, 10))
    
    # O(1) vs O(n) для вставки
    o1 = [1] * len(n)
    on = n
    
    ax1.plot(n, o1, 'b-', label='O(1) - LinkedList.insert_at_start', linewidth=2)
    ax1.plot(n, on, 'r-', label='O(n) - list.insert(0)', linewidth=2)
    ax1.set_xlabel('n (количество элементов)')
    ax1.set_ylabel('Временная сложность')
    ax1.set_title('Асимптотическая сложность вставки в начало')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # O(1) vs O(n) для удаления из начала
    ax2.plot(n, o1, 'g-', label='O(1) - deque.popleft()', linewidth=2)
    ax2.plot(n, on, 'r-', label='O(n) - list.pop(0)', linewidth=2)
    ax2.set_xlabel('n (количество элементов)')
    ax2.set_ylabel('Временная сложность')
    ax2.set_title('Асимптотическая сложность удаления из начала')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    save_plot(fig, 'asymptotic_complexity.png')
    return fig

def generate_all_plots(insertion_data, queue_data):
    plot_insertion_comparison(*insertion_data)
    plot_queue_comparison(*queue_data)
    plot_asymptotic_comparison()
    print("Все графики сохранены в папку 'lab2/report/'")