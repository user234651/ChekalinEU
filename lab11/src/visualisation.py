import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

from prefix_function import compute_prefix_function, compute_prefix_function_verbose
from z_function import compute_z_function, compute_z_function_verbose

def plot_algorithm_comparison():
    """График сравнения алгоритмов."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results_data = json.load(f)
    except FileNotFoundError:
        print("Файл benchmark_results.json не найден.")
        return
    
    benchmarks_data = results_data.get("measurements", {})
    
    algorithms_list = ["KMP", "Z-алгоритм", "Бойер-Мур", "Рабин-Карп"]
    
    test_names = list(benchmarks_data.keys())
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x_positions = range(len(test_names))
    bar_width = 0.2
    
    for idx, algo_name in enumerate(algorithms_list):
        times_data = []
        for test_name in test_names:
            if test_name in benchmarks_data:
                time_val = benchmarks_data[test_name].get(algo_name, {}).get("time_per_run", 0)
                times_data.append(time_val)
        
        if times_data:
            ax.bar([p + idx * bar_width for p in x_positions], times_data, bar_width, label=algo_name)
    
    ax.set_xlabel("Тип теста", fontsize=12)
    ax.set_ylabel("Время (микросекунды)", fontsize=12)
    ax.set_title("Сравнение алгоритмов поиска", fontsize=14, fontweight='bold')
    ax.set_xticks([p + bar_width * 1.5 for p in x_positions])
    ax.set_xticklabels([name[:20] for name in test_names], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("01_algorithm_comparison.png", dpi=150)
    print("Сохранён график: 01_algorithm_comparison.png")
    plt.close()

def plot_scalability():
    """График масштабируемости."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results_data = json.load(f)
    except FileNotFoundError:
        return
    
    scalability_data = results_data.get("scalability_test", {})
    
    if not scalability_data:
        return
    
    text_sizes = sorted([int(k) for k in scalability_data.keys()])
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms_list = ["KMP", "Z-алгоритм", "Рабин-Карп"]
    
    for algo_name in algorithms_list:
        times_data = [scalability_data[str(size)].get(algo_name, 0) for size in text_sizes]
        ax.plot(text_sizes, times_data, marker='o', linewidth=2, markersize=8, label=algo_name)
    
    ax.set_xlabel("Размер текста (символов)", fontsize=12)
    ax.set_ylabel("Время (микросекунды)", fontsize=12)
    ax.set_title("Масштабируемость алгоритмов", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig("02_scalability.png", dpi=150)
    print("Сохранён график: 02_scalability.png")
    plt.close()

def plot_pattern_size_influence():
    """Влияние длины паттерна на производительность."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results_data = json.load(f)
    except FileNotFoundError:
        return
    
    pattern_data = results_data.get("pattern_length_impact", {})
    
    if not pattern_data:
        return
    
    pattern_sizes = sorted([int(k) for k in pattern_data.keys()])
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms_list = ["KMP", "Z-алгоритм", "Рабин-Карп"]
    
    for algo_name in algorithms_list:
        times_data = [pattern_data[str(size)].get(algo_name, 0) for size in pattern_sizes]
        ax.plot(pattern_sizes, times_data, marker='s', linewidth=2, markersize=8, label=algo_name)
    
    ax.set_xlabel("Длина паттерна (символов)", fontsize=12)
    ax.set_ylabel("Время (микросекунды)", fontsize=12)
    ax.set_title("Влияние длины паттерна", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("03_pattern_size_influence.png", dpi=150)
    print("Сохранён график: 03_pattern_size_influence.png")
    plt.close()

def plot_worst_case_analysis():
    """Анализ неудачных сценариев."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results_data = json.load(f)
    except FileNotFoundError:
        return
    
    worst_case_data = results_data.get("worst_scenarios", {})
    
    if not worst_case_data:
        return
    
    test_cases = list(worst_case_data.keys())
    algorithms_list = ["KMP", "Z-алгоритм", "Бойер-Мур", "Рабин-Карп"]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x_positions = range(len(test_cases))
    bar_width = 0.2
    
    for idx, algo_name in enumerate(algorithms_list):
        times_data = []
        for test_case in test_cases:
            time_val = worst_case_data[test_case].get(algo_name, {}).get("time_microseconds", 0)
            times_data.append(time_val)
        
        ax.bar([p + idx * bar_width for p in x_positions], times_data, bar_width, label=algo_name)
    
    ax.set_xlabel("Тестовый сценарий", fontsize=12)
    ax.set_ylabel("Время (микросекунды)", fontsize=12)
    ax.set_title("Анализ неудачных случаев", fontsize=14, fontweight='bold')
    ax.set_xticks([p + bar_width * 1.5 for p in x_positions])
    ax.set_xticklabels(test_cases, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("04_worst_case_analysis.png", dpi=150)
    print("Сохранён график: 04_worst_case_analysis.png")
    plt.close()

def visualize_prefix_function():
    """Визуализация префикс-функции."""
    
    test_strings = [
        "XYXY",
        "ZZZZ",
        "XYZXYZXY",
        "AABAAAB",
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, s in enumerate(test_strings):
        pi_result = compute_prefix_function(s)
        
        ax = axes[idx]
        
        x_vals = range(len(s))
        ax.bar(x_vals, pi_result, color='steelblue', alpha=0.7, edgecolor='black')
        
        for i, char in enumerate(s):
            ax.text(i, -0.5, char, ha='center', fontsize=12, fontweight='bold')
        
        for i, val in enumerate(pi_result):
            ax.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel("Позиция", fontsize=11)
        ax.set_ylabel("Значение", fontsize=11)
        ax.set_title(f"Префикс-функция для '{s}'", fontsize=12, fontweight='bold')
        ax.set_xticks(x_vals)
        ax.set_ylim(-1, max(pi_result) + 1 if pi_result else 1)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("05_prefix_function_visualization.png", dpi=150)
    print("Сохранён график: 05_prefix_function_visualization.png")
    plt.close()

def visualize_z_function():
    """Визуализация Z-функции."""
    
    test_strings = [
        "XYXY",
        "ZZZZ",
        "ABCDA",
        "AABAAAB",
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, s in enumerate(test_strings):
        z_result = compute_z_function(s)
        
        ax = axes[idx]
        
        x_vals = range(len(s))
        colors = ['green' if z_result[i] > 0 else 'lightcoral' for i in range(len(z_result))]
        ax.bar(x_vals, z_result, color=colors, alpha=0.7, edgecolor='black')
        
        for i, char in enumerate(s):
            ax.text(i, -0.5, char, ha='center', fontsize=12, fontweight='bold')
        
        for i, val in enumerate(z_result):
            if val > 0:
                ax.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel("Позиция", fontsize=11)
        ax.set_ylabel("Значение", fontsize=11)
        ax.set_title(f"Z-функция для '{s}'", fontsize=12, fontweight='bold')
        ax.set_xticks(x_vals)
        ax.set_ylim(-1, max(z_result) + 1 if z_result else 1)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("06_z_function_visualization.png", dpi=150)
    print("Сохранён график: 06_z_function_visualization.png")
    plt.close()

def create_summary_visualization():
    """Создание сводной визуализации."""
    
    fig = plt.figure(figsize=(16, 10))
    
    fig.suptitle('Алгоритмы поиска подстроки - Сводка результатов', 
                fontsize=16, fontweight='bold', y=0.98)
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results_data = json.load(f)
            system_info = results_data.get("system_details", {})
            
            info_text = (f"Система: {system_info.get('os', 'Неизвестно')} | "
                        f"Ядра: {system_info.get('cpu_count', '?')} | "
                        f"Память: {system_info.get('ram_gb', 0):.1f} ГБ | "
                        f"Дата: {results_data.get('timestamp', 'Неизвестно')[:10]}")
            fig.text(0.5, 0.955, info_text, ha='center', fontsize=10, style='italic')
    except:
        pass
    
    gs = fig.add_gridspec(3, 2, left=0.08, right=0.95, top=0.93, bottom=0.05, hspace=0.3, wspace=0.3)
    
    ax_info = fig.add_subplot(gs[0, :])
    ax_info.axis('off')
    
    info_text = """
    ОСНОВНЫЕ ВЫВОДЫ:
    • KMP (Кнут-Моррис-Пратт): Универсальный алгоритм для любых случаев
    • Бойер-Мур: Эффективен при больших алфавитах и отсутствии совпадений
    • Z-алгоритм: Хорош для анализа строк и поиска периодов
    • Рабин-Карп: Полезен при поиске нескольких шаблонов одновременно
    """
    ax_info.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[2, 1])
    
    s1 = "XYZXYZXY"
    pi_result = compute_prefix_function(s1)
    ax1.bar(range(len(s1)), pi_result, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_title(f"Префикс-функция: '{s1}'", fontweight='bold')
    ax1.set_ylabel("Значение")
    ax1.set_xticks(range(len(s1)))
    ax1.set_xticklabels(list(s1))
    
    s2 = "AABAAAB"
    z_result = compute_z_function(s2)
    colors = ['green' if z_result[i] > 0 else 'lightcoral' for i in range(len(z_result))]
    ax2.bar(range(len(s2)), z_result, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_title(f"Z-функция: '{s2}'", fontweight='bold')
    ax2.set_ylabel("Значение")
    ax2.set_xticks(range(len(s2)))
    ax2.set_xticklabels(list(s2))
    
    ax3.axis('off')
    complexity_data = [
        ['Алгоритм', 'Время', 'Память', 'Лучший случай'],
        ['KMP', 'O(n+m)', 'O(m)', 'Любые строки'],
        ['Z-алгоритм', 'O(n+m)', 'O(n)', 'Анализ строк'],
        ['Бойер-Мур', 'O(n/m)', 'O(|Σ|)', 'Большие алфавиты'],
        ['Рабин-Карп', 'O(n+m)', 'O(1)', 'Множество шаблонов'],
    ]
    
    table = ax3.table(cellText=complexity_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.25, 0.25, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    for i in range(len(complexity_data[0])):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax3.set_title("Сложность алгоритмов", fontweight='bold', pad=20)
    
    ax4.axis('off')
    recommendations = """
    РЕКОМЕНДАЦИИ:
    
    • Короткие шаблоны или периодические тексты
      → Используйте KMP или Z-алгоритм
    
    • Большой алфавит (текст, ДНК)
      → Используйте Бойера-Мура
    
    • Поиск нескольких шаблонов сразу
      → Используйте Рабина-Карпа
    
    • Требования реального времени
      → Используйте Бойера-Мура
    
    • Ограничения по памяти
      → Используйте Рабина-Карпа
    """
    ax4.text(0.05, 0.95, recommendations, fontsize=10, verticalalignment='top',
            family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.savefig("00_summary_visualization.png", dpi=150, bbox_inches='tight')
    print("Сохранён график: 00_summary_visualization.png")
    plt.close()

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("СОЗДАНИЕ ГРАФИКОВ И ДИАГРАММ")
    print("=" * 80)
    
    print("\nСоздание сводной визуализации...")
    create_summary_visualization()
    
    print("\nСоздание графика сравнения алгоритмов...")
    plot_algorithm_comparison()
    
    print("\nСоздание графика масштабируемости...")
    plot_scalability()
    
    print("\nСоздание графика влияния длины паттерна...")
    plot_pattern_size_influence()
    
    print("\nСоздание графика анализа неудачных случаев...")
    plot_worst_case_analysis()
    
    print("\nСоздание визуализации префикс-функции...")
    visualize_prefix_function()
    
    print("\nСоздание визуализации Z-функции...")
    visualize_z_function()
    
    print("\n" + "=" * 80)
    print("ГРАФИКИ УСПЕШНО СОЗДАНЫ")
    print("=" * 80)
    
    print("\nСозданные файлы:")
    png_files = list(Path(".").glob("*.png"))
    for i, file in enumerate(sorted(png_files), 1):
        print(f"  {i}. {file.name}")