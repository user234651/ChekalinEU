import time
import random
import matplotlib.pyplot as plt
from modules.binary_search_tree import BinTree, BNode
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
report_dir = os.path.join(base_dir, 'report')

os.makedirs(report_dir, exist_ok=True)

output_path = os.path.join(report_dir, 'bst_performance_analysis.png')

def build_balanced_tree(size):
    """
    Генерация «случайного» сбалансированного дерева.

    Сложность: вставки суммарно O(n log n) в среднем.
    """
    tree = BinTree()
    values = random.sample(range(size * 3), size)

    for value in values:
        tree.add(value)

    return tree, values


def build_degenerate_tree(size):
    """
    Генерация вырожденного дерева (возрастающая последовательность).

    Сложность: O(n)
    """
    tree = BinTree()
    values = list(range(size))

    if size > 990:
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(size + 100)

    try:
        for value in values:
            tree.add(value)
    finally:
        if size > 990:
            sys.setrecursionlimit(old_limit)

    return tree, values


def build_degenerate_tree_iterative(size):
    """
    Построение вырожденного дерева напрямую, без рекурсий.
    Сложность: O(n)
    """
    tree = BinTree()

    if size == 0:
        return tree, []

    values = list(range(size))

    tree.root = BNode(values[0])
    current = tree.root

    for i in range(1, size):
        current.right = BNode(values[i])
        current = current.right

    return tree, values


def measure_find_time(tree, search_values, num_searches=1000):
    """
    Замер среднего времени поиска.
    Сложность: O(num_searches)
    """
    start_time = time.perf_counter()

    for _ in range(num_searches):
        value = random.choice(search_values)
        tree.find(value)

    end_time = time.perf_counter()

    return (end_time - start_time) / num_searches


def run_analysis():
    print("=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ BST ===\n")

    print(f"Текущий лимит рекурсии: {sys.getrecursionlimit()}")
    print()

    sizes = [100, 500, 800, 1000, 1500, 2000]
    balanced_times = []
    degenerate_times = []
    balanced_heights = []
    degenerate_heights = []

    print("Размер | Баланс. время (мкс) | Вырожд. время (мкс) | Баланс. высота | Вырожд. высота")
    print("-" * 85)

    for size in sizes:
        try:
            print(f"Обрабатываем размер: {size}...")

            balanced_tree, balanced_values = build_balanced_tree(size)

            if size > 800:
                degenerate_tree, degenerate_values = build_degenerate_tree_iterative(size)
            else:
                degenerate_tree, degenerate_values = build_degenerate_tree(size)

            balanced_time = measure_find_time(balanced_tree, balanced_values) * 1e6
            degenerate_time = measure_find_time(degenerate_tree, degenerate_values) * 1e6

            balanced_height = balanced_tree.compute_height()
            degenerate_height = degenerate_tree.compute_height()

            balanced_times.append(balanced_time)
            degenerate_times.append(degenerate_time)
            balanced_heights.append(balanced_height)
            degenerate_heights.append(degenerate_height)

            print(f"{size:6} | {balanced_time:18.2f} | {degenerate_time:19.2f} | {balanced_height:13} | {degenerate_height:14}")

        except RecursionError as e:
            print(f"Пропуск размера {size} из-за ошибки рекурсии: {e}")
            continue
        except Exception as e:
            print(f"Ошибка при размере {size}: {e}")
            continue

    if balanced_times and degenerate_times:
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(sizes[:len(balanced_times)], balanced_times, 'o-', label='Сбалансированное дерево', linewidth=2)
        plt.plot(sizes[:len(degenerate_times)], degenerate_times, 's-', label='Вырожденное дерево', linewidth=2)
        plt.xlabel('Количество элементов')
        plt.ylabel('Время поиска (микросекунды)')
        plt.title('Зависимость времени поиска от размера дерева')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.plot(sizes[:len(balanced_heights)], balanced_heights, 'o-', label='Сбалансированное дерево', linewidth=2)
        plt.plot(sizes[:len(degenerate_heights)], degenerate_heights, 's-', label='Вырожденное дерево', linewidth=2)
        plt.plot(sizes, [size - 1 for size in sizes], '--', label='Идеальная высота (n-1)', alpha=0.7)
        plt.plot(sizes, [1.44 * (size + 1).bit_length() for size in sizes], '--',
                 label='Теоретическая высота (~1.44log2n)', alpha=0.7)
        plt.xlabel('Количество элементов')
        plt.ylabel('Высота дерева')
        plt.title('Зависимость высоты дерева от количества элементов')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()

        print("\nАнализ завершен успешно! Графики сохранены в 'bst_performance_analysis.png'")
    else:
        print("Не удалось получить данные для построения графиков.")

    return sizes, balanced_times, degenerate_times, balanced_heights, degenerate_heights


if __name__ == "__main__":
    run_analysis()
