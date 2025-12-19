import time
import random
import string
import json
from typing import Callable, Dict, Tuple, List
from datetime import datetime
import platform
import psutil

from kmp_search import kmp_search, kmp_search_first
from z_function import z_search
from string_matching import boyer_moore_search, rabin_karp_search

def make_random_sequence(length: int, alphabet_size: int = 4) -> str:
    alphabet = string.ascii_uppercase[:alphabet_size]
    return ''.join(random.choice(alphabet) for _ in range(length))

def make_repeating_sequence(base: str, times: int) -> str:
    return base * times

def make_single_char_sequence(char: str, length: int) -> str:
    return char * length

def make_worst_case_sequence(pattern: str, total_len: int) -> str:
    if len(pattern) == 0:
        return ""
    
    used_symbols = set(pattern)
    for symbol in string.ascii_uppercase:
        if symbol not in used_symbols:
            return symbol * total_len
    
    return '0' * total_len

def measure_performance(
    algorithm_func: Callable,
    text_data: str,
    pattern_data: str,
    runs: int = 1
) -> Tuple[float, List]:
    start_moment = time.perf_counter()
    
    output = None
    for _ in range(runs):
        output = algorithm_func(text_data, pattern_data)
    
    end_moment = time.perf_counter()
    elapsed = end_moment - start_moment
    
    return elapsed, output

def run_full_benchmark() -> Dict:
    print("\n" + "=" * 80)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ ПОИСКА")
    print("=" * 80)
    
    print("\n" + "-" * 80)
    print("ИНФОРМАЦИЯ О СИСТЕМЕ:")
    print("-" * 80)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Операционная система: {platform.system()} {platform.release()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Объем RAM: {psutil.virtual_memory().total / (1024**3):.2f} ГБ")
    print(f"Количество ядер: {psutil.cpu_count()}")
    
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "system_details": {
            "os": f"{platform.system()} {platform.release()}",
            "processor": platform.processor(),
            "ram_gb": psutil.virtual_memory().total / (1024**3),
            "cpu_count": psutil.cpu_count()
        },
        "measurements": {}
    }
    
    algorithm_list = {
        "KMP": kmp_search,
        "Z-алгоритм": z_search,
        "Бойер-Мур": boyer_moore_search,
        "Рабин-Карп": rabin_karp_search,
    }
    
    test_scenarios = {
        "Случайные символы (малый алфавит)": {
            "text": make_random_sequence(10000, alphabet_size=4),
            "pattern": make_random_sequence(10, alphabet_size=4),
            "info": "10000 символов, алфавит из 4 букв"
        },
        "Случайные символы (полный алфавит)": {
            "text": make_random_sequence(10000, alphabet_size=26),
            "pattern": make_random_sequence(10, alphabet_size=26),
            "info": "10000 символов, 26 букв"
        },
        "Повторяющийся паттерн": {
            "text": make_repeating_sequence("XYZ", 3000),
            "pattern": "XYZXZ",
            "info": "Повтор 'XYZ' 3000 раз"
        },
        "Однотипные символы": {
            "text": make_single_char_sequence("B", 10000),
            "pattern": "BBB",
            "info": "10000 символов 'B'"
        },
        "Неудачный сценарий": {
            "text": make_worst_case_sequence("XYZ", 10000),
            "pattern": "XYZ",
            "info": "Текст не содержит паттерн"
        }
    }
    
    for scenario_name, scenario_data in test_scenarios.items():
        print(f"\n" + "-" * 80)
        print(f"СЦЕНАРИЙ: {scenario_name}")
        print("-" * 80)
        print(f"Описание: {scenario_data['info']}")
        print(f"Длина текста: {len(scenario_data['text'])}")
        print(f"Длина шаблона: {len(scenario_data['pattern'])}")
        
        scenario_results = {}
        
        for algo_name, algo_func in algorithm_list.items():
            iterations = 100 if len(scenario_data['text']) < 1000 else 10
            
            total_time, found_positions = measure_performance(
                algo_func,
                scenario_data['text'],
                scenario_data['pattern'],
                iterations
            )
            
            time_per_run = total_time / iterations
            
            scenario_results[algo_name] = {
                "total_time": total_time,
                "time_per_run": time_per_run,
                "iterations": iterations,
                "matches_found": len(found_positions) if found_positions else 0
            }
            
            print(f"\n  {algo_name}:")
            print(f"    Время на запуск: {time_per_run * 1e6:.3f} мкс")
            print(f"    Найдено совпадений: {len(found_positions) if found_positions else 0}")
        
        results_data["measurements"][scenario_name] = scenario_results
        
        fastest_algo = min(scenario_results.items(), key=lambda x: x[1]['time_per_run'])
        print(f"\n  ЛУЧШИЙ РЕЗУЛЬТАТ: {fastest_algo[0]} ({fastest_algo[1]['time_per_run'] * 1e6:.3f} мкс)")
    
    return results_data

