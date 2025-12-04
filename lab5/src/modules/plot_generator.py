import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

# Папка для сохранения графиков
REPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../report"))
os.makedirs(REPORT_DIR, exist_ok=True)

def plot_operation_times(results: Dict):
    """
    Строит графики времени операций (insert/get/delete) для каждой хеш-функции
    и каждого типа хеш-таблицы в зависимости от коэффициента заполнения.
    """
    for hf_name, hf_data in results.items():
        for table_type in ['chaining', 'open_addressing']:
            load_factors = sorted(hf_data.keys())
            insert_times = [hf_data[lf][table_type]['insert_time'] for lf in load_factors]
            get_times = [hf_data[lf][table_type]['get_time'] for lf in load_factors]
            delete_times = [hf_data[lf][table_type]['delete_time'] for lf in load_factors]

            plt.figure(figsize=(8, 5))
            plt.plot(load_factors, insert_times, marker='o', label='Insert')
            plt.plot(load_factors, get_times, marker='s', label='Get')
            plt.plot(load_factors, delete_times, marker='^', label='Delete')
            plt.xlabel("Коэффициент заполнения")
            plt.ylabel("Время (с)")
            plt.title(f"{table_type.capitalize()} - Время операций ({hf_name})")
            plt.legend()
            plt.grid(True)
            filename = os.path.join(REPORT_DIR, f"{table_type}_{hf_name}_times.png")
            plt.savefig(filename)
            plt.close()
            print(f"Сохранено: {filename}")


def plot_collision_histogram(hash_table_class, hash_fn, num_keys=1000):
    """
    Строит гистограмму распределения коллизий для указанной хеш-функции.
    Для цепочек - длины бакетов, для открытой адресации - количество попыток вставки.
    """
    from modules.hash_table_chaining import HashTableChaining
    from modules.hash_table_open_addressing import OpenAddressingHashTable

    keys = [f"key_{i}" for i in range(num_keys)]
    
    if hash_table_class == HashTableChaining:
        ht = HashTableChaining(initial_capacity=101, hash_fn=hash_fn)
        for i, k in enumerate(keys):
            ht.insert(k, i)
        bucket_lengths = [len(bucket) for bucket in ht._buckets]
        plt.figure(figsize=(8, 5))
        plt.hist(bucket_lengths, bins=range(max(bucket_lengths)+2), edgecolor='black')
        plt.xlabel("Длина цепочки")
        plt.ylabel("Количество бакетов")
        plt.title(f"Распределение коллизий (Chaining) - {hash_fn.name}")
        filename = os.path.join(REPORT_DIR, f"chaining_collision_{hash_fn.name}.png")
        plt.savefig(filename)
        plt.close()
        print(f"Сохранено: {filename}")

    elif hash_table_class == OpenAddressingHashTable:
        ht = OpenAddressingHashTable(initial_capacity=101, method='linear', hash_fn=hash_fn)
        probe_counts = []
        for i, k in enumerate(keys):
            count = 0
            idx = ht._find_slot(k)
            # подсчёт коллизий (количество проб)
            for j in range(ht._capacity):
                probe_idx = ht._probe(k, j)
                current = ht._keys[probe_idx]
                count += 1
                if current is None or current is ht._deleted:
                    break
            probe_counts.append(count)
            ht.insert(k, i)

        plt.figure(figsize=(8, 5))
        plt.hist(probe_counts, bins=range(max(probe_counts)+2), edgecolor='black')
        plt.xlabel("Количество проб для вставки")
        plt.ylabel("Количество ключей")
        plt.title(f"Распределение коллизий (OpenAddressing) - {hash_fn.name}")
        filename = os.path.join(REPORT_DIR, f"open_collision_{hash_fn.name}.png")
        plt.savefig(filename)
        plt.close()
        print(f"Сохранено: {filename}")


def generate_all_plots(results):
    # Время операций
    plot_operation_times(results)
    
    # Гистограммы коллизий
    from modules.hash_functions import HashFunction, sum_hash, poly_hash, djb2_hash
    from modules.hash_table_chaining import HashTableChaining
    from modules.hash_table_open_addressing import OpenAddressingHashTable

    hash_functions = [
        HashFunction(sum_hash, "sum_hash"),
        HashFunction(poly_hash, "poly_hash"),
        HashFunction(djb2_hash, "djb2_hash")
    ]

    for hf in hash_functions:
        plot_collision_histogram(HashTableChaining, hf)
        plot_collision_histogram(OpenAddressingHashTable, hf)
