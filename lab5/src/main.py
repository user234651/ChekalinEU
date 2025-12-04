from modules.hash_functions import HashFunction, sum_hash, poly_hash, djb2_hash
from modules.hash_table_chaining import HashTableChaining
from modules.hash_table_open_addressing import OpenAddressingHashTable
from modules import performance_analysis, plot_generator

def demo_hash_tables():
    print("=== Демонстрация работы HashTableChaining ===")
    ht_chain = HashTableChaining(hash_fn=HashFunction(sum_hash, "sum_hash"))
    ht_chain.insert("apple", 1)
    ht_chain.insert("banana", 2)
    ht_chain.insert("cherry", 3)
    print("Размер:", ht_chain.size)
    print("Получаем banana:", ht_chain.get("banana"))
    ht_chain.delete("banana")
    print("После удаления banana:", ht_chain.get("banana"))
    print("Содержит apple?", "apple" in ht_chain)
    print()

    print("=== Демонстрация работы OpenAddressingHashTable ===")
    ht_open = OpenAddressingHashTable(method='double', hash_fn=HashFunction(djb2_hash, "djb2_hash"))
    ht_open.insert("apple", 1)
    ht_open.insert("banana", 2)
    ht_open.insert("cherry", 3)
    print("Размер:", ht_open.size)
    print("Получаем cherry:", ht_open.get("cherry"))
    ht_open.delete("cherry")
    print("После удаления cherry:", ht_open.get("cherry"))

def demo_performance_analysis():
    print("\n=== Анализ производительности ===")
    results = performance_analysis.analyze_performance()
    for hf_name, hf_data in results.items():
        print(f"\nХеш-функция: {hf_name}")
        for lf, timings in hf_data.items():
            print(f"  Коэффициент заполнения: {lf}")
            print(f"    Chaining: insert={timings['chaining']['insert_time']:.6f}s, "
                  f"get={timings['chaining']['get_time']:.6f}s, "
                  f"delete={timings['chaining']['delete_time']:.6f}s")
            print(f"    OpenAddressing: insert={timings['open_addressing']['insert_time']:.6f}s, "
                  f"get={timings['open_addressing']['get_time']:.6f}s, "
                  f"delete={timings['open_addressing']['delete_time']:.6f}s")
    return results

if __name__ == "__main__":
    demo_hash_tables()
    demo_performance_analysis()
    plot_generator.generate_all_plots(demo_performance_analysis())
