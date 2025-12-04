import time
import random
import matplotlib.pyplot as plt
from modules.greedy_algorithms import GreedyMethods, PackSolver, TimeInterval, PackItem
import string
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
report_dir = os.path.join(base_dir, 'report')

os.makedirs(report_dir, exist_ok=True)

output_path = os.path.join(report_dir, 'analysis.png')

def analyze_interval():
    """Анализ задачи выбора непересекающихся интервалов."""
    print("=== АНАЛИЗ: ОТБОР ИНТЕРВАЛОВ ===\n")

    intervals = [
        TimeInterval(1, 3, "A"),
        TimeInterval(2, 5, "B"),
        TimeInterval(4, 7, "C"),
        TimeInterval(6, 9, "D"),
        TimeInterval(8, 10, "E"),
        TimeInterval(1, 2, "F"),
    ]

    print("Все интервалы:")
    for it in intervals:
        print(f"  {it.name}: [{it.start}, {it.end}]")

    chosen = GreedyMethods.schedule_intervals(intervals)

    print("\nВыбранные (жадно):")
    for it in chosen:
        print(f"  {it.name}: [{it.start}, {it.end}]")

    print(f"\nВсего выбрано: {len(chosen)}")

    sizes = [10, 50, 100, 500, 1000]
    times = []

    print("\nЗамеры времени:")
    for size in sizes:
        test_intervals = []
        for i in range(size):
            start = random.randint(0, size * 2)
            end = start + random.randint(1, 10)
            test_intervals.append(TimeInterval(start, end, f"Task_{i}"))

        t0 = time.perf_counter()
        GreedyMethods.schedule_intervals(test_intervals)
        t1 = time.perf_counter()

        elapsed = (t1 - t0) * 1000
        times.append(elapsed)
        print(f"  Размер {size}: {elapsed:.3f} мс")

    return sizes, times

def analyze_knapsack():
    """Анализ методов для рюкзака."""
    print("\n=== АНАЛИЗ: РЮКЗАК ===\n")

    capacity = 10
    items = [
        PackItem(60, 10, "Item1"),
        PackItem(100, 20, "Item2"),
        PackItem(120, 30, "Item3"),
    ]

    greedy_val, exact_val = PackSolver.compare_pack_methods(capacity, items)

    print("\n--- Пример нестандартного случая ---")
    capacity_small = 10
    tricky = [
        PackItem(60, 6, "X"),
        PackItem(50, 5, "Y"),
        PackItem(50, 5, "Z"),
    ]

    PackSolver.compare_pack_methods(capacity_small, tricky)

    sizes = [10, 20, 50, 100]
    frac_times = []
    zero_one_times = []

    print("\nЗамеры времени:")
    for size in sizes:
        test_items = []
        for i in range(size):
            weight = random.randint(1, 20)
            value = random.randint(1, 100)
            test_items.append(PackItem(value, weight, f"Item_{i}"))

        capacity_test = size * 5

        t0 = time.perf_counter()
        GreedyMethods.fractional_pack(capacity_test, test_items)
        t1 = time.perf_counter()
        frac_times.append((t1 - t0) * 1000)

        if size <= 20:
            t0 = time.perf_counter()
            PackSolver.brute_force_0_1_pack(capacity_test, test_items)
            t1 = time.perf_counter()
            zero_one_times.append((t1 - t0) * 1000)
        else:
            zero_one_times.append(None)

        print(f"  Размер {size}: непрерывный={frac_times[-1]:.3f} мс, 0-1={zero_one_times[-1] if zero_one_times[-1] else 'N/A'} мс")

    return sizes, frac_times, zero_one_times

