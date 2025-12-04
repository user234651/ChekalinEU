import timeit
from typing import List, Callable
from modules.hash_functions import HashFunction, sum_hash, poly_hash, djb2_hash
from modules.hash_table_chaining import HashTableChaining
from modules.hash_table_open_addressing import OpenAddressingHashTable

HASH_FUNCTIONS = [
    HashFunction(sum_hash, "sum_hash"),
    HashFunction(poly_hash, "poly_hash"),
    HashFunction(djb2_hash, "djb2_hash")
]

LOAD_FACTORS = [0.1, 0.5, 0.7, 0.9]
NUM_KEYS = 1000

def generate_keys(n: int) -> List[str]:
    return [f"key_{i}" for i in range(n)]

def measure_time(hash_table_class: Callable, hash_fn: HashFunction, load_factor: float, num_keys: int = NUM_KEYS) -> dict:
    keys = generate_keys(num_keys)
    ht = hash_table_class(initial_capacity=max(11, int(num_keys / load_factor)), hash_fn=hash_fn)

    # Вставка
    insert_time = timeit.timeit(lambda: [ht.insert(k, i) for i, k in enumerate(keys)], number=1)

    # Получение
    get_time = timeit.timeit(lambda: [ht.get(k) for k in keys], number=1)

    # Удаление
    delete_time = timeit.timeit(lambda: [ht.delete(k) for k in keys], number=1)

    return {
        "insert_time": insert_time,
        "get_time": get_time,
        "delete_time": delete_time
    }

def analyze_performance():
    results = {}

    for hf in HASH_FUNCTIONS:
        results[hf.name] = {}
        for lf in LOAD_FACTORS:
            chaining_result = measure_time(HashTableChaining, hf, lf)
            open_result = measure_time(lambda **kwargs: OpenAddressingHashTable(method='linear', **kwargs), hf, lf)
            results[hf.name][lf] = {
                "chaining": chaining_result,
                "open_addressing": open_result
            }

    return results