def run_scalability_test() -> Dict:
    print("\n" + "=" * 80)
    print("ТЕСТИРОВАНИЕ МАСШТАБИРУЕМОСТИ")
    print("=" * 80)
    
    output_data = {"scalability_test": {}}
    
    text_sizes = [1000, 5000, 10000, 50000, 100000]
    sample_pattern = "PQRST"
    
    algorithms = {
        "KMP": kmp_search,
        "Z-алгоритм": z_search,
        "Рабин-Карп": rabin_karp_search,
    }
    
    print(f"\nОбразец для поиска: '{sample_pattern}'")
    print(f"Тип текста: Случайные символы (5 букв)\n")
    
    for size_val in text_sizes:
        print(f"Размер: {size_val:6d} - ", end="", flush=True)
        text_sample = make_random_sequence(size_val, alphabet_size=5)
        
        size_results = {}
        
        for algo_name, algo_func in algorithms.items():
            start_point = time.perf_counter()
            algo_func(text_sample, sample_pattern)
            elapsed_time = time.perf_counter() - start_point
            
            size_results[algo_name] = elapsed_time * 1e6
            print(f"{algo_name}: {elapsed_time*1e6:8.2f} мкс | ", end="", flush=True)
        
        print()
        output_data["scalability_test"][size_val] = size_results
    
    return output_data

def run_worst_case_test() -> Dict:
    print("\n" + "=" * 80)
    print("АНАЛИЗ НЕУДАЧНЫХ СЦЕНАРИЕВ")
    print("=" * 80)
    
    output_data = {"worst_scenarios": {}}
    
    test_cases = {
        "Паттерн в начале": ("PQRSTU" + make_random_sequence(5000, 4), "PQR"),
        "Паттерн в конце": (make_random_sequence(5000, 4) + "PQRSTU", "PQR"),
        "Паттерн отсутствует": (make_random_sequence(5000, 4), "WXY"),
        "Частичные совпадения": (make_repeating_sequence("AABAAAB", 500), "AABAAC"),
    }
    
    algorithms = {
        "KMP": kmp_search,
        "Z-алгоритм": z_search,
        "Бойер-Мур": boyer_moore_search,
        "Рабин-Карп": rabin_karp_search,
    }
    
    for case_name, (text_sample, pattern_sample) in test_cases.items():
        print(f"\n{case_name}:")
        print(f"  Длина текста: {len(text_sample)}, Паттерн: {pattern_sample}")
        
        case_results = {}
        
        for algo_name, algo_func in algorithms.items():
            start_point = time.perf_counter()
            result_data = algo_func(text_sample, pattern_sample)
            elapsed_time = time.perf_counter() - start_point
            
            case_results[algo_name] = {
                "time_microseconds": elapsed_time * 1e6,
                "matches_count": len(result_data) if result_data else 0
            }
            
            print(f"  {algo_name:15s}: {elapsed_time*1e6:10.2f} мкс ({len(result_data) if result_data else 0} совпад.)")
        
        output_data["worst_scenarios"][case_name] = case_results
    
    return output_data

def run_pattern_length_test() -> Dict:
    print("\n" + "=" * 80)
    print("ВЛИЯНИЕ ДЛИНЫ ПАТТЕРНА НА СКОРОСТЬ")
    print("=" * 80)
    
    output_data = {"pattern_length_impact": {}}
    
    text_sample = make_random_sequence(50000, alphabet_size=4)
    pattern_lengths = [1, 3, 5, 10, 20, 50, 100]
    
    algorithms = {
        "KMP": kmp_search,
        "Z-алгоритм": z_search,
        "Рабин-Карп": rabin_karp_search,
    }
    
    print(f"Длина текста: {len(text_sample)}\n")
    
    for pattern_len in pattern_lengths:
        print(f"Длина паттерна: {pattern_len:3d} - ", end="", flush=True)
        pattern_sample = make_random_sequence(pattern_len, alphabet_size=4)
        
        length_results = {}
        
        for algo_name, algo_func in algorithms.items():
            start_point = time.perf_counter()
            algo_func(text_sample, pattern_sample)
            elapsed_time = time.perf_counter() - start_point
            
            length_results[algo_name] = elapsed_time * 1e6
            print(f"{algo_name}: {elapsed_time*1e6:8.2f} мкс | ", end="", flush=True)
        
        print()
        output_data["pattern_length_impact"][pattern_len] = length_results
    
    return output_data

if __name__ == "__main__":
    final_results = {}
    
    final_results.update(run_full_benchmark())
    
    scalability_data = run_scalability_test()
    final_results.update(scalability_data)
    
    worst_case_data = run_worst_case_test()
    final_results.update(worst_case_data)
    
    pattern_analysis_data = run_pattern_length_test()
    final_results.update(pattern_analysis_data)
    
    print("\n" + "=" * 80)
    print("СОХРАНЕНИЕ ИТОГОВЫХ ДАННЫХ")
    print("=" * 80)
    
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Результаты сохранены в файл 'benchmark_results.json'")