def analyze_huffman():
    """Анализ кодирования Хаффмана."""
    print("\n=== АНАЛИЗ: ХАФФМАН ===\n")

    test_text = "this is an example for huffman encoding"
    print(f"Исход: '{test_text}'")
    print(f"Длина: {len(test_text)} символов")
    print(f"ASCII: {len(test_text) * 8} бит")

    codes, encoded_text, tree = GreedyMethods.huffman_encode(test_text)
    print(f"\nЗакодированно: {encoded_text}")
    print(f"Длина кода: {len(encoded_text)} бит")
    print(f"Коэфф. сжатия: {len(encoded_text) / (len(test_text) * 8):.2%}")

    print("\nКоды:")
    for ch, code in sorted(codes.items()):
        print(f"  '{ch}': {code}")

    def print_tree(node, prefix="", is_left=True):
        if node is None:
            return ""
        result = ""
        if node.right:
            result += print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        char_repr = f"'{node.char}'" if node.char else "internal"
        result += prefix + ("└── " if is_left else "┌── ") + f"{char_repr}({node.freq})\n"
        if node.left:
            result += print_tree(node.left, prefix + ("    " if is_left else "│   "), True)
        return result

    print("\nДерево:")
    print(print_tree(tree))

    sizes = [100, 500, 1000, 5000, 10000]
    times = []
    ratios = []

    print("\nЗамеры:")
    for size in sizes:
        text = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=size))
        t0 = time.perf_counter()
        codes, encoded, _ = GreedyMethods.huffman_encode(text)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        ratio = len(encoded) / (len(text) * 8)
        times.append(elapsed)
        ratios.append(ratio)
        print(f"  Размер {size}: время={elapsed:.3f} мс, сжатие={ratio:.2%}")

    return sizes, times, ratios

def analyze_prim():
    """Анализ алгоритма Прима."""
    print("\n=== АНАЛИЗ: PRIM ===\n")

    vertices = ['A', 'B', 'C', 'D']
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 3),
        ('B', 'C', 2),
        ('B', 'D', 4),
        ('C', 'D', 5),
    ]

    print("Граф:")
    for u, v, w in edges:
        print(f"  {u} -- {v} (w: {w})")

    mst = GreedyMethods.prim_mst(vertices, edges)

    print("\nMST:")
    total = 0
    for e in mst:
        print(f"  {e.u} -- {e.v} (w: {e.weight})")
        total += e.weight

    print(f"Общий вес: {total}")

    return total, mst

def run_comprehensive_analysis():
    """Запуск комплексного анализа всех реализованных алгоритмов."""
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ ЖАДНЫХ АЛГОРИТМОВ ===\n")
    print()

    interval_sizes, interval_times = analyze_interval()
    kn_sizes, frac_times, zero_one_times = analyze_knapsack()
    h_sizes, h_times, comp_ratios = analyze_huffman()
    mst_weight, mst_edges = analyze_prim()

    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.plot(interval_sizes, interval_times, 'o-', label='Выбор интервалов', linewidth=2)
    plt.plot(kn_sizes, frac_times, 's-', label='Непрерывный рюкзак', linewidth=2)
    plt.plot(h_sizes[:len(h_times)], h_times, '^-', label='Хаффман', linewidth=2)

    available_sizes = [s for s, t in zip(kn_sizes, zero_one_times) if t is not None]
    available_times = [t for t in zero_one_times if t is not None]
    if available_sizes:
        plt.plot(available_sizes, available_times, 'd-', label='0-1 (перебор)', linewidth=2)

    plt.xlabel('Размер входа')
    plt.ylabel('Время (мс)')
    plt.title('Производительность')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')

    plt.subplot(2, 2, 2)
    plt.plot(h_sizes, comp_ratios, 'o-', linewidth=2)
    plt.xlabel('Размер текста')
    plt.ylabel('Коэфф. сжатия')
    plt.title('Хаффман: эффективность')
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 3)
    x_pos = range(len(kn_sizes))
    plt.bar([x - 0.2 for x in x_pos], frac_times, 0.4, label='Непрерывный', alpha=0.8)
    zero_one_available = [t if t else 0 for t in zero_one_times]
    plt.bar([x + 0.2 for x in x_pos], zero_one_available, 0.4, label='0-1 (перебор)', alpha=0.8)
    plt.xlabel('Размер задачи')
    plt.ylabel('Время (мс)')
    plt.title('Рюкзак: сравнение')
    plt.xticks(x_pos, kn_sizes)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 4)
    demo_sizes = [10, 20, 50, 100]
    selected_counts = []
    for size in demo_sizes:
        test_intervals = []
        for i in range(size):
            start = random.randint(0, size * 2)
            end = start + random.randint(1, 10)
            test_intervals.append(TimeInterval(start, end, f"Task_{i}"))
        sel = GreedyMethods.schedule_intervals(test_intervals)
        selected_counts.append(len(sel))

    plt.plot(demo_sizes, selected_counts, 'o-', linewidth=2)
    plt.xlabel('Всего интервалов')
    plt.ylabel('Выбрано')
    plt.title('Отбор интервалов')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

    print("\nАнализ завершён. Графики в 'analysis.png'")

if __name__ == "__main__":
    random.seed(42)
    run_comprehensive_analysis()
