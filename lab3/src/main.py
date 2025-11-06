import os
import csv
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt  # requirements includes matplotlib
from timeit import default_timer as timer

from modules import recursion, memoization, recursion_tasks

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "report")
REPORT_DIR = os.path.normpath(REPORT_DIR)
os.makedirs(REPORT_DIR, exist_ok=True)

def experiment_fibonacci(n_values):
    times_naive = []
    times_memo = []
    for n in n_values:
        # naive timing (use the counted version to ensure call counting) -- may be slow
        memoization.reset_naive_counter()
        t0 = timer()
        val_naive = recursion.fibonacci_naive(n) if n <= 20 else None  # prevent huge waits: compute naive up to 20 directly
        t1 = timer()
        # But user requested comparison for n=35 specifically; we'll measure 35 using counted versions in memoization.compare...
        times_naive.append((val_naive, t1 - t0))

        # memoized timing
        fib_mem, get_count, reset_mem = memoization.make_memoized_fib()
        reset_mem()
        t0 = timer()
        val_mem = fib_mem(n)
        t1 = timer()
        times_memo.append((val_mem, t1 - t0))
    return times_naive, times_memo

def run_full_experiments():
    # 1) Compare naive vs memo for n=35 (as requested)
    print("Сравнение для n=35 (наивная и мемоизированная)...")
    cmp35 = memoization.compare_naive_and_memo(35)
    print("n =", cmp35['n'])
    print("Наивная: value={}, time={:.3f}s, calls={}".format(cmp35['naive']['value'], cmp35['naive']['time'], cmp35['naive']['calls']))
    print("Мемоизация: value={}, time={:.6f}s, calls={}".format(cmp35['memo']['value'], cmp35['memo']['time'], cmp35['memo']['calls']))

    # 2) Экспериментальное исследование: измерим времена для n=0..35
    ns = list(range(0, 36))
    times_naive = []
    times_memo = []
    for n in ns:
        # naive (guard: naive can be slow for n>30, but user wanted experimental — we do it up to 35; could take time)
        t0 = timer()
        # use fibonacci_naive_counted to count
        from modules.memoization import reset_naive_counter, fibonacci_naive_counted
        reset_naive_counter()
        val_naive = fibonacci_naive_counted(n)
        t1 = timer()
        naive_time = t1 - t0

        # memoized
        fib_mem, get_count, reset_mem = memoization.make_memoized_fib()
        reset_mem()
        t0 = timer()
        val_memo = fib_mem(n)
        t1 = timer()
        memo_time = t1 - t0

        times_naive.append(naive_time)
        times_memo.append(memo_time)
        print(f"n={n}: naive_time={naive_time:.6f}s memo_time={memo_time:.6f}s")

    # 3) Сохранить график
    fig_path = os.path.join(REPORT_DIR, "fib_times.png")
    plt.figure(figsize=(10,6))
    plt.plot(ns, times_naive, label='naive')
    plt.plot(ns, times_memo, label='memoized')
    plt.yscale('log')  # log-scale to visualize wide range
    plt.xlabel('n')
    plt.ylabel('time (s, log scale)')
    plt.title('Fibonacci: naive vs memoized')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    print("График сохранён в", fig_path)

    # 4) Бинарный поиск (пример)
    arr = list(range(0, 100, 2))
    idx = recursion_tasks.binary_search_recursive(arr, 42)
    print("binary_search_recursive: index of 42 in even array:", idx)

    # 5) Обход файловой системы (пример на текущей папке проекта)
    start_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("Рекурсивный обход (корень):", start_path)
    lines, max_depth = recursion_tasks.walk_dir_recursive(start_path)
    tree_path = os.path.join(REPORT_DIR, "tree.txt")
    with open(tree_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Дерево сохранено в {tree_path}. Макс глубина (директорий): {max_depth}")

    # 6) Ханойские башни пример n=4 (печать последовательности)
    n_hanoi = 4
    moves = recursion_tasks.hanoi_moves(n_hanoi, 'A', 'C', 'B')
    moves_path = os.path.join(REPORT_DIR, f"hanoi_{n_hanoi}_moves.txt")
    with open(moves_path, "w", encoding="utf-8") as f:
        for i, (s, d) in enumerate(moves, 1):
            f.write(f"{i}: {s} -> {d}\n")
    print(f"Ханой ({n_hanoi}): {len(moves)} перемещений. Последовательность сохранена в {moves_path}")

if __name__ == "__main__":
    run_full_experiments()
