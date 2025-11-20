# src/main.py
from modules.performance_analysis import measure_insert
from modules.hash_functions import simple_hash, polynomial_hash, djb2_hash
from modules.hash_table_chaining import ChainingHashTable
from modules.hash_table_open_addressing import OpenAddressingHashTable

def main():
    tables = [
        (ChainingHashTable, simple_hash, 'Chaining Simple'),
        (OpenAddressingHashTable, polynomial_hash, 'Open Linear Poly', 'linear'),
        (OpenAddressingHashTable, djb2_hash, 'Open Double DJB2', 'double')
    ]
    for t in tables:
        table_class, hash_func, name = t[:3]
        probe_type = t[3] if len(t) > 3 else 'linear'
        time_taken = measure_insert(table_class, hash_func, n=5000, probe_type=probe_type)
        print(f"{name}: {time_taken:.5f}s")

if __name__ == "__main__":
    main()